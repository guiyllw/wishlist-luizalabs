from wishlist.domain.product.models import Product
from wishlist.domain.product.ports import UpdateProduct
from wishlist.test.helpers import AsyncMock


class TestUpdateProduct:

    async def test_update_product_with_success(
        self,
        update_product_request
    ):
        update_product = UpdateProduct(
            AsyncMock(return_value=True)
        )

        updated = await update_product.update(
            Product(**update_product_request)
        )

        assert updated is True
