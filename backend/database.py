from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Ecr05080!@localhost:3306/product_reviews" # Connect to MySQL database

# Connect to MySQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# Create session for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


