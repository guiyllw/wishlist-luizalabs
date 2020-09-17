from wishlist.domain.product.ports import CreateProduct
from wishlist.test.helpers import AsyncMock


class TestCreateProduct:

    async def test_create_product_with_success(
        self,
        create_product_request,
        product_response
    ):
        create_product = CreateProduct(
            AsyncMock(return_value=product_response)
        )

        product = await create_product.create(create_product_request)

        assert product == product_response
