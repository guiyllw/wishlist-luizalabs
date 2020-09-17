from wishlist.domain.customer.ports import FindCustomer
from wishlist.test.helpers import AsyncMock


class TestFindCustomer:

    async def test_find_one_with_all_fields_succeeded(
        self,
        customer_response
    ):
        find_customer = FindCustomer(
            AsyncMock(return_value=customer_response)
        )

        customer = await find_customer.find_one({
            'id': 'fake-id'
        })

        assert customer == customer_response

    async def test_find_one_with_projected_field_succeeded(
        self,
        create_customer_request,
        customer_response_email_projected
    ):
        find_customer = FindCustomer(
            AsyncMock(return_value=customer_response_email_projected)
        )

        customer = await find_customer.find_one({
            'id': 'fake-id'
        })

        assert customer.email == create_customer_request['email']
        assert customer.name is None
        assert customer.id is None

    async def test_find_all_with_all_fields_succeeded(
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

    async def test_find_all_with_projected_field_succeeded(
        self,
        create_customer_request,
        customer_list_response_email_projected
    ):
        find_customer = FindCustomer(
            AsyncMock(return_value=customer_list_response_email_projected)
        )

        meta, customers = await find_customer.find_all({
            'id': 'fake-id'
        }, 1, 10, ['email'])

        assert meta == customer_list_response_email_projected[0]

        assert customers[0].email == create_customer_request['email']
        assert customers[0].name is None
        assert customers[0].id is None
