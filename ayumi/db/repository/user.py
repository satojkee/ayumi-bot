from typing import Any, Optional
from sqlalchemy.orm import Session

from ayumi.db import provider
from ayumi.db.models import User


__all__ = ('UserRepo',)


class UserRepo:
    @classmethod
    @provider
    async def create(cls, session: Session, **kwargs: Any) -> None:
        """Use it to add a new `User` to the db.

        :param session: Session - db session
        :param kwargs: Any - user data
        :return: None
        """
        instance = await cls.get(session=session, uuid=kwargs['uuid'])
        if instance is None:
            session.add(User(**kwargs))
            session.commit()

    @staticmethod
    @provider
    async def get(session: Session, uuid: int) -> Optional[User]:
        """Use it to get a `User` instance by its telegram id.

        :param session: Session - db session
        :param uuid: int - user's uuid
        :return: Optional[User]
        """
        return session.query(User).filter_by(uuid=uuid).first()

    @staticmethod
    @provider
    async def get_all(session: Session) -> list[User]:
        """Use it to get a list of `User` instances stored in the db.

        :param session: Session - db session
        :return: list[User] - a list of `User` instances
        """
        # noinspection PyTypeChecker
        return session.query(User).all()

    @classmethod
    @provider
    async def delete(cls, session: Session, uuid: int) -> None:
        """Use it to remove a `User` instance by its telegram id.

        :param session: Session - db session
        :param uuid: int - user's uuid
        :return: None
        """
        instance = await cls.get(session=session, uuid=uuid)
        if instance:
            session.delete(instance)
            session.commit()
