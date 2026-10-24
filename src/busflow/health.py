import asyncio
from typing import Any


async def check_postgres(connection_factory: Any) -> bool:
    try:
        connection = await asyncio.wait_for(connection_factory(), timeout=1.0)
        await connection.close()
        return True
    except Exception:
        return False


async def check_redis(redis_client: Any) -> bool:
    try:
        return bool(await asyncio.wait_for(redis_client.ping(), timeout=1.0))
    except Exception:
        return False
