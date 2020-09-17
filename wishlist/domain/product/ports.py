import abc
from typing import Dict, List, Optional
from uuid import uuid4

from wishlist.domain.product.adapters import (
    CreateProductAdapter,
    DeleteProductAdapter,
    FindProductAdapter,
    UpdateProductAdapter
)
from wishlist.domain.product.models import Product


class CreateProductPort(metaclass=abc.ABCMeta):
    async def create(self, create_product_request: Dict) -> Product:
        pass  # pragma: no-cover


class UpdateProductPort(metaclass=abc.ABCMeta):
    async def update(self, product: Product) -> bool:
        pass  # pragma: no-cover


class FindProductPort(metaclass=abc.ABCMeta):
    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> Product:
        pass  # pragma: no-cover

    async def find_all(
        self,
        query: Dict,
        page: int,
        size: int,
        projection: Optional[List[str]] = None
    ) -> (Dict, List[Product]):
        pass  # pragma: no-cover

    async def find_by_id(
        self,
        id: str,
        projection: Optional[List[str]] = None
    ) -> Product:
        return await self.find_one({
            'id': id
        }, projection)

    async def idexists(self, id: str) -> bool:
        registered_product = await self.find_by_id(id, ['id'])
        return bool(registered_product)


class DeleteProductPort(metaclass=abc.ABCMeta):
    async def delete(self, input) -> str:
        pass  # pragma: no-cover


class CreateProduct(CreateProductPort):
    def __init__(
        self,
        create_product_adapter: CreateProductAdapter
    ):
        self._create_product_adapter = create_product_adapter

    async def create(self, create_product_request) -> Product:
        price = create_product_request['price']
        brand = create_product_request['brand']
        title = create_product_request['title']
        review_score = create_product_request.get('review_score')

        return await self._create_product_adapter(
            Product(
                id=str(uuid4()),
                price=price,
                brand=brand,
                title=title,
                review_score=review_score
            )
        )


class UpdateProduct(UpdateProductPort):
    def __init__(
        self,
        update_product_adapter: UpdateProductAdapter
    ):
        self._update_product_adapter = update_product_adapter

    async def update(self, product: Product) -> bool:
        return await self._update_product_adapter(product)


class FindProduct(FindProductPort):
    def __init__(
        self,
        find_product_adapter: FindProductAdapter
    ):
        self._find_product_adapter = find_product_adapter

    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> Product:
        return await self._find_product_adapter.find_one(
            query,
            projection
        )

    async def find_all(
        self,
        query: Dict,
        page: int,
        size: int,
        projection: Optional[List[str]] = None
    ) -> (Dict, List[Product]):
        return await self._find_product_adapter.find_all(
            query,
            page,
            size,
            projection
        )

    async def check_email_exists(self, email: str) -> bool:
        found_product = await self.find_one({
            'email': email
        }, ['email'])

        return bool(found_product)


class DeleteProduct(DeleteProductPort):
    def __init__(
        self,
        delete_product_adapter: DeleteProductAdapter
    ):
        self._delete_product_adapter = delete_product_adapter

    async def delete(self, id: str) -> str:
        return await self._delete_product_adapter.delete(
            id
        )
