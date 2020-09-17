import abc
from typing import Dict, List, Optional

from wishlist.domain.customer.models import Customer


class CreateCustomerAdapter(metaclass=abc.ABCMeta):
    async def create(self, customer: Customer) -> Customer:
        pass  # pragma: no-cover


class UpdateCustomerAdapter(metaclass=abc.ABCMeta):
    async def update(self, customer: Customer) -> bool:
        pass  # pragma: no-cover


class FindCustomerAdapter(metaclass=abc.ABCMeta):
    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> Customer:
        pass  # pragma: no-cover

    async def find_all(
        self,
        query: Dict,
        page: int,
        size: int,
        projection: Optional[List[str]] = None
    ) -> (Dict, List[Customer]):
        pass  # pragma: no-cover


class DeleteCustomerAdapter(metaclass=abc.ABCMeta):
    async def delete(self, id: str) -> str:
        pass  # pragma: no-cover
