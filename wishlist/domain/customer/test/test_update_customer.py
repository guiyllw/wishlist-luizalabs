import pytest

from wishlist.domain.customer.exceptions import CustomerAlreadyRegisteredError
from wishlist.domain.customer.ports import UpdateCustomer
from wishlist.test.helpers import AsyncMock


class TestUpdateCustomer:

    async def test_update_customer_with_success(
        self,
        update_customer_request
    ):
        update_customer = UpdateCustomer(
            AsyncMock(return_value=True),
            AsyncMock()
        )

        updated = await update_customer.update(update_customer_request)

        assert updated is True

    async def test_update_customer_with_duplicated_email(
        self,
        update_customer_request,
        customer_response
    ):
        update_customer = UpdateCustomer(
            AsyncMock(),
            AsyncMock(return_value=customer_response)
        )

        with pytest.raises(CustomerAlreadyRegisteredError):
            await update_customer.update(update_customer_request)
