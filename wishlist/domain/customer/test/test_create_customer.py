import pytest

from wishlist.domain.customer.exceptions import CustomerAlreadyRegisteredError
from wishlist.domain.customer.ports import CreateCustomer
from wishlist.test.helpers import AsyncMock


class TestCreateCustomer:

    async def test_create_customer_with_success(
        self,
        create_customer_request,
        customer_response
    ):
        create_customer = CreateCustomer(
            AsyncMock(return_value=customer_response),
            AsyncMock()
        )

        customer = await create_customer.create(create_customer_request)

        assert customer == customer_response

    async def test_create_customer_with_duplicated_email(
        self,
        create_customer_request,
        customer_response
    ):
        create_customer = CreateCustomer(
            AsyncMock(),
            AsyncMock(return_value=customer_response)
        )

        with pytest.raises(CustomerAlreadyRegisteredError):
            await create_customer.create(create_customer_request)
