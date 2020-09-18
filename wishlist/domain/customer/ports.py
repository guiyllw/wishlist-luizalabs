import abc
from typing import Dict, List
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
    @abc.abstractmethod
    async def create(self, customer: Dict) -> Customer:
        pass  # pragma: no-cover


class UpdateCustomerPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, customer: Dict) -> bool:
        pass  # pragma: no-cover


class FindCustomerPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find_one(self, query: Dict) -> Customer:
        pass  # pragma: no-cover

    @abc.abstractmethod
    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Customer]):
        pass  # pragma: no-cover

    async def find_by_id(self, id_: str) -> Customer:
        return await self.find_one({
            'id': id_
        })

    async def find_by_email(self, email: str) -> Customer:
        return await self.find_one({
            'email': email
        })


class DeleteCustomerPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def delete(self, id_: str) -> int:
        pass  # pragma: no-cover


class CreateCustomer(CreateCustomerPort):
    def __init__(
        self,
        create_customer_adapter: CreateCustomerAdapter,
        find_customer_port: FindCustomerPort
    ):
        self._create_customer_adapter = create_customer_adapter
        self._find_customer_port = find_customer_port

    async def create(self, customer: Dict) -> Customer:
        email = customer['email']

        email_exists = await self._find_customer_port.find_by_email(email)
        if email_exists:
            raise CustomerAlreadyRegisteredError()

        customer['id'] = str(uuid4())
        return await self._create_customer_adapter.create(customer)


class UpdateCustomer(UpdateCustomerPort):
    def __init__(
        self,
        update_customer_adapter: UpdateCustomerAdapter,
        find_customer_port: FindCustomerPort
    ):
        self._update_customer_adapter = update_customer_adapter
        self._find_customer_port = find_customer_port

    async def update(self, customer: Dict) -> bool:
        id_exists = await self._find_customer_port.find_by_id(customer['id'])
        if not id_exists:
            raise CustomerNotFoundError()

        email_already_registered = await self._email_already_registered(
            customer['id'],
            customer['email']
        )
        if email_already_registered:
            raise CustomerAlreadyRegisteredError()

        return await self._update_customer_adapter.update(customer)

    async def _email_already_registered(self, id_: str, email: str):
        registered_customer = await self._find_customer_port.find_by_email(
            email
        )

        if registered_customer and registered_customer.id != id_:
            return True

        return False


class FindCustomer(FindCustomerPort):
    def __init__(self, find_customer_adapter: FindCustomerAdapter):
        self._find_customer_adapter = find_customer_adapter

    async def find_one(self, query: Dict) -> Customer:
        return await self._find_customer_adapter.find_one(query)

    async def find_all(
        self, query: Dict, page: int, size: int
    ) -> (Dict, List[Customer]):
        return await self._find_customer_adapter.find_all(query, page, size)


class DeleteCustomer(DeleteCustomerPort):
    def __init__(self, delete_customer_adapter: DeleteCustomerAdapter):
        self._delete_customer_adapter = delete_customer_adapter

    async def delete(self, id_: str) -> int:
        return await self._delete_customer_adapter.delete(id_)
