"""
应用配置管理
"""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    APP_NAME: str = "Mocker API Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = (
        "mysql+pymysql://root:qwer4321@localhost:3306/mocker"  # MySQL数据库
    )
    DATABASE_ECHO: bool = False

    # API配置
    API_V1_STR: str = "/api/v1"

    # CORS配置
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
    ]

    # Mock服务配置
    MOCK_PREFIX: str = "/mock"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()
