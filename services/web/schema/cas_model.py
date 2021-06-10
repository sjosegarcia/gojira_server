from pydantic.main import BaseModel
from typing import Optional


class CasModel(BaseModel):
    ok: bool
    description: Optional[str]
    result: Optional[dict]

    class Config:
        """
        https://pydantic-docs.helpmanual.io/usage/model_config/
        """

        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        orm_mode = False
        validate_all = True
        use_enum_values = False
        validate_assignment = False
