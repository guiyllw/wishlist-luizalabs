from typing import Optional

from pydantic import BaseModel


class Customer(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
