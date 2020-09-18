import abc
from typing import Dict, List
from uuid import uuid4

from wishlist.domain.product.adapters import (
    CreateProductAdapter,
    DeleteProductAdapter,
    FindProductAdapter,
    UpdateProductAdapter
)
from wishlist.domain.product.models import Product


class CreateProductPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create(self, product: Dict) -> Product:
        pass  # pragma: no-cover


class UpdateProductPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, product: Dict) -> bool:
        pass  # pragma: no-cover


class FindProductPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find_one(self, query: Dict) -> Product:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Product]):
        pass  # pragma: no-cover

    async def find_by_id(self, id_: str) -> Product:
        return await self.find_one({
            'id': id_
        })


class DeleteProductPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def delete(self, id_: str) -> int:
        pass  # pragma: no-cover


class CreateProduct(CreateProductPort):
    def __init__(self, create_product_adapter: CreateProductAdapter):
        self._create_product_adapter = create_product_adapter

    async def create(self, product: Dict) -> Product:
        return await self._create_product_adapter.create(
            Product(id=str(uuid4()), **product)
        )


class UpdateProduct(UpdateProductPort):
    def __init__(
        self,
        update_product_adapter: UpdateProductAdapter
    ):
        self._update_product_adapter = update_product_adapter

    async def update(self, product: Dict) -> bool:
        return await self._update_product_adapter.update(product)


class FindProduct(FindProductPort):
    def __init__(self, find_product_adapter: FindProductAdapter):
        self._find_product_adapter = find_product_adapter

    async def find_one(self, query: Dict) -> Product:
        return await self._find_product_adapter.find_one(query)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Product]):
        return await self._find_product_adapter.find_all(query, page, size)


class DeleteProduct(DeleteProductPort):
    def __init__(self, delete_product_adapter: DeleteProductAdapter):
        self._delete_product_adapter = delete_product_adapter

    async def delete(self, id_: str) -> int:
        return await self._delete_product_adapter.delete(id_)
