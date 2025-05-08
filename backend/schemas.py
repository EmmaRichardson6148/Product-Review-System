from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewCreate(BaseModel):
    product_id: int
    user_name: str
    rating: int = Field(..., ge=1, le=5)
    review_text: str
    category_ids: List[int]

class ReviewSchema(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    review_text: str

    class Config:
        orm_mode = True

class ReviewResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    rating: int
    review_text: str

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    product_name: str
    description: Optional[str]
    reviews: List[ReviewSchema] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_id": 1,
                "user_id": 123,
                "rating": 5,
                "review_text": "Great value!",
                "category_ids": [1, 2]
            }
        }
class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ProductCreate(BaseModel):
    product_name: str
    description: str