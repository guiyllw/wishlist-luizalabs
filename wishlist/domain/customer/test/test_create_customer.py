import pytest

from wishlist.domain.customer.exceptions import CustomerAlreadyRegisteredError
from wishlist.domain.customer.ports import CreateCustomer
from wishlist.test.helpers import AsyncMock


class TestCreateCustomer:

    async def test_create_customer_with_success(
        self,
        customer_dict,
        customer
    ):
        del customer_dict['id']
        create_customer = CreateCustomer(
            AsyncMock(return_value=customer),
            AsyncMock()
        )

        customer = await create_customer.create(customer_dict)

        assert customer == customer

    async def test_create_customer_with_duplicated_email(
        self,
        customer_dict,
        customer
    ):
        create_customer = CreateCustomer(
            AsyncMock(),
            AsyncMock(return_value=customer)
        )

        with pytest.raises(CustomerAlreadyRegisteredError):
            await create_customer.create(customer_dict)
