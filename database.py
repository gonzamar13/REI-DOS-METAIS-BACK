from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:reidosmetais2025@109.199.112.8:5433/postgres", echo=True)


SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base()
