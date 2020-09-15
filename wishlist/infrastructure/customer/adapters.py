from wishlist.domain.customer.adapters import (
    CreateCustomerAdapter,
    DeleteCustomerAdapter,
    UpdateCustomerAdapter
)
from wishlist.infrastructure.common.metaclasses import SingletonMeta


class SqlAdapter(
    CreateCustomerAdapter,
    UpdateCustomerAdapter,
    DeleteCustomerAdapter,
    UpdateCustomerAdapter,
    metaclass=SingletonMeta
):
    def __init__(self):
        pass

    async def create(self, create_input):
        pass

    async def update(self, update_input):
        pass

    async def find_one(self, find_one_input):
        pass

    async def find_all(self, find_all_input):
        pass

    async def delete(self, input):
        pass
