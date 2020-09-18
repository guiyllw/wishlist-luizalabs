from typing import List, Optional

from wishlist.application.webapi.common.models import (
    Metadata,
    SerializableModel
)


class CreateProductRequest(SerializableModel):
    price: float
    brand: str
    title: str
    review_score: Optional[float] = None


class ProductResponse(SerializableModel):
    id: str
    price: float
    image: str
    brand: str
    title: str
    review_score: Optional[float] = None


class ProductListResponse(SerializableModel):
    meta: Metadata
    products: List[ProductResponse]
