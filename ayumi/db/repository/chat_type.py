"""Contains `ChatTypeRepo` class with database operations over
    `ChatType` model.
"""


from dataclasses import asdict
from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ayumi.config import ChatTypes
from ayumi.db import provider
from ayumi.db.models import ChatType


__all__ = ('ChatTypeRepo',)


class ChatTypeRepo:
    """Contains all required db operation over `ChatType` model."""
    @staticmethod
    @provider
    async def create(session: AsyncSession) -> None:
        """Use this method to create necessary ChatType's
            from the `app_config.toml` file.

        :param session: AsyncSession - db session
        :return: None
        """
        for _, chat_type in asdict(ChatTypes()).items():
            session.add(ChatType(name=chat_type))

        await session.commit()

    @staticmethod
    @provider
    async def get(session: AsyncSession, **kwargs: Any) -> Optional[ChatType]:
        """Use it to get a `ChatType` instance by its name.

        :param session: AsyncSession - db session
        :param kwargs: Any - filters
        :return: Optional[ChatType]
        """
        result = await session.execute(select(ChatType).filter_by(**kwargs))

        return result.scalar()
