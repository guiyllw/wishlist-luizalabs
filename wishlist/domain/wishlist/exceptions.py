class AddProductsError(Exception):
    def __init__(self):
        super().__init__('Error on add product to wishlist')


class NoValidProductsError(Exception):
    def __init__(self):
        super().__init__('No valid products found')
