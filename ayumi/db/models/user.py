from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from ._base import BaseModel
from ayumi.config import app_config

__all__ = ('User',)


class User(BaseModel):
    __tablename__ = 'ayumi_users'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[int] = mapped_column(unique=True)
    level: Mapped[int] = mapped_column(default=app_config.security.default)
    created: Mapped[date] = mapped_column(default=date.today)
