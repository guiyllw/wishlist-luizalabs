import operator
from datetime import datetime

import stringcase
from pydantic import BaseModel


class SerializableModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        ignore_extra = True
        skip_optional = True

        alias_generator = stringcase.camelcase
        json_encoders = {
            datetime: operator.methodcaller('isoformat')
        }


class Metadata(SerializableModel):
    page: int
    size: int
    count: int
