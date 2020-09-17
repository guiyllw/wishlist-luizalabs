import pytest

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
def product_ids_with_unknown_ids():
    return [
        '1',
        'unknown-2',
        '3',
        'unknown-4',
        '5'
    ]


@pytest.fixture
def wishlist_response():
    return WishList(
        id_='fake-id',
        customer_id='fake-customer-id',
        product_ids=[
            'fake-product-id-1',
            'fake-product-id-2',
            'fake-product-id-3',
            'fake-product-id-4',
            'fake-product-id-5'
        ]
    )
