from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.registry import mapper_registry
from models.user import User

from utils import userinfo_exist

class in_memory_db:
    def __init__(self):
        engine = create_engine("sqlite:///") # in memory db
        with engine.begin() as connection:
            mapper_registry.metadata.create_all(connection)

        self.Session = sessionmaker(bind=engine)

    def add_user(self, username, email):
        with self.Session.begin() as session:
            session.add(
                User(username=username, email=email, hashed_password='1234')
            )

def test_info_exist():
    db = in_memory_db()
    assert userinfo_exist(db.Session, 'jack123', 'jack456@gmail.com') == False
    db.add_user('jack123', 'jack456@gmail.com')
    assert userinfo_exist(db.Session, 'jack123', 'jack456@gmail.com') == True
    assert userinfo_exist(db.Session, 'jack', 'jack456@gmail.com') == True
