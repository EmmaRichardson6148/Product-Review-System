from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(250), nullable=False)
    description = Column(String, nullable=True)
    reviews = relationship("Review", back_populates="product")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    
    product = relationship("Product", back_populates="reviews")
    categories = relationship("ReviewCategoryMap", back_populates="review")

class ReviewCategory(Base):
    __tablename__ = "review_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(250), unique=True, nullable=False)

    category_mappings = relationship("ReviewCategoryMap", back_populates="category")

class ReviewCategoryMap(Base):
    __tablename__ = "review_category_map"

    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("review_categories.id"), primary_key=True)

    review = relationship("Review", back_populates="categories")
    category = relationship("ReviewCategory", back_populates="category_mappings")
