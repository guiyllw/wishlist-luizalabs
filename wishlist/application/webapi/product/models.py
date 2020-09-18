from typing import List, Optional

from wishlist import settings
from wishlist.application.webapi.common.models import (
    Metadata,
    SerializableModel
)


class FullProduct(SerializableModel):
    id: str
    price: float
    brand: str
    image: Optional[str] = None
    title: str
    review_score: Optional[float] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = f'{settings.APP_HOST}/images/{self.id}.jpg'


class CreateProductRequest(SerializableModel):
    price: float
    brand: str
    title: str
    review_score: Optional[float] = None


class ProductListResponse(SerializableModel):
    meta: Metadata
    products: List[FullProduct]
