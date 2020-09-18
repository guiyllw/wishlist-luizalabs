from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse

from wishlist.application.webapi.wishlist.models import (
    AddProductsRequest,
    CustomerWishList,
    FullCustomerWishList
)
from wishlist.domain.customer.exceptions import CustomerNotFoundError
from wishlist.domain.customer.ports import FindCustomer
from wishlist.domain.product.ports import FindProduct
from wishlist.domain.wishlist.exceptions import (
    NoValidProductsError,
    WishListNotFoundError
)
from wishlist.domain.wishlist.ports import (
    AddProducts,
    FindWishList,
    RemoveProducts,
    UpdateWishList
)
from wishlist.infrastructure.customer.adapters import CustomerAdapter
from wishlist.infrastructure.product.adapters import ProductAdapter
from wishlist.infrastructure.wishlist.adapters import WishListAdapter

router = APIRouter()

wishlist_adapter = WishListAdapter()
customer_adapter = CustomerAdapter()
product_adapter = ProductAdapter()

find_wishlist_port = FindWishList(wishlist_adapter)
find_customer_port = FindCustomer(customer_adapter)
find_product_port = FindProduct(product_adapter)

update_wishlist_port = UpdateWishList(wishlist_adapter)

add_products_port = AddProducts(
    wishlist_adapter,
    find_wishlist_port,
    update_wishlist_port,
    find_customer_port,
    find_product_port
)

remove_products_port = RemoveProducts(
    find_wishlist_port,
    update_wishlist_port
)


@router.post('/')
async def add_products(
    add_products_request: AddProductsRequest
) -> CustomerWishList:
    try:
        customer_wishlist = await add_products_port.add_to_list(
            add_products_request.dict()
        )

        return JSONResponse(
            content=CustomerWishList(
                **customer_wishlist.dict()
            ).dict(),
            status_code=HTTPStatus.CREATED
        )
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except NoValidProductsError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.get('/{customer_id}')
async def find_customer_wishlist(
    customer_id: str
) -> FullCustomerWishList:
    try:
        wishlist = await find_wishlist_port.find_customer_wishlist(customer_id)
        if not wishlist:
            raise WishListNotFoundError()

        products = []
        for product_id in wishlist.product_ids:
            product = await find_product_port.find_by_id(product_id)
            if product:
                products.append(product)

        return JSONResponse(
            content=FullCustomerWishList(
                id=wishlist.id,
                customer_id=wishlist.customer_id,
                products=products
            ).dict(),
            status_code=HTTPStatus.OK
        )
    except (CustomerNotFoundError, WishListNotFoundError) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.patch('/{customer_id}')
async def remove_products(
    customer_id: str, product_ids: List[str]
) -> FullCustomerWishList:
    try:
        await remove_products_port.remove_products(
            customer_id, product_ids
        )

        return Response(status_code=HTTPStatus.OK)
    except (CustomerNotFoundError, WishListNotFoundError) as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
