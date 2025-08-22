"""
响应生成器工具
"""

import json
import re
from datetime import datetime
from typing import Any, Dict, Optional

from faker import Faker
from jinja2 import Template

fake = Faker("zh_CN")


class ResponseGenerator:
    """响应生成器类"""

    @staticmethod
    def generate_response(
        mock_config, request_data: Dict[str, Any]
    ) -> tuple[Dict[str, Any], Dict[str, str]]:
        """
        生成响应数据

        Args:
            mock_config: Mock配置对象
            request_data: 请求数据

        Returns:
            tuple: (响应体, 响应头)
        """
        # 生成响应体
        if mock_config.response_template:
            # 使用模板生成响应
            response_body = ResponseGenerator._render_template(
                mock_config.response_template, request_data
            )
        elif mock_config.response_body:
            # 使用静态响应体
            response_body = ResponseGenerator._process_dynamic_fields(
                mock_config.response_body, request_data
            )
        else:
            # 默认响应
            response_body = {
                "message": "Mock response",
                "timestamp": datetime.now().isoformat(),
                "path": request_data.get("path", ""),
                "method": request_data.get("method", ""),
            }

        # 生成响应头
        response_headers = mock_config.response_headers or {}
        default_headers = {
            "Content-Type": "application/json",
            "X-Mock-Response": "true",
            "X-Mock-Timestamp": datetime.now().isoformat(),
        }
        response_headers = {**default_headers, **response_headers}

        return response_body, response_headers

    @staticmethod
    def _render_template(template_str: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """渲染Jinja2模板"""
        try:
            # 添加faker函数到模板上下文
            template_context = {
                **context,
                "fake": fake,
                "now": datetime.now(),
                "timestamp": datetime.now().isoformat(),
            }

            template = Template(template_str)
            rendered = template.render(**template_context)

            # 尝试解析为JSON
            try:
                return json.loads(rendered)
            except json.JSONDecodeError:
                return {"content": rendered}

        except Exception as e:
            return {
                "error": "Template rendering failed",
                "message": str(e),
                "template": template_str,
            }

    @staticmethod
    def _process_dynamic_fields(
        response_body: Dict[str, Any], request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """处理响应体中的动态字段"""

        def process_value(value):
            if isinstance(value, str):
                # 处理占位符
                value = ResponseGenerator._replace_placeholders(value, request_data)
            elif isinstance(value, dict):
                # 递归处理字典
                value = {k: process_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                # 递归处理列表
                value = [process_value(item) for item in value]

            return value

        return process_value(response_body)

    @staticmethod
    def _replace_placeholders(text: str, context: Dict[str, Any]) -> str:
        """替换文本中的占位符"""

        # 替换请求参数占位符 {{request.param_name}}
        def replace_request_param(match):
            param_name = match.group(1)
            params = context.get("params", {})
            return str(params.get(param_name, f"{{{{request.{param_name}}}}}"))

        text = re.sub(r"\{\{request\.(\w+)\}\}", replace_request_param, text)

        # 替换时间占位符
        text = text.replace("{{now}}", datetime.now().isoformat())
        text = text.replace("{{timestamp}}", str(int(datetime.now().timestamp())))

        # 替换Faker占位符
        faker_patterns = {
            "{{fake.name}}": lambda: fake.name(),
            "{{fake.email}}": lambda: fake.email(),
            "{{fake.phone}}": lambda: fake.phone_number(),
            "{{fake.address}}": lambda: fake.address(),
            "{{fake.company}}": lambda: fake.company(),
            "{{fake.uuid}}": lambda: fake.uuid4(),
            "{{fake.number}}": lambda: str(fake.random_int(1, 1000)),
            "{{fake.text}}": lambda: fake.text(max_nb_chars=100),
        }

        for pattern, generator in faker_patterns.items():
            if pattern in text:
                text = text.replace(pattern, generator())

        return text
