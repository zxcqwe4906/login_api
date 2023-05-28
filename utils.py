from passlib.context import CryptContext
from sqlalchemy import select, or_, and_
from models.user import User
from datetime import datetime, timedelta
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"])

SECRET_KEY = "my_secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

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

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    # specific key
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(Session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f'payload" {payload}')
        username = payload.get("username")
        email = payload.get("email")
        if not username or not email:
            return False
    except JWTError as e:
        print(f'error message: {e}')
        return False

    # check if username/email exist, if not, return False
    with Session.begin() as session:
        query = (
            select(User).where(
                and_(User.username==username, User.email==email)
            )
        )
        result_user = session.execute(query).scalar()
        if not result_user:
            return False

        result_user.is_active = True

    return True