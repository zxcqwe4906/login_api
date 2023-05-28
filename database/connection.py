from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.registry import mapper_registry

with open('db_url.txt') as f:
    URL = f.read()

engine = create_engine(URL, echo=True)
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

Session = sessionmaker(bind=engine)