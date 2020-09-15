from dataclasses import dataclass


@dataclass
class Customer:
    id_: str = None
    name: str = None
    email: str = None
