class AddProductsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NoValidProductsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
