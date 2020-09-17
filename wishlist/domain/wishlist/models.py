from dataclasses import dataclass
from typing import List


@dataclass
class WishList:
    id: str = None
    customer_id: str = None
    product_ids: List[str] = None
