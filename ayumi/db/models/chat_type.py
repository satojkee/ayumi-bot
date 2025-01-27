"""This module contains `ChatType` model."""


from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import BaseModel


__all__ = ('ChatType',)


class ChatType(BaseModel):
    """Represents a chat type.

    Attr:
        id - primary key
        name - type name
    """
    __tablename__ = 'ayumi_chat_types'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    chats: Mapped[list['Chat']] = relationship(back_populates='chat_type')
