from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("DATABASE_URL", echo=True)


SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
