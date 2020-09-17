from wishlist.domain.wishlist.ports import AddProducts
from wishlist.test.helpers import AsyncMock


class TestAddProducts:
    async def test_add_products_with_success(
        self,
        product_ids,
        wishlist_response
    ):
        add_products = AddProducts(
            AsyncMock(return_value=wishlist_response)
        )

        wishlist = await add_products.add_to_list(
            'fake-customer-id',
            product_ids
        )

        assert wishlist == wishlist_response
