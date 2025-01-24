"""This module contains `User` model."""


from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from ._base import BaseModel


__all__ = ('User',)


class User(BaseModel):
    """Represents a user.

    Attr:
        id - primary key
        uuid - user's telegram id
        level - user's access level
        created - creation date
    """
    __tablename__ = 'ayumi_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[int] = mapped_column(unique=True)
    level: Mapped[int] = mapped_column()
    created: Mapped[date] = mapped_column(default=date.today)
