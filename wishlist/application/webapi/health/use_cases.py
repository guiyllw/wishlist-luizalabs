from http import HTTPStatus

from fastapi import APIRouter, Response

router = APIRouter()


@router.get('/')
def health_check() -> Response:
    return Response(status_code=HTTPStatus.OK)
