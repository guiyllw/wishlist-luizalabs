import abc
from typing import Dict, List

from wishlist.domain.customer.models import Customer


class CreateCustomerAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def create(self, customer: Customer) -> Customer:
        pass  # pragma: no-cover


class UpdateCustomerAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, customer: Customer) -> bool:
        pass  # pragma: no-cover


class FindCustomerAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find_one(self, query: Dict) -> Customer:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Dict]):
        pass  # pragma: no-cover


class DeleteCustomerAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def delete(self, id_: str) -> str:
        pass  # pragma: no-cover
