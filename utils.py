from passlib.context import CryptContext
from sqlalchemy import select, or_
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"])

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def userinfo_exist(Session, username, email) -> bool:
    with Session() as session:
        query = (
            select(User).where(
                or_(User.username==username, User.email==email)
            )
        )
        results = session.execute(query).all()
    return len(results) > 0
