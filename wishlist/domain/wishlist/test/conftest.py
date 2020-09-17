import pytest

from wishlist.domain.customer.models import Customer
from wishlist.domain.wishlist.models import WishList


@pytest.fixture
def product_ids():
    return [
        '1',
        '2',
        '3',
        '4',
        '5'
    ]


@pytest.fixture
def product_ids_with_duplication(wishlist_response):
    return [
        *wishlist_response.product_ids,
        'fake-product-id-6',
        'fake-product-id-7',
        'fake-product-id-8'
    ]


@pytest.fixture
def wishlist_response():
    return WishList(
        id='fake-id',
        customer_id='fake-customer-id',
        product_ids=[
            'fake-product-id-1',
            'fake-product-id-2',
            'fake-product-id-3',
            'fake-product-id-4',
            'fake-product-id-5'
        ]
    )


@pytest.fixture
def found_customer():
    return Customer(
        id='fake-id',
        name='Guilherme',
        email='fake-mail@test.com'
    )


@pytest.fixture
def wishlist_response_customer_id_projected():
    return WishList(
        customer_id='fake-customer-id'
    )


@pytest.fixture
def update_wishlist_request(product_ids):
    return {
        'id': 'fake-id',
        'customer_id': 'fake-customer-id',
        'product_ids': product_ids
    }
