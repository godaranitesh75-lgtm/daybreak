import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

database_url = make_url(os.getenv("DATABASE_URL", "sqlite:///./coffee_shop.db"))
if database_url.get_backend_name() == "postgresql" and database_url.drivername == "postgresql":
    database_url = database_url.set(drivername="postgresql+psycopg")

engine_options = {"pool_pre_ping": True}
if database_url.get_backend_name() == "sqlite":
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
