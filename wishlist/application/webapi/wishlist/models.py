from typing import List

from wishlist.application.webapi.common.models import SerializableModel
from wishlist.application.webapi.product.models import ProductResponse


class AddProductsRequest(SerializableModel):
    customer_id: str
    product_ids: List[str]


class CustomerWishListResponse(SerializableModel):
    id: str
    customer_id: str
    products: List[ProductResponse]
