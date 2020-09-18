from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    brand: Optional[str] = None
    title: Optional[str] = None
    review_score: Optional[float] = None
