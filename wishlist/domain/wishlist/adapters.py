import abc
from typing import Dict, List, Optional

from wishlist.domain.wishlist.models import WishList


class AddProductsAdapter(metaclass=abc.ABCMeta):
    async def add_to_list(self, WishList) -> WishList:
        pass  # pragma: no-cover


class UpdateWishListAdapter(metaclass=abc.ABCMeta):
    async def update(self, wishlist: WishList) -> bool:
        pass  # pragma: no-cover


class FindWishListAdapter(metaclass=abc.ABCMeta):
    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> WishList:
        pass  # pragma: no-cover
