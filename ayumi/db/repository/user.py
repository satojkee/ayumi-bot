from typing import Any, Optional, Iterable, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ayumi.db import provider
from ayumi.db.models import User


__all__ = ('UserRepo',)


class UserRepo:
    @classmethod
    @provider
    async def create(cls, session: AsyncSession, **kwargs: Any) -> None:
        """Use it to add a new `User` to the db.

        :param session: AsyncSession - db session
        :param kwargs: Any - user data
        :return: None
        """
        instance = await cls.get(session=session, uuid=kwargs['uuid'])
        if instance is None:
            session.add(User(**kwargs))
            await session.commit()

    @staticmethod
    @provider
    async def get(session: AsyncSession,
                  uuid: Union[int, str]) -> Optional[User]:
        """Use it to get a `User` instance by its telegram id.

        :param session: AsyncSession - db session
        :param uuid: Union[int, str] - user's uuid
        :return: Optional[User]
        """
        result = await session.execute(select(User).filter_by(uuid=uuid))

        return result.scalar()

    @staticmethod
    @provider
    async def get_all(session: AsyncSession) -> Iterable[User]:
        """Use it to get a list of `User` instances stored in the db.

        :param session: AsyncSession - db session
        :return: list[User] - a list of `User` instances
        """
        result = await session.execute(select(User))

        return result.scalars().all()

    @classmethod
    @provider
    async def delete(cls, session: AsyncSession,
                     uuid: Union[int, str]) -> None:
        """Use it to remove a `User` instance by its telegram id.

        :param session: AsyncSession - db session
        :param uuid: Union[int, str] - user's uuid
        :return: None
        """
        instance = await cls.get(session=session, uuid=uuid)
        if instance:
            await session.delete(instance)
            await session.commit()
