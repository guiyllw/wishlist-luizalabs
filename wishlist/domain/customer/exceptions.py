class CustomerAlreadyRegisteredError(Exception):
    def __init__(self):
        super().__init__('Customer already registered')


class CustomerNotFoundError(Exception):
    def __init__(self):
        super().__init__('Customer not found')
