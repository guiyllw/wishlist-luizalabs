from unittest.mock import patch

import pytest

from wishlist.domain.customer.exceptions import (
    CustomerAlreadyRegisteredError,
    CustomerNotFoundError
)
from wishlist.domain.customer.ports import UpdateCustomer
from wishlist.test.helpers import AsyncMock


class TestUpdateCustomer:

    async def test_update_customer_with_success(
        self,
        customer_dict,
        customer
    ):
        update_customer = UpdateCustomer(
            AsyncMock(return_value=True),
            AsyncMock(return_value=customer)
        )

        updated = await update_customer.update(customer_dict)

        assert updated is True

    async def test_update_customer_not_exists(
        self,
        customer_dict
    ):
        update_customer = UpdateCustomer(
            AsyncMock(),
            AsyncMock()
        )

        with pytest.raises(CustomerNotFoundError):
            await update_customer.update(customer_dict)

    async def test_update_customer_duplicated_email(
        self,
        customer_dict,
        customer
    ):
        update_customer = UpdateCustomer(
            AsyncMock(),
            AsyncMock(return_value=customer)
        )

        with patch.object(
            UpdateCustomer, '_email_already_registered', return_value=True
        ):
            with pytest.raises(CustomerAlreadyRegisteredError):
                await update_customer.update(customer_dict)
