from wishlist.domain.wishlist.models import WishList
from wishlist.domain.wishlist.ports import UpdateWishList
from wishlist.test.helpers import AsyncMock


class TestUpdateWishList:

    async def test_update_wishlist_with_success(
        self,
        update_wishlist_request
    ):
        update_wishlist = UpdateWishList(
            AsyncMock(return_value=True)
        )

        updated = await update_wishlist.update(
            WishList(**update_wishlist_request)
        )

        assert updated is True
