import operator
from datetime import datetime

from pydantic import BaseModel


class SerializableModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        ignore_extra = True

        json_encoders = {
            datetime: operator.methodcaller('isoformat')
        }

    def dict(self, *args, **kwargs):
        kwargs = {
            **kwargs,
            'exclude_none': True
        }

        return super().dict(*args, **kwargs)


class Metadata(SerializableModel):
    page: int
    size: int
    count: int
