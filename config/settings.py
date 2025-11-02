import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""
    PROJECT_NAME: str = "请帖服务API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 数据库配置（MySQL）
    DB_USER: str = "root"
    DB_PASSWORD: str = "123456"
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "invitation"
    DB_CHARSET: str = "utf8mb4"
    DB_ECHO: bool = True

    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    # 上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env"
    )


settings = Settings()