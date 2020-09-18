from typing import List

from wishlist.application.webapi.common.models import (
    Metadata,
    SerializableModel
)


class FullCustomer(SerializableModel):
    id: str
    name: str
    email: str


class CreateCustomerRequest(SerializableModel):
    name: str
    email: str


class CustomerListResponse(SerializableModel):
    meta: Metadata
    customers: List[FullCustomer]
