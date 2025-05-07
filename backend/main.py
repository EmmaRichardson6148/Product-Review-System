from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, Review, ReviewCategory, ReviewCategoryMap
from schemas import ReviewCreate, ProductResponse

from typing import List



app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

Base.metadata.create_all(bind=engine)

@app.post("/reviews/", response_model=ReviewCreate)
def submit_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(
        product_id=review.product_id,
        user_id=review.user_id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    for category_id in review.category_ids:
        db.add(ReviewCategoryMap(review_id=db_review.id, category_id=category_id))
    db.commit()

    return db_review

@app.get("/products/", response_model=List[ProductResponse])
def get_products(sort: str = None, rating: int = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)

    if rating:
        query = query.join(Review).filter(Review.rating >= rating)
    if category:
        query = query.join(ReviewCategoryMapping).join(ReviewCategory).filter(ReviewCategory.category_name == category)
    if sort == "rating":
        query = query.order_by(Review.rating.desc())

    return query.all()

@app.get("/reviews/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    return reviews
