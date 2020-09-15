import abc
from typing import Dict, List, Optional

from wishlist.domain.customer.adapters import (
    CreateCustomerAdapter,
    FindCustomerAdapter,
    UpdateCustomerAdapter
)
from wishlist.domain.customer.exceptions import CustomerAlreadyRegisteredError
from wishlist.domain.customer.models import Customer


class CreateCustomerPort(metaclass=abc.ABCMeta):
    async def create(self, create_customer_request: Dict) -> Customer:
        pass  # pragma: no-cover


class UpdateCustomerPort(metaclass=abc.ABCMeta):
    async def update(self, update_input) -> bool:
        pass  # pragma: no-cover


class FindCustomerPort(metaclass=abc.ABCMeta):
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

    async def check_email_exists(self, email: str) -> bool:
        pass  # pragma: no-cover


class DeleteCustomerPort(metaclass=abc.ABCMeta):
    async def delete(self, input) -> str:
        pass  # pragma: no-cover


class CreateCustomer(CreateCustomerPort):
    def __init__(
        self,
        create_customer_adapter: CreateCustomerAdapter,
        find_customer_adapter: FindCustomerAdapter
    ):
        self._create_customer_adapter = create_customer_adapter
        self._find_customer_adapter = find_customer_adapter

    async def create(self, create_customer_request) -> Customer:
        name = create_customer_request['name']
        email = create_customer_request['email']

        if await self._find_customer_adapter.check_email_exists(email):
            raise CustomerAlreadyRegisteredError()

        return await self._create_customer_adapter(
            Customer(
                name=name,
                email=email
            )
        )


class UpdateCustomer(UpdateCustomerPort):
    def __init__(
        self,
        update_customer_adapter: UpdateCustomerAdapter,
        find_customer_adapter: FindCustomerAdapter
    ):
        self._update_customer_adapter = update_customer_adapter
        self._find_customer_adapter = find_customer_adapter

    async def update(self, update_customer_request: Dict) -> bool:
        id_ = update_customer_request['id']
        name = update_customer_request['name']
        email = update_customer_request['email']

        if await self._find_customer_adapter.check_email_exists(email):
            raise CustomerAlreadyRegisteredError()

        return await self._update_customer_adapter(
            Customer(
                id_=id_,
                name=name,
                email=email
            )
        )


class FindCustomer(FindCustomerPort):
    def __init__(
        self,
        find_customer_adapter: FindCustomerAdapter
    ):
        self._find_customer_adapter = find_customer_adapter

    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> Customer:
        return await self._find_customer_adapter.find_one(
            query,
            projection
        )

    async def find_all(
        self,
        query: Dict,
        page: int,
        size: int,
        projection: Optional[List[str]] = None
    ) -> (Dict, List[Customer]):
        return await self._find_customer_adapter.find_all(
            query,
            page,
            size,
            projection
        )

    async def check_email_exists(self, email: str) -> bool:
        found_customer = await self.find_one({
            'email': email
        }, ['email'])

        return bool(found_customer)


class DeleteCustomer(DeleteCustomerPort):
    def __init__(
        self,
        delete_customer_adapter
    ):
        self._delete_customer_adapter = delete_customer_adapter

    async def delete(self, id_: str) -> str:
        return await self._delete_customer_adapter.delete(
            id_
        )
