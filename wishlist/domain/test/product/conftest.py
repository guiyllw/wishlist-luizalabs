import pytest

from wishlist.domain.product.models import Product


@pytest.fixture
def create_product_request():
    return {
        'price': 99.90,
        'brand': 'tabajara',
        'title': 'Descascador de uva',
        'review_score': 4.5
    }


@pytest.fixture
def product_response(create_product_request):
    return Product(
        id='fake-id',
        price=create_product_request['price'],
        brand=create_product_request['brand'],
        title=create_product_request['title'],
        review_score=create_product_request['review_score']
    )


@pytest.fixture
def product_response_price_projected(create_product_request):
    return Product(
        price=create_product_request['price']
    )


@pytest.fixture
def product_list_response(product_response):
    meta = {
        'page': 1,
        'size': 10,
        'count': 1
    }

    return (meta, [product_response])


@pytest.fixture
def product_list_response_price_projected(product_response_price_projected):
    meta = {
        'page': 1,
        'size': 10,
        'count': 1
    }

    return (meta, [product_response_price_projected])


@pytest.fixture
def update_product_request():
    return {
        'id': 'fake-id',
        'price': 119.90,
        'brand': 'tabajara inc',
        'title': 'Descascador de azeitona',
        'review_score': 3.0
    }
