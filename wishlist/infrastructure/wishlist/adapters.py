from typing import Dict, List, Optional

from wishlist.domain.wishlist.adapters import (
    AddProductsAdapter,
    FindWishListAdapter,
    UpdateWishListAdapter
)
from wishlist.domain.wishlist.models import WishList
from wishlist.infrastructure.common.databases import MongoDB


class WishListAdapter(
    AddProductsAdapter,
    UpdateWishListAdapter,
    FindWishListAdapter
):
    def __init__(self):
        self._collection = MongoDB().get_collection('wishlist')

    async def create(self, wishlist: Dict) -> WishList:
        id_ = await self._repository.create(wishlist)
        return WishList(id=id_, **wishlist)

    async def update(self, wishlist: Dict) -> bool:
        return await self._repository.update(wishlist['id'], wishlist)

    async def find_one(self, query: Dict) -> WishList:
        wishlist = await self._repository.find_one(query)
        if not wishlist:
            return None

        return WishList(**wishlist)
