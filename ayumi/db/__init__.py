from typing import Any, Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ayumi.config import DATABASE_URI, app_config


__all__ = ('provider', 'init_schemas')


# Engine is always used to create session (`Session` instances)
engine = create_engine(url=DATABASE_URI, **app_config.sqlalchemy)
# Automatically create sessions with the same params
SessionFactory = sessionmaker(bind=engine)


def provider(func: Callable) -> Any:
    """Use it as decorator for db transactions.
    Automatically injects a `Session` instance into the decorated func.

    :param func: Callable
    :return: Any
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if kwargs.get('session') is None:
            with SessionFactory() as session:
                try:
                    return func(session=session, *args, **kwargs)
                except Exception as e:
                    session.rollback()

                    raise e
        else:
            return func(*args, **kwargs)

    return wrapper


def init_schemas() -> None:
    """Use it to re/create required schemas in the db."""
    from ayumi.db.models import BaseModel

    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)
