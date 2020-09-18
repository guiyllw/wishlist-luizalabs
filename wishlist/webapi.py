from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from wishlist.application.webapi.common.helpers import format_error
from wishlist.application.webapi.customer.use_cases import (
    router as customer_router
)
from wishlist.application.webapi.health.use_cases import (
    router as health_router
)
from wishlist.application.webapi.product.use_cases import (
    router as product_router
)
from wishlist.application.webapi.wishlist.use_cases import (
    router as wishlist_router
)

app = FastAPI(title='WishList',
              description='LuizaLabs hiring test')


def configure_handlers():
    @app.exception_handler(Exception)
    async def exception_handler(
        _: Request,
        e: Exception
    ) -> JSONResponse:

        return JSONResponse(content=format_error(e),
                            status_code=HTTPStatus.INTERNAL_SERVER_ERROR)


def configure_routes():
    app.include_router(
        router=health_router,
        tags=['Health Check']
    )

    app.include_router(
        router=customer_router,
        prefix='/customer',
        tags=['Customer']
    )

    app.include_router(
        router=product_router,
        prefix='/product',
        tags=['Product']
    )

    app.include_router(
        router=wishlist_router,
        prefix='/wishlist',
        tags=['WishList']
    )


def configure():
    configure_routes()
    configure_handlers()


configure()
