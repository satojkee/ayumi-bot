"""This module contains `Chat` model."""


from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import BaseModel


__all__ = ('Chat',)


class Chat(BaseModel):
    """Represents a chat.

    Attr:
        id - primary key
        chat_id - telegram id
        level - access level
        created - creation date
        chat_type_id - chat type id (foreign key)
    """
    __tablename__ = 'ayumi_chats'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[str] = mapped_column(unique=True)
    chat_type_id: Mapped[int] = mapped_column(
        ForeignKey('ayumi_chat_types.id')
    )
    title: Mapped[Optional[str]] = mapped_column()
    level: Mapped[int] = mapped_column()
    created: Mapped[date] = mapped_column(default=date.today)

    chat_type: Mapped['ChatType'] = relationship(back_populates='chats')
