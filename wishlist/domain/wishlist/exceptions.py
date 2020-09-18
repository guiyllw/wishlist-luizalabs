class NoValidProductsError(Exception):
    def __init__(self):
        super().__init__('No valid products found')


class WishListNotFoundError(Exception):
    def __init__(self):
        super().__init__('Wishlist not found')
