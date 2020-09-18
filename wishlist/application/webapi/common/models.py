import operator
from datetime import datetime

import stringcase
from pydantic import BaseModel


class SerializableModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        ignore_extra = True

        alias_generator = stringcase.camelcase
        json_encoders = {
            datetime: operator.methodcaller('isoformat')
        }

    def dict(self, *args, **kwargs):
        kwargs = {
            **kwargs,
            'by_alias': True,
            'exclude_none': True
        }

        return super().dict(*args, **kwargs)


class Metadata(SerializableModel):
    page: int
    size: int
    count: int
