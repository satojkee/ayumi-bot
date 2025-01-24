"""This module contains `BaseModel`, which is a base class for all models."""


from sqlalchemy.orm import DeclarativeBase


__all__ = ('BaseModel',)


class BaseModel(DeclarativeBase):
    """Base class for all database models."""
