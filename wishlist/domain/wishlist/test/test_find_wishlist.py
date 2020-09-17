from wishlist.domain.wishlist.ports import FindWishList
from wishlist.test.helpers import AsyncMock


class TestFindWishList:

    async def test_find_one_with_all_fields_succeeded(
        self,
        wishlist_response
    ):
        find_wishlist = FindWishList(
            AsyncMock(return_value=wishlist_response)
        )

        wishlist = await find_wishlist.find_one({
            'id': 'fake-id'
        })

        assert wishlist == wishlist_response

    async def test_find_one_with_projected_field_succeeded(
        self,
        wishlist_response_customer_id_projected
    ):
        find_wishlist = FindWishList(
            AsyncMock(
                return_value=wishlist_response_customer_id_projected
            )
        )

        wishlist = await find_wishlist.find_one({
            'id': 'fake-id'
        })

        customer_id = wishlist_response_customer_id_projected.customer_id

        assert wishlist.customer_id == customer_id
        assert wishlist.id is None
        assert wishlist.product_ids is None
