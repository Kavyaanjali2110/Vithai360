from fastapi import APIRouter
from database.db import users

router = APIRouter()

@router.post("/register")

def register(data:dict):

    users.insert_one(data)

    return {"message":"User registered successfully"}


@router.post("/login")

def login(data:dict):

    user = users.find_one({"email":data["email"]})

    if user:
        return {"message":"Login successful"}

    return {"message":"Invalid user"}