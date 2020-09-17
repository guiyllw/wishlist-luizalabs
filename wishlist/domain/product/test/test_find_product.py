from wishlist.domain.product.ports import FindProduct
from wishlist.test.helpers import AsyncMock


class TestFindProduct:

    async def test_find_one_with_all_fields_succeeded(
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

    async def test_find_one_with_projected_field_succeeded(
        self,
        create_product_request,
        product_response_price_projected
    ):
        find_product = FindProduct(
            AsyncMock(return_value=product_response_price_projected)
        )

        product = await find_product.find_one({
            'id': 'fake-id'
        })

        assert product.price == create_product_request['price']
        assert product.id is None
        assert product.image is None
        assert product.brand is None
        assert product.title is None
        assert product.review_score is None

    async def test_find_all_with_all_fields_succeeded(
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

    async def test_find_all_with_projected_field_succeeded(
        self,
        create_product_request,
        product_list_response_price_projected
    ):
        find_product = FindProduct(
            AsyncMock(return_value=product_list_response_price_projected)
        )

        meta, products = await find_product.find_all({
            'id': 'fake-id'
        }, 1, 10, ['price'])

        assert meta == product_list_response_price_projected[0]

        assert products[0].price == create_product_request['price']
        assert products[0].id is None
        assert products[0].image is None
        assert products[0].brand is None
        assert products[0].title is None
        assert products[0].review_score is None
