from wishlist.domain.customer.ports import FindCustomer
from wishlist.test.helpers import AsyncMock


class TestFindCustomer:

    async def test_find_one_with_succeeded(
        self,
        customer_dict,
        customer
    ):
        find_customer = FindCustomer(
            AsyncMock(return_value=customer_dict)
        )

        found_customer = await find_customer.find_one({
            'id': 'fake-id'
        })

        assert found_customer == customer

    async def test_find_all_with_succeeded(
        self,
        customer_list_response
    ):
        find_customer = FindCustomer(
            AsyncMock(return_value=customer_list_response)
        )

        meta, customers = await find_customer.find_all({
            'id': 'fake-id'
        }, 1, 10)

        assert meta == customer_list_response[0]
        assert customers == customer_list_response[1]
