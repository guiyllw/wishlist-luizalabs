from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from wishlist.application.webapi.wishlist.models import (
    AddProductsRequest,
    CustomerWishListResponse
)
from wishlist.domain.customer.exceptions import CustomerNotFoundError
from wishlist.domain.customer.ports import FindCustomer
from wishlist.domain.product.ports import FindProduct
from wishlist.domain.wishlist.exceptions import NoValidProductsError
from wishlist.domain.wishlist.ports import (
    AddProducts,
    FindWishList,
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


@router.post('/')
async def add_products(
    add_products_request: AddProductsRequest
) -> CustomerWishListResponse:
    try:
        customer_wishlist = await add_products_port.create(
            add_products_request.dict()
        )

        return JSONResponse(
            content=customer_wishlist,
            status_code=HTTPStatus.CREATED
        )
    except CustomerNotFoundError:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    except NoValidProductsError:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.get('/{customer_id}')
async def find_customer_wishlist(
    customer_id: str
) -> CustomerWishListResponse:
    wishlist = await find_wishlist_port.find_customer_wishlist(customer_id)
    if not wishlist:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    products = []
    for product_id in wishlist.product_ids:
        product = await find_product_port.find_by_id(product_id)
        products.append(product)

    return JSONResponse(
        content=CustomerWishListResponse(
            id=wishlist.id,
            customer_id=wishlist.customer_id,
            products=products
        ),
        status_code=HTTPStatus.OK
    )
