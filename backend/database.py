from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Ecr05080%21@localhost:3306/product_reviews" Connect to MySQL database
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./test.db")

# Connect to MySQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create session for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


