import abc
from typing import Dict, List
from uuid import uuid4

from wishlist.domain.customer.exceptions import CustomerNotFoundError
from wishlist.domain.customer.models import Customer
from wishlist.domain.customer.ports import FindCustomerPort
from wishlist.domain.product.ports import FindProductPort
from wishlist.domain.wishlist.adapters import (
    AddProductsAdapter,
    FindWishListAdapter,
    UpdateWishListAdapter
)
from wishlist.domain.wishlist.exceptions import NoValidProductsError
from wishlist.domain.wishlist.models import WishList


class AddProductsPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add_to_list(
        self, customer_id: str, product_ids: List[str]
    ) -> WishList:
        pass  # pragma: no-cover


class FindWishListPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def find_one(self, query: Dict) -> Customer:
        pass  # pragma: no-cover

    async def find_customer_wishlist(self, customer_id: str):
        return await self.find_one({
            'customer_id': customer_id
        })


class UpdateWishListPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, wishlist: Dict) -> bool:
        pass  # pragma: no-cover


class RemoveProductsPort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def remove_products(
        self, customer_id: str, product_ids: List[str]
    ) -> bool:
        pass  # pragma: no-cover


class FindWishList(FindWishListPort):
    def __init__(self, find_wishlist_adapter: FindWishListAdapter):
        self._find_wishlist_adapter = find_wishlist_adapter

    async def find_one(self, query: Dict) -> WishList:
        return await self._find_wishlist_adapter.find_one(query)


class UpdateWishList(UpdateWishListPort):
    def __init__(self, update_wishlist_adapter: UpdateWishListAdapter):
        self._update_wishlist_adapter = update_wishlist_adapter

    async def update(self, wishlist: Dict) -> bool:
        return await self._update_wishlist_adapter.update(wishlist)


class AddProducts(AddProductsPort):
    def __init__(
        self,
        add_products_adapter: AddProductsAdapter,
        find_wishlist_port: FindWishListPort,
        update_wishlist_port: UpdateWishListPort,
        find_customer_port: FindCustomerPort,
        find_product_port: FindProductPort
    ):
        self._add_products_adapter = add_products_adapter
        self._find_wishlist_port = find_wishlist_port
        self._update_wishlist_port = update_wishlist_port
        self._find_customer_port = find_customer_port
        self._find_product_port = find_product_port

    async def add_to_list(
        self, add_products_request: Dict
    ) -> WishList:
        customer_id = add_products_request['customer_id']
        product_ids = add_products_request['product_ids']

        customer_exists = await self._find_customer_port.find_by_id(
            customer_id
        )
        if not customer_exists:
            raise CustomerNotFoundError()

        valid_product_ids = await self._get_valid_product_ids(product_ids)
        if not valid_product_ids:
            raise NoValidProductsError()

        unique_product_ids = self._get_unique_product_ids(
            valid_product_ids
        )

        wishlist = await self._find_wishlist_port.find_customer_wishlist(
            customer_id
        )

        if not wishlist:
            return await self._add_products_adapter.create({
                'id': str(uuid4()),
                'customer_id': customer_id,
                'product_ids': unique_product_ids
            })

        unique_product_ids = self._get_unique_product_ids([
            *wishlist.product_ids,
            *unique_product_ids
        ])

        wishlist.product_ids = unique_product_ids

        await self._update_wishlist_port.update(wishlist.dict())
        return wishlist

    async def _get_valid_product_ids(
        self, product_ids: List[str]
    ) -> List[str]:
        valid_product_ids = []
        for product_id in product_ids:
            product_exists = await self._find_product_port.find_by_id(
                product_id
            )

            if not product_exists:
                continue

            valid_product_ids.append(product_id)

        return valid_product_ids

    def _get_unique_product_ids(self, product_ids: List[str]) -> List[str]:
        return list(set(product_ids))


class RemoveProducts(RemoveProductsPort):
    def __init__(
        self,
        find_wishlist_port: FindWishListPort,
        update_wishlist_port: UpdateWishListPort
    ):
        self._find_wishlist_port = find_wishlist_port
        self._update_wishlist_port = update_wishlist_port

    async def remove_products(
        self, customer_id: str, product_ids: List[str]
    ) -> bool:
        wishlist = await self._find_wishlist_port.find_customer_wishlist(
            customer_id
        )

        if not wishlist:
            return False

        new_product_ids = []
        for product_id in wishlist.product_ids:
            if product_id in product_ids:
                continue

            new_product_ids.append(product_id)

        wishlist.product_ids = new_product_ids

        return await self._update_wishlist_port.update(wishlist.dict())
