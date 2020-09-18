from typing import Dict, List, Optional

from wishlist.domain.wishlist.adapters import (
    AddProductsAdapter,
    FindWishListAdapter,
    UpdateWishListAdapter
)
from wishlist.domain.wishlist.models import WishList
from wishlist.infrastructure.common.databases import MongoDB


class WishListMongoAdapter(
    AddProductsAdapter,
    UpdateWishListAdapter,
    FindWishListAdapter
):
    def __init__(self):
        self._collection = MongoDB().get_collection('customer')

    async def add_to_list(self, WishList) -> WishList:
        pass

    async def update(self, wishlist: WishList) -> bool:
        pass

    async def find_one(
        self,
        query: Dict,
        projection: Optional[List[str]] = None
    ) -> WishList:
        pass
