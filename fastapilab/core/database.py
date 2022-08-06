from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import os

engine_uri = URL(
        drivername='postgresql',
        username=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT"),
        database=os.environ.get("POSTGRES_DATABASE")
    )
engine = create_engine(engine_uri, pool_size=int(os.environ.get("POOL_SIZE")),
        max_overflow=int(os.environ.get("POOL_OVERFLOW")))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
