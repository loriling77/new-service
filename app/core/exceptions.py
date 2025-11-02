from typing import Any, Dict, Optional


class BaseAPIException(Exception):
    def __init__(self, status_code: int, code: int, message: str, detail: Optional[Any] = None):
        self.status_code = status_code
        self.detail: Dict[str, Any] = {
            "code": code,
            "message": message,
        }
        # 如果有详细信息，添加到响应中
        if detail is not None:
            self.detail["detail"] = detail


class ValidationException(BaseAPIException):
    def __init__(self, detail: Optional[Any] = None):
        """
        初始化验证异常

        Args:
            detail: 详细的验证错误信息（如字段名、错误原因等）
        """
        super().__init__(status_code=422, code=422, message="参数验证失败", detail=detail)
class NotFoundException(BaseAPIException):
    """
    资源不存在异常

    当请求的资源（如用户、分类等）不存在时抛出
    对应HTTP状态码404（Not Found）
    """

    def __init__(self, resource: str = "资源"):
        """
        初始化资源不存在异常

        Args:
            resource: 资源名称（如"用户"、"分类"、"请帖"等）
        """
        super().__init__(status_code=404, code=404, message=f"{resource}不存在")


class AlreadyExistsException(BaseAPIException):
    """
    资源已存在异常

    当尝试创建已存在的资源时抛出（如重复的用户名、分类名等）
    对应HTTP状态码409（Conflict）
    """

    def __init__(self, resource: str = "资源"):
        """
        初始化资源已存在异常

        Args:
            resource: 资源名称（如"用户名"、"分类名称"等）
        """
        super().__init__(status_code=409, code=409, message=f"{resource}已存在")

