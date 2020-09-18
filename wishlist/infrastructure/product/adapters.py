from typing import Dict, List

from wishlist.domain.product.adapters import (
    CreateProductAdapter,
    DeleteProductAdapter,
    FindProductAdapter,
    UpdateProductAdapter
)
from wishlist.domain.product.models import Product
from wishlist.infrastructure.common.repositories import MongoRepository


class ProductAdapter(
    CreateProductAdapter,
    UpdateProductAdapter,
    DeleteProductAdapter,
    FindProductAdapter
):
    def __init__(self):
        self._repository = MongoRepository('product')

    async def create(self, product: Dict) -> Product:
        id_ = await self._repository.create(product)
        return Product(id=id_, **product)

    async def update(self, product: Dict) -> bool:
        return await self._repository.update(product['id'], product)

    async def find_one(self, query: Dict) -> Product:
        product = await self._repository.find_one(query)
        if not product:
            return None

        return Product(**product)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Product]):
        meta, products = await self._repository.find_all_and_count(
            query, page, size
        )

        return (meta, [Product(**p) for p in products])

    async def delete(self, id_: str) -> str:
        return await self._repository.delete(id_)
