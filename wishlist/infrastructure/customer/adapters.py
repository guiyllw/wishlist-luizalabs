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

    async def create(self, customer: Dict) -> Customer:
        await self._repository.create(customer)
        return Customer(**customer)

    async def update(self, customer: Dict) -> bool:
        return await self._repository.update(customer['id'], customer)

    async def find_one(self, query: Dict) -> Customer:
        customer = await self._repository.find_one(query)
        if not customer:
            return None

        return Customer(**customer)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Customer]):
        meta, customers = await self._repository.find_all_and_count(
            query, page, size
        )

        return (meta, [Customer(**c) for c in customers])

    async def delete(self, id_: str) -> str:
        return await self._repository.delete(id_)
