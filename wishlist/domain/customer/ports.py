import abc
from typing import Dict, List, Optional
from uuid import uuid4

from wishlist.domain.customer.adapters import (
    CreateCustomerAdapter,
    DeleteCustomerAdapter,
    FindCustomerAdapter,
    UpdateCustomerAdapter
)
from wishlist.domain.customer.exceptions import (
    CustomerAlreadyRegisteredError,
    CustomerNotFoundError
)
from wishlist.domain.customer.models import Customer


class CreateCustomerPort(metaclass=abc.ABCMeta):
    async def create(self, create_customer_request: Dict) -> Customer:
        pass  # pragma: no-cover


class UpdateCustomerPort(metaclass=abc.ABCMeta):
    async def update(self, customer: Customer) -> bool:
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

    async def find_by_id(
        self,
        id: str,
        projection: Optional[List[str]] = None
    ) -> Customer:
        return await self.find_one({
            'id': id
        }, projection)

    async def find_by_email(
        self,
        email: str,
        projection: Optional[List[str]] = None
    ) -> Customer:
        return await self.find_one({
            'email': email
        }, projection)

    async def idexists(self, id: str) -> bool:
        registered_customer = await self.find_by_id(id, ['id'])
        return bool(registered_customer)


class DeleteCustomerPort(metaclass=abc.ABCMeta):
    async def delete(self, input) -> str:
        pass  # pragma: no-cover


class CreateCustomer(CreateCustomerPort):
    def __init__(
        self,
        create_customer_adapter: CreateCustomerAdapter,
        find_customer_port: FindCustomerPort
    ):
        self._create_customer_adapter = create_customer_adapter
        self._find_customer_port = find_customer_port

    async def create(self, create_customer_request) -> Customer:
        name = create_customer_request['name']
        email = create_customer_request['email']

        email_exists = await self._find_customer_port.email_exists(email)
        if email_exists:
            raise CustomerAlreadyRegisteredError()

        return await self._create_customer_adapter(
            Customer(
                id=str(uuid4()),
                name=name,
                email=email
            )
        )


class UpdateCustomer(UpdateCustomerPort):
    def __init__(
        self,
        update_customer_adapter: UpdateCustomerAdapter,
        find_customer_port: FindCustomerAdapter
    ):
        self._update_customer_adapter = update_customer_adapter
        self._find_customer_port = find_customer_port

    async def update(self, customer: Customer) -> bool:
        idexists = await self._find_customer_port.idexists(customer.id)
        if not idexists:
            raise CustomerNotFoundError()

        email_already_registered = await self._email_already_registered(
            customer.id,
            customer.email
        )

        if email_already_registered:
            raise CustomerAlreadyRegisteredError()

        return await self._update_customer_adapter(customer)

    async def _email_already_registered(
        self,
        id: str,
        email: str
    ):
        registered_customer = await self._find_customer_port.find_by_email(
            email,
            ['id']
        )

        if registered_customer.id != id:
            return True

        return False


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


class DeleteCustomer(DeleteCustomerPort):
    def __init__(
        self,
        delete_customer_adapter: DeleteCustomerAdapter
    ):
        self._delete_customer_adapter = delete_customer_adapter

    async def delete(self, id: str) -> str:
        return await self._delete_customer_adapter.delete(
            id
        )
