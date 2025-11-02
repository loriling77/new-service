from typing import Any, Dict, List, Optional


def success_response(data: Any, message: str = "成功") -> Dict[str, Any]:
    return {
        "code": 0,  # 0表示成功
        "message": message,
        "data": data
    }

def created_response(data: Any, message: str = "创建成功") -> Dict[str, Any]:
    return {
        "code": 0,
        "message": message,
        "data": data
    }

def pagination_response(
    items: List[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "成功",
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    total_pages = (total + page_size - 1) // page_size

    payload: Dict[str, Any] = {
        "code": 0,
        "message": message,
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
    }

    if extra:
        payload["data"].update(extra)

    return payload