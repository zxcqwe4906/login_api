from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.registry import mapper_registry

engine = create_engine("sqlite:///user.db", echo=True)
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

Session = sessionmaker(bind=engine)