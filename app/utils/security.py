import bcrypt


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希加密

    Args:
        password: 明文密码

    Returns:
        str: 加密后的密码哈希值（字符串格式）
    """
    # bcrypt.hashpw：加密密码
    # password.encode("utf-8")：将字符串编码为字节
    # bcrypt.gensalt()：自动生成盐值
    # .decode("utf-8")：将字节解码回字符串
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确

    Args:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的加密密码哈希值

    Returns:
        bool: 如果密码正确返回True，否则返回False
    """
    try:
        # bcrypt.checkpw：验证密码
        # 会自动提取哈希值中的盐值进行比较
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),  # 编码明文密码
            hashed_password.encode("utf-8")  # 编码存储的哈希值
        )
    except Exception:
        # 如果出现任何错误（如格式错误），返回False
        return False
````

**app/core/dependencies.py:**

```python
"""
FastAPI依赖注入模块

提供认证和授权相关的依赖项（Dependency）
这些依赖项可以被路由处理器使用，实现权限控制

依赖项：
- get_current_user: 获取当前登录用户
- get_current_admin_user: 获取当前管理员用户（必须是admin角色）
- get_current_app_user: 获取当前App用户（必须是user角色）
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.models.user import User, UserRole

# HTTP Bearer认证方案
# 客户端需要在请求头中提供：Authorization: Bearer <token>
security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    获取当前登录用户

    从请求头中提取JWT令牌，验证并解析用户信息
    如果令牌无效或用户不存在，抛出401异常

    Args:
        credentials: HTTP Bearer认证凭证（包含令牌）

    Returns:
        User: 当前登录的用户对象

    Raises:
        HTTPException: 令牌无效或用户不存在时抛出401异常

    注意：
        开发环境支持dev-admin和dev-user便捷令牌，直接返回虚拟用户对象
        生产环境应移除此功能
    """
    # 从认证凭证中提取令牌
    token = credentials.credentials
    # 验证令牌并获取用户ID
    user_id = verify_token(token)

    if not user_id:
        # 令牌无效（过期、签名错误等）
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )

    # 【开发便捷账号】支持dev-admin和dev-user快速开发
    # 生产环境应移除此功能，只允许从数据库查询真实用户
    if user_id in ("dev-admin", "dev-user"):
        # 根据令牌确定角色
        role = UserRole.ADMIN if user_id == "dev-admin" else UserRole.USER
        # 返回一个内存用户对象（不必存在于数据库）
        user = User(
            username=user_id,
            email=f"{user_id}@example.com",
            hashed_password="",
            role=role
        )
        return user

    # 从数据库查询真实用户
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    return user


async def get_current_admin_user(
        user: User = Depends(get_current_user)
) -> User:
    """
    获取当前管理员用户

    依赖get_current_user，但额外检查用户角色必须是管理员
    只有管理员可以访问管理端接口

    Args:
        user: 当前登录用户（从get_current_user依赖获取）

    Returns:
        User: 当前管理员用户对象

    Raises:
        HTTPException: 如果用户不是管理员，抛出403权限不足异常
    """
    # 检查用户角色
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return user


async def get_current_app_user(
        user: User = Depends(get_current_user)
) -> User:
    """
    获取当前App用户

    依赖get_current_user，但额外检查用户角色必须是普通用户
    只有普通用户可以访问App端接口

    Args:
        user: 当前登录用户（从get_current_user依赖获取）

    Returns:
        User: 当前App用户对象

    Raises:
        HTTPException: 如果用户不是普通用户，抛出403权限不足异常
    """
    # 检查用户角色
    if user.role != UserRole.USER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return user