from typing import Any

from sqlalchemy.ext.declarative import declared_attr, as_declarative


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()
