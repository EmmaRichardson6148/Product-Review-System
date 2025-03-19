from pydantic import BaseModel
from typing import List, Optional

class ReviewCreate(BaseModel):
    product_id: int
    user_id: int
    rating: int
    review_text: str
    category_ids: List[int]

class ReviewSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    review_text: str

    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    reviews: List[ReviewSchema] = []

    class Config:
        from_attributes = True
