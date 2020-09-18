from typing import List, Optional

from pydantic import BaseModel


class WishList(BaseModel):
    id: Optional[str] = None
    customer_id: Optional[str] = None
    product_ids: Optional[List[str]] = None
