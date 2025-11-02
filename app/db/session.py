from tortoise import Tortoise
import logging
from urllib.parse import quote_plus
from app.core.config import settings

logger = logging.getLogger("db")


def _build_mysql_url() -> str:
    user = settings.DB_USER
    password = settings.DB_PASSWORD
    host = settings.DB_HOST
    port = settings.DB_PORT
    db = settings.DB_NAME
    charset = settings.DB_CHARSET

    safe_user = quote_plus(user)
    safe_pwd = quote_plus(password)
    return f"mysql://{safe_user}:{safe_pwd}@{host}:{port}/{db}?charset={charset}"


async def init_db() -> None:
    dsn = _build_mysql_url()
    logger.info("DB init start: %s", dsn.replace(settings.DB_PASSWORD, "***"))

    try:
        # 初始化Tortoise ORM
        await Tortoise.init(
            db_url=dsn,  # 数据库连接URL
            modules={
                "models": [
                    "app.models.user",  # 注册用户模型
                    "app.models.invitation",  # 注册请帖相关模型（包括分类）
                ]
            }
        )

        # 自动生成数据库表结构
        # safe=True: 如果表已存在则跳过，不会删除已存在的表
        await Tortoise.generate_schemas(safe=True)
        logger.info("DB init success")

    except Exception as e:
        # 记录完整异常信息并重新抛出
        logger.exception("DB init failed: %s", e)
        raise

async def close_db() -> None:
    await Tortoise.close_connections()
