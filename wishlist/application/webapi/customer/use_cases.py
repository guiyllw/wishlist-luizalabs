from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse

from wishlist.application.webapi.common.models import Metadata
from wishlist.application.webapi.customer.models import (
    CreateCustomerRequest,
    CustomerListResponse,
    FullCustomer
)
from wishlist.domain.customer.exceptions import (
    CustomerAlreadyRegisteredError,
    CustomerNotFoundError
)
from wishlist.domain.customer.ports import (
    CreateCustomer,
    DeleteCustomer,
    FindCustomer,
    UpdateCustomer
)
from wishlist.infrastructure.customer.adapters import CustomerAdapter

router = APIRouter()

customer_adapter = CustomerAdapter()

find_customer_port = FindCustomer(customer_adapter)

create_customer_port = CreateCustomer(
    customer_adapter,
    find_customer_port
)

update_customer_port = UpdateCustomer(
    customer_adapter,
    find_customer_port
)

delete_customer_port = DeleteCustomer(customer_adapter)


@router.post('/')
async def create_customer(
    create_customer_request: CreateCustomerRequest
) -> FullCustomer:
    try:
        created_customer = await create_customer_port.create(
            create_customer_request.dict()
        )

        return JSONResponse(
            content=FullCustomer(**created_customer.dict()).dict(),
            status_code=HTTPStatus.CREATED
        )
    except CustomerAlreadyRegisteredError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.put('/')
async def update_customer(
    update_customer_request: FullCustomer
) -> FullCustomer:
    try:
        await update_customer_port.update(
            update_customer_request.dict()
        )

        return Response(status_code=HTTPStatus.OK)
    except CustomerAlreadyRegisteredError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/{id_}')
async def find_one_customer(id_: str) -> FullCustomer:
    try:
        customer = await find_customer_port.find_by_id(id_)
        if not customer:
            raise CustomerNotFoundError()

        return JSONResponse(
            content=FullCustomer(**customer.dict()).dict(),
            status_code=HTTPStatus.OK
        )
    except CustomerNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))


@router.get('/')
async def find_all_customer(
    page: int, size: int = 10
) -> CustomerListResponse:
    meta, customers = await find_customer_port.find_all(
        query={},
        page=page,
        size=size
    )

    return JSONResponse(
        content=CustomerListResponse(
            meta=Metadata(**meta),
            customers=customers
        ).dict(),
        status_code=HTTPStatus.OK
    )


@router.delete('/{id_}')
async def delete_customer(id_: str) -> Response:
    await delete_customer_port.delete(id_)

    return Response(status_code=HTTPStatus.NO_CONTENT)
