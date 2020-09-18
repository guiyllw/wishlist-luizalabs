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

    async def create(self, product: Product) -> Product:
        product.id = await self._repository.create(product.dict())
        return product

    async def update(self, product: Product) -> bool:
        return await self._repository.update(product.id, product.dict())

    async def find_one(self, query: Dict) -> Product:
        return await self._repository.find_one(query)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Product]):
        return await self._repository.find_all_and_count(query, page, size)

    async def delete(self, id_: str) -> str:
        return await self._repository.delete(id_)
