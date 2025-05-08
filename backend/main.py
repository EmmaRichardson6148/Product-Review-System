from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, Review, ReviewCategory, ReviewCategoryMap, User
from schemas import ReviewCreate, ProductResponse, UserCreate, UserResponse, ProductCreate

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

@app.post("/seed/")
def seed_data(db: Session = Depends(get_db)):

    if db.query(Product).first():
        return {"message": "Already seeded."}

    product = Product(product_name="Floral skirt", description="A-line maxi skirt with floral print")
    category = ReviewCategory(category_name="Durability")
    db.add_all([product, category])
    db.commit()
    return {"message": "Seeded sample product and category"}

@app.post("/seed/categories/")
def seed_review_categories(db: Session = Depends(get_db)):
    categories = [
        ReviewCategory(category_name="Fit"),
        ReviewCategory(category_name="Material"),
        ReviewCategory(category_name="Durability"),
        ReviewCategory(category_name="Style"),
        ReviewCategory(category_name="Value for Money")
    ]

    db.add_all(categories)
    db.commit()
    return {"message": "Review categories seeded"}


@app.post("/products/", response_model=ProductResponse)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/seed/users/")
def seed_users(db: Session = Depends(get_db)):
    users = [
        User(name="Alice"),
        User(name="Barb"),
        User(name="Charlie"),
        User(name="Diana"),
        User(name="Emily"),
        User(name="Fiona"),
        User(name="Ally"),
        User(name="Hannah"),
        User(name="Sara"),
        User(name="Jasmine")
    ]

    db.add_all(users)
    db.commit()
    return {"message": "Users seeded"}


@app.post("/reviews/", response_model=ReviewCreate)
def submit_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Check if user exists, or create new one
    user = db.query(User).filter(User.name == review.user_name).first()
    if not user:
        user = User(name=review.user_name)
        db.add(user)
        db.commit()
        db.refresh(user)

    db_review = Review(
        product_id=review.product_id,
        user_id=user.id,
        rating=review.rating,
        review_text=review.review_text
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    for category_id in review.category_ids:
        db.add(ReviewCategoryMap(review_id=db_review.id, category_id=category_id))
    db.commit()

    return {"message": "Review submitted."}

@app.get("/products/", response_model=List[ProductResponse])
def get_products(sort: str = None, rating: int = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Product)

    if rating:
        query = query.join(Review).filter(Review.rating >= rating)
    if category:
        query = query.join(ReviewCategoryMap).join(ReviewCategory).filter(ReviewCategory.category_name == category)
    if sort == "rating":
        query = query.order_by(Review.rating.desc())

    return query.all()

@app.get("/reviews/{product_id}")
def get_reviews(product_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found")
    return reviews