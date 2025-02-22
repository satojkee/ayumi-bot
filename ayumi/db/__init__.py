"""Contains database related stuff."""


from typing import Any, Callable

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)

from ayumi.config import DATABASE_URI, app_config


__all__ = ('provider', 'init_tables')


# Engine is always used to create session (`AsyncSession` instances)
engine = create_async_engine(url=DATABASE_URI, **app_config.sqlalchemy)
# Automatically create sessions with the same params
SessionFactory = async_sessionmaker(bind=engine)


def provider(func: Callable) -> Any:
    """Use it as decorator for db transactions.
    Automatically injects a `Session` instance into the decorated func.

    :param func: Callable
    :return: Any
    """
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        if kwargs.get('session') is None:
            async with SessionFactory() as session:
                try:
                    return await func(session=session, *args, **kwargs)
                except Exception as e:
                    await session.rollback()

                    raise e
        else:
            return await func(*args, **kwargs)

    return wrapper


def init_tables(drop: bool = False) -> None:
    """Use it to re/create required schemas in the db.

    :param drop: bool - drop attached tables if set to `True`
    :return: None
    """
    import asyncio

    async def _create_necessary() -> None:
        from ayumi.db.repository import ChatTypeRepo
        # fill `ayumi_chat_types` table with telegram API supported types
        await ChatTypeRepo.create()

    async def _init_tables() -> None:
        from ayumi.db.models import BaseModel

        try:
            async with engine.begin() as conn:
                if drop:
                    await conn.run_sync(BaseModel.metadata.drop_all)
                await conn.run_sync(BaseModel.metadata.create_all)

            await engine.dispose()

        except Exception as e:
            import sys
            import logging

            logging.getLogger(__name__).error('connection error: %s', e)

            sys.exit(-1)

    asyncio.run(_init_tables())
    # fill tables with necessary data
    if drop:
        asyncio.run(_create_necessary())
