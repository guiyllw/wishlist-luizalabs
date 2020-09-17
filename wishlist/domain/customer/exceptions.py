class CustomerAlreadyRegisteredError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CustomerNotFoundError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
