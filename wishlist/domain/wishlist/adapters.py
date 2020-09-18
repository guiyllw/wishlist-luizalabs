import abc
from typing import Dict

from wishlist.domain.wishlist.models import WishList


class AddProductsAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add_to_list(self, WishList) -> WishList:
        pass  # pragma: no-cover


class UpdateWishListAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, wishlist: WishList) -> bool:
        pass  # pragma: no-cover


class FindWishListAdapter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find_one(self, query: Dict) -> WishList:
        pass  # pragma: no-cover
