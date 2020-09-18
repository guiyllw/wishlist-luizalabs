from wishlist.domain.customer.ports import DeleteCustomer
from wishlist.test.helpers import AsyncMock


class TestDeleteCustomer:

    async def test_delete_customer_with_success(self):
        delete_customer = DeleteCustomer(
            AsyncMock(return_value=1)
        )

        n_deleted = await delete_customer.delete('fake-id')

        assert n_deleted == 1

    async def test_delete_customer_that_not_exists(self):
        delete_customer = DeleteCustomer(
            AsyncMock(return_value=0)
        )

        n_deleted = await delete_customer.delete('fake-id')

        assert n_deleted == 0
