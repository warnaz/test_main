from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


login, password = "postgres", "master"
engine = create_engine(url=f"postgresql://{login}:{password}@db/postgres", echo=True)
