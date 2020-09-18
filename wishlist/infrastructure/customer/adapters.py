from typing import Dict, List

from wishlist.domain.customer.adapters import (
    CreateCustomerAdapter,
    DeleteCustomerAdapter,
    FindCustomerAdapter,
    UpdateCustomerAdapter
)
from wishlist.domain.customer.models import Customer
from wishlist.infrastructure.common.repositories import MongoRepository


class CustomerAdapter(
    CreateCustomerAdapter,
    UpdateCustomerAdapter,
    DeleteCustomerAdapter,
    FindCustomerAdapter
):
    def __init__(self):
        self._repository = MongoRepository('customer')

    async def create(self, customer: Customer) -> Customer:
        customer.id = await self._repository.create(customer.dict())
        return customer

    async def update(self, customer: Customer) -> bool:
        return await self._repository.update(customer.id, customer.dict())

    async def find_one(self, query: Dict) -> Customer:
        return await self._repository.find_one(query)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Customer]):
        return await self._repository.find_all_and_count(query, page, size)

    async def delete(self, id_: str) -> str:
        return await self._repository.delete(id_)
