from .constants import POSTGRES, SQLITE


async def Connexer(dsn: str):
    vendor, _, remainder = dsn.partition('://')
    if vendor == POSTGRES:
        from asyncpg import connect
        return vendor, await connect(dsn=dsn)
    elif vendor == SQLITE:
        from aiosqlite import connect
        return vendor, await connect(remainder)
