from fastapi import FastAPI, Body, HTTPException
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

app = FastAPI()

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
