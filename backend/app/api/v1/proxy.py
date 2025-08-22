"""
Mock代理服务API路由
"""

import time
from typing import Any, Dict

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from ...api.deps import get_db
from ...services.log_service import LogService
from ...services.mock_service import MockService
from ...utils.response_generator import ResponseGenerator

router = APIRouter()


@router.api_route(
    "/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
)
async def mock_proxy(request: Request, path: str, db: Session = Depends(get_db)):
    """Mock代理服务 - 处理所有Mock请求"""
    start_time = time.time()

    # 获取请求信息
    method = request.method
    full_path = f"/{path}"

    # 获取请求数据
    request_headers = dict(request.headers)
    request_params = dict(request.query_params)

    # 获取请求体
    request_body = None
    try:
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                request_body = await request.json()
            elif "application/x-www-form-urlencoded" in content_type:
                form_data = await request.form()
                request_body = dict(form_data)
            else:
                body_bytes = await request.body()
                request_body = {"raw": body_bytes.decode("utf-8", errors="ignore")}
    except Exception:
        request_body = None

    # 查找匹配的Mock接口
    mock_api = MockService.find_matching_mock(db, method, full_path)

    if not mock_api:
        # 没有找到匹配的Mock接口，记录日志并返回404
        response_time_ms = int((time.time() - start_time) * 1000)

        LogService.create_log(
            db=db,
            mock_api_id=None,
            request_method=method,
            request_path=full_path,
            request_headers=request_headers,
            request_body=request_body,
            request_params=request_params,
            response_status_code=404,
            response_headers={"Content-Type": "application/json"},
            response_body={
                "error": "Mock API not found",
                "path": full_path,
                "method": method,
            },
            response_time_ms=response_time_ms,
            client_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        return Response(
            content='{"error": "Mock API not found"}',
            status_code=404,
            headers={"Content-Type": "application/json"},
        )

    # 生成响应
    request_data = {
        "method": method,
        "path": full_path,
        "headers": request_headers,
        "params": request_params,
        "body": request_body,
    }

    try:
        response_body, response_headers = ResponseGenerator.generate_response(
            mock_api, request_data
        )
        status_code = mock_api.status_code

    except Exception as e:
        # 响应生成失败
        response_body = {
            "error": "Response generation failed",
            "message": str(e),
            "mock_id": mock_api.id,
        }
        response_headers = {"Content-Type": "application/json"}
        status_code = 500

    # 计算响应时间
    response_time_ms = int((time.time() - start_time) * 1000)

    # 记录请求日志
    LogService.create_log(
        db=db,
        mock_api_id=mock_api.id,
        request_method=method,
        request_path=full_path,
        request_headers=request_headers,
        request_body=request_body,
        request_params=request_params,
        response_status_code=status_code,
        response_headers=response_headers,
        response_body=response_body,
        response_time_ms=response_time_ms,
        client_ip=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    # 返回响应
    import json

    return Response(
        content=json.dumps(response_body, ensure_ascii=False, indent=2),
        status_code=status_code,
        headers=response_headers,
    )
