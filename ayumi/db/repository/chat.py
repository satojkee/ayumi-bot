"""Contains `ChatRepo` class with database operations over `Chat` model."""


from typing import Any, Optional, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ayumi.db import provider
from ayumi.db.models import Chat


__all__ = ('ChatRepo',)


class ChatRepo:
    """Contains all required db operations over `Chat` model."""

    @classmethod
    @provider
    async def create(cls, session: AsyncSession, **kwargs: Any) -> None:
        """Use it to add a new `Chat` to the db.

        :param session: AsyncSession - db session
        :param kwargs: Any - Chat data
        :return: None
        """
        instance = await cls.get(session=session, **kwargs)
        if instance is None:
            session.add(Chat(**kwargs))
            await session.commit()

    @staticmethod
    @provider
    async def get(session: AsyncSession,
                  **kwargs: Any) -> Optional[Chat]:
        """Use it to get a `Chat` instance by its telegram id.

        :param session: AsyncSession - db session
        :param kwargs: Any - filters
        :return: Optional[Chat]
        """
        result = await session.execute(select(Chat).filter_by(**kwargs))

        return result.scalar()

    @staticmethod
    @provider
    async def get_all(session: AsyncSession,
                      **kwargs: Any) -> Iterable[Chat]:
        """Use it to get a list of `Chat` instances stored in the db.

        :param session: AsyncSession - db session
        :param kwargs: Any - filters
        :return: list[Chat] - a list of `Chat` instances
        """
        result = await session.execute(select(Chat).filter_by(**kwargs))

        return result.scalars().all()

    @classmethod
    @provider
    async def delete(cls, session: AsyncSession,
                     **kwargs: Any) -> None:
        """Use it to remove a `Chat` instance by its telegram id.

        :param session: AsyncSession - db session
        :param kwargs: Any - filters
        :return: None
        """
        instance = await cls.get(session=session, **kwargs)
        if instance:
            await session.delete(instance)
            await session.commit()

    @classmethod
    @provider
    async def update(cls, session: AsyncSession,
                     chat_id: str, **kwargs: Any) -> None:
        """Use it to update an already existing `Chat` instance.

        :param session: AsyncSession - db session
        :param chat_id: str - telegram chat as string
        :param kwargs: Any - Chat data
        :return: None
        """
        instance = await cls.get(session=session, chat_id=chat_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)

            await session.commit()
        else:
            # if the Chat doesn't exist, create a new one
            await cls.create(session=session, chat_id=chat_id, **kwargs)
