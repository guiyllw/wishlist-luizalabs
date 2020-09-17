from dataclasses import dataclass


@dataclass
class Product:
    id: str = None
    price: float = None
    image: str = None
    brand: str = None
    title: str = None
    review_score: float = None
