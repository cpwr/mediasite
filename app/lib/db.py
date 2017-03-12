import asyncpg

async def configure_db_client(loop, config):
    pool = await asyncpg.connect(
        config['dsn'],
        loop=loop,
        timeout=config['timeout'],
        command_timeout=config['timeout'],
    )
    return pool
