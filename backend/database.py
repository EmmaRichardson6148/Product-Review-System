from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv() # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://Ecr05080!@localhost/product_reviews") # Connect to MySQL database

engine = create_engine(DATABASE_URL) # Database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Create a session maker
Base = declarative_base() # Base class for models

# Initialize database tables
def init_db():
    import models
    Base.metadata.create_all(bind=engine)


