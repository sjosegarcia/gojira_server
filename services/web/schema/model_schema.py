import orjson
from pydantic import BaseModel
from pydantic.json import pydantic_encoder
from typing import Any, Callable
from uuid import UUID


def orjson_dumps(value: Any, *, default: Callable) -> str:
    return orjson.dumps(
        value, default=default, option=orjson.OPT_SERIALIZE_UUID
    ).decode()


class Model(BaseModel):
    class Config:
        """
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        allow_none = True
        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        json_dumps = orjson_dumps
        json_encoders = {UUID: lambda x: pydantic_encoder(x)}
        json_loads = orjson.loads
        orm_mode = True
        validate_all = True
        use_enum_values = False
        validate_assignment = True
        frozen = True
