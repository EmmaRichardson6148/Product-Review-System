from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    submitted = Column(DateTime, server_default=func.now())

    reviews = relationship("Review", back_populates="user")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(75), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    reviews = relationship("Review", back_populates="product")


class ReviewCategory(Base):
    __tablename__ = "review_categories"
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(250), unique=True, nullable=False)

    review_mappings = relationship("ReviewCategoryMap", back_populates="category")


class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    rating = Column(Integer, nullable=False)
    review_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    categories = relationship("ReviewCategoryMap", back_populates="review")


class ReviewCategoryMapping(Base):
    __tablename__ = "review_category_map"
    review_id = Column(Integer, ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True)
    category_id = Column(Integer, ForeignKey("review_categories.id", ondelete="CASCADE"), primary_key=True)

    review = relationship("Review", back_populates="categories")
    category = relationship("ReviewCategory", back_populates="review_mappings")