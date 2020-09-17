import abc
from typing import Dict, List, Optional

from wishlist.domain.product.models import Product


class CreateProductAdapter(metaclass=abc.ABCMeta):
    async def create(self, product: Product) -> Product:
        pass  # pragma: no-cover


class UpdateProductAdapter(metaclass=abc.ABCMeta):
    async def update(self, product: Product) -> bool:
        pass  # pragma: no-cover


class FindProductAdapter(metaclass=abc.ABCMeta):
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


class DeleteProductAdapter(metaclass=abc.ABCMeta):
    async def delete(self, id_: str) -> str:
        pass  # pragma: no-cover
