import pytest

from wishlist.domain.customer.exceptions import CustomerNotFoundError
from wishlist.domain.wishlist.exceptions import NoValidProductsError
from wishlist.domain.wishlist.ports import AddProducts
from wishlist.test.helpers import AsyncMock


class TestAddProducts:
    async def test_add_products_to_new_wishlist_with_success(
        self,
        product_ids,
        wishlist_response,
        found_customer
    ):
        add_products = AddProducts(
            AsyncMock(return_value=wishlist_response),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(return_value=found_customer),
            AsyncMock(return_value=True)
        )

        wishlist = await add_products.add_to_list(
            'fake-customer-id',
            product_ids
        )

        assert wishlist == wishlist_response

    async def test_add_products_with_no_customer_raises(
        self,
        product_ids,
        wishlist_response
    ):
        add_products = AddProducts(
            AsyncMock(return_value=wishlist_response),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(return_value=True)
        )

        with pytest.raises(CustomerNotFoundError):
            await add_products.add_to_list(
                'fake-customer-id',
                product_ids
            )

    async def test_add_products_with_invalid_products_raises(
        self,
        wishlist_response,
        found_customer
    ):
        add_products = AddProducts(
            AsyncMock(return_value=wishlist_response),
            AsyncMock(),
            AsyncMock(),
            AsyncMock(return_value=found_customer),
            AsyncMock()
        )

        with pytest.raises(NoValidProductsError):
            await add_products.add_to_list(
                'fake-customer-id',
                []
            )

    async def test_add_products_with_existent_list_with_success(
        self,
        wishlist_response,
        found_customer,
        product_ids
    ):
        add_products = AddProducts(
            AsyncMock(),
            AsyncMock(return_value=wishlist_response),
            AsyncMock(return_value=True),
            AsyncMock(return_value=found_customer),
            AsyncMock(return_value=True)
        )

        wishlist = await add_products.add_to_list(
            'fake-customer-id',
            product_ids
        )

        assert wishlist == wishlist_response

    async def test_add_products_with_duplicated_product_ids_should_be_unique(
        self,
        wishlist_response,
        found_customer,
        product_ids
    ):
        add_products = AddProducts(
            AsyncMock(),
            AsyncMock(return_value=wishlist_response),
            AsyncMock(return_value=True),
            AsyncMock(return_value=found_customer),
            AsyncMock(return_value=True)
        )

        wishlist = await add_products.add_to_list(
            'fake-customer-id',
            product_ids
        )

        assert all(
            product_id in wishlist.product_ids
            for product_id in product_ids
        ) is True

        assert all(
            product_id in wishlist.product_ids
            for product_id in wishlist_response.product_ids
        ) is True

        assert all(
            wishlist.product_ids.count(product_id) == 1
            for product_id in wishlist.product_ids
        ) is True
