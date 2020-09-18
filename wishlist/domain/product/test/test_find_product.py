from wishlist.domain.product.ports import FindProduct
from wishlist.test.helpers import AsyncMock


class TestFindProduct:

    async def test_find_one_with_succeeded(
        self,
        product_response
    ):
        find_product = FindProduct(
            AsyncMock(return_value=product_response)
        )

        product = await find_product.find_one({
            'id': 'fake-id'
        })

        assert product == product_response

    async def test_find_all_with_succeeded(
        self,
        product_list_response
    ):
        find_product = FindProduct(
            AsyncMock(return_value=product_list_response)
        )

        meta, products = await find_product.find_all({
            'id': 'fake-id'
        }, 1, 10)

        assert meta == product_list_response[0]
        assert products == product_list_response[1]
