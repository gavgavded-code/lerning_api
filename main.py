from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import json
from typing import List, TypedDict
class person(TypedDict):
    name: str
    number: int
    password: str
app=FastAPI()

DATA_FILE="data.json"

def load_users()->List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE,'r',encoding='utf-8') as file:
            return json.load(file)
    except(json.JSONDecodeError, FileNotFoundError):
        return []

def save_users(users:List[dict])->None:
    with open(DATA_FILE,'w',encoding="utf-8") as file:
        json.dump(users,file,ensure_ascii=False,indent=2)

def user_in_json(users:List[dict],name:str,number:int)->bool:
    for user in users:
            if user.get('name') == name and user.get('number') == number:
                return True
    return False 

@app.get("/")
def home():
    return FileResponse("public/index.html")

@app.post("/hello")
def hello(user:person):
    users=load_users()
    if user_in_json(users, user.get('name'),user.get('number')):
        return{"message":"Вы уже зарегстрированы"}
    else:
        new_user={"name": user.get('name'), "number": user.get('number'),"password": user.get('password')}
        users.append(new_user)
        save_users(users)
        return {"message":f"hi {user.get('name')}, your number-{user.get('number')}, your password-{user.get('password')}"}