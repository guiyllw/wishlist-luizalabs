from wishlist.domain.product.ports import DeleteProduct
from wishlist.test.helpers import AsyncMock


class TestDeleteProduct:

    async def test_delete_product_with_success(self):
        delete_product = DeleteProduct(
            AsyncMock(return_value=1)
        )

        n_deleted = await delete_product.delete('fake-id')

        assert n_deleted == 1

    async def test_delete_product_that_not_exists(
        self,
        update_product_request,
        product_response
    ):
        delete_product = DeleteProduct(
            AsyncMock(return_value=0)
        )

        n_deleted = await delete_product.delete('fake-id')

        assert n_deleted == 0
