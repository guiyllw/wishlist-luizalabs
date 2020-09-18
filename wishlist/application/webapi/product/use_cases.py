from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse

from wishlist.application.webapi.common.models import Metadata
from wishlist.application.webapi.product.models import (
    CreateProductRequest,
    ProductListResponse,
    ProductResponse
)
from wishlist.domain.product.ports import (
    CreateProduct,
    DeleteProduct,
    FindProduct,
    UpdateProduct
)
from wishlist.infrastructure.product.adapters import ProductAdapter

router = APIRouter()

product_adapter = ProductAdapter()

find_product_port = FindProduct(product_adapter)
create_product_port = CreateProduct(product_adapter)
update_product_port = UpdateProduct(product_adapter)
delete_product_port = DeleteProduct(product_adapter)


@router.post('/')
async def create_product(
    create_product_request: CreateProductRequest
) -> ProductResponse:
    created_product = await create_product_port.create(
        create_product_request.dict()
    )

    return JSONResponse(
        content=created_product,
        status_code=HTTPStatus.CREATED
    )


@router.get('/{id_}')
async def find_one_product(
    id_: str
) -> ProductResponse:
    product = await find_product_port.find_by_id(id_)
    if not product:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    return JSONResponse(
        content=product,
        status_code=HTTPStatus.OK
    )


@router.get('/')
async def find_all_product(page: int, size: int = 10) -> ProductListResponse:
    meta, products = await find_product_port.find_all(
        query={},
        page=page,
        size=size
    )

    return JSONResponse(
        content=ProductListResponse(
            meta=Metadata(**meta),
            products=products
        ),
        status_code=HTTPStatus.OK
    )


@router.delete('/{id_}')
async def delete_product(id_: str) -> Response:
    await delete_product_port.delete(id_)

    return Response(status_code=HTTPStatus.NO_CONTENT)
