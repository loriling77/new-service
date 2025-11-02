from pydantic import BaseModel, Field


class TimeStampMixin(BaseModel):
    """
    时间戳字段混入类

    用于响应Schema，包含创建时间和更新时间字段
    可以混入到任何响应模型中
    """
    # 创建时间：可选字段，格式为ISO 8601字符串
    created_at: str | None = Field(None, description="创建时间")
    # 更新时间：可选字段，格式为ISO 8601字符串
    updated_at: str | None = Field(None, description="更新时间")


class PaginationParams(BaseModel):
    """
    分页参数基类

    用于查询请求，提供分页功能
    可以继承此类并添加其他查询参数
    """
    # 页码：从1开始，最小值为1
    page: int = Field(1, ge=1, description="页码")
    # 每页数量：最小
# 最大100（防止查询过多数据）
    page_size: int = Field(10, ge=1, le=100, description="每页数量")