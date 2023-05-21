from fastapi import FastAPI
from database.connection import Session
from pydantic import EmailStr

app = FastAPI()

@app.post("/signup/")
def signup(
    username: str,
    email: EmailStr,
    password: str
):
    return {
        'username': username,
        'email': email,
    }
