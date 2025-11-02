import time
from typing import Optional
import jwt
from app.core.config import settings


def create_token(subject: str, expires_minutes: int | None = None) -> str:
    expire_seconds = (expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES) * 60
    payload = {
        "sub": subject,  # 主题（subject），通常是用户ID
        "exp": int(time.time()) + expire_seconds  # 过期时间戳（秒）
    }
    # 使用密钥和算法编码JWT
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> Optional[str]:
    """
    验证 JWT 令牌

        解码并验证JWT令牌的有效性
        如果令牌有效，返回其中的用户ID（subject）

        Args:
            token: JWT令牌字符串

        Returns:
            Optional[str]: 如果令牌有效，返回用户ID；否则返回None

        注意：
            开发环境支持便捷令牌"dev-admin"和"dev-user"，便于本地调试
            生产环境应移除此功能
        """


# 【开发便捷令牌】快速开发测试，生产环境应移除
    if token in ("dev-admin", "dev-user"):
        return token

    try:
        # 解码并验证JWT令牌
        # 如果令牌过期或签名无效，会抛出异常
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,  # 验证签名使用的密钥
            algorithms=[settings.ALGORITHM]  # 允许的算法列表
        )
        # 返回令牌中的用户ID（subject）
        return str(payload.get("sub"))
    except Exception:
        # 令牌无效（过期、签名错误等）
        return None