from typing import Any

from sqlalchemy.ext.declarative import declared_attr, as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
