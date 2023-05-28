from fastapi import (
    FastAPI,
    Body,
    HTTPException,
    Response
)
from database.connection import Session
from pydantic import EmailStr
from utils import (
    get_password_hash,
    verify_password,
    userinfo_exist,
    create_access_token,
    verify_token
)
from models.user import User
from sqlalchemy import select, and_

app = FastAPI()

COOKIE_NAME = 'Authorization'

@app.post("/signup/")
def signup(
    username: str = Body(),
    email: EmailStr = Body(),
    password: str= Body()
):
    if userinfo_exist(Session=Session, username=username, email=email):
        raise HTTPException(status_code=401, detail='username or email already exists')

    try:
        password_hash = get_password_hash(password)
        with Session.begin() as session:
            new_user = User(
                username=username,
                email=email,
                hashed_password=password_hash,
            )
            session.add(new_user)
        token = create_access_token({'username': username, 'email': email})
        return {'message': 'success', 'token': token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='unkown error')

@app.post("/verify/{token}")
def verify(token: str):
    if verify_token(Session, token):
        return {'message': 'success'}
    else:
        raise HTTPException(status_code=402, detail='verify token failed')

@app.post("/signin/")
def signin(
    response: Response,
    username: str = Body(),
    email: EmailStr = Body(),
    password: str = Body(),
):
    # check if username, email exist
    with Session() as session:
        query = (
            select(User).where(
                and_(User.username==username, User.email==email)
            )
        )
        result_user = session.execute(query).scalar()
        if not result_user:
            raise HTTPException(status_code=403, detail='user not found')
        if not result_user.is_active:
            raise HTTPException(status_code=403, detail='user not verified')
    hashed_password = result_user.hashed_password

    if verify_password(plain_password=password, hashed_password=hashed_password):
        token = create_access_token({'username': username, 'email': email})
        response.set_cookie(key=COOKIE_NAME, value=token)
        return {COOKIE_NAME: token}
    else:
        raise HTTPException(status_code=406, detail='wrong password')
