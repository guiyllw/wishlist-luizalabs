import pytest

from wishlist.domain.customer.models import Customer


@pytest.fixture
def customer_dict():
    return {
        'id': 'fake-id',
        'name': 'Guilherme Vasconcellos',
        'email': 'fake-mail-2@test.com'
    }


@pytest.fixture
def customer(customer_dict):
    return Customer(
        id='fake-id',
        name=customer_dict['name'],
        email=customer_dict['email']
    )


@pytest.fixture
def customer_list_response(customer_dict):
    meta = {
        'page': 1,
        'size': 10,
        'count': 1
    }

    return (meta, [customer_dict])
