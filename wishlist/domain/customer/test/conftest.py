import pytest

from wishlist.domain.customer.models import Customer


@pytest.fixture
def create_customer_request():
    return {
        'name': 'Guilherme',
        'email': 'fake-mail@test.com'
    }


@pytest.fixture
def customer_response(create_customer_request):
    return Customer(
        id_='fake-id',
        name=create_customer_request['name'],
        email=create_customer_request['email']
    )


@pytest.fixture
def customer_response_email_projected(create_customer_request):
    return Customer(
        email=create_customer_request['email']
    )


@pytest.fixture
def customer_list_response(customer_response):
    meta = {
        'page': 1,
        'size': 10,
        'count': 1
    }

    return (meta, [customer_response])


@pytest.fixture
def customer_list_response_email_projected(customer_response_email_projected):
    meta = {
        'page': 1,
        'size': 10,
        'count': 1
    }

    return (meta, [customer_response_email_projected])


@pytest.fixture
def update_customer_request():
    return {
        'id': 'fake-id',
        'name': 'Guilherme',
        'email': 'fake-mail@test.com'
    }
