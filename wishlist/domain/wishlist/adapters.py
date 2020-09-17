import abc

from wishlist.domain.wishlist.models import WishList


class AddProductsAdapter(metaclass=abc.ABCMeta):
    async def add_to_list(self, WishList) -> WishList:
        pass  # pragma: no-cover
