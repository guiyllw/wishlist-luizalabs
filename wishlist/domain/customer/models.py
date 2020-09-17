from dataclasses import dataclass


@dataclass
class Customer:
    id: str = None
    name: str = None
    email: str = None
