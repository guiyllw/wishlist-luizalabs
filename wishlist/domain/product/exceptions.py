class ProductNotFoundError(Exception):
    def __init__(self):
        super().__init__('Product not found')
