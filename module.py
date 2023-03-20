from pydantic import BaseModel
from typing import Union
from passlib.context import CryptContext
from pymongo import MongoClient
from datetime import datetime, timedelta
from jose import jwt
from bson.objectid import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = MongoClient('mongodb://localhost:27017/')
auth_db = db.fastapi_api
users = auth_db.users

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[str, None] = None

class User(BaseModel):
    id: str
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserInDB(BaseModel):
    id: str
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    hashed_password: str

print(BaseModel)

def verify_password(plain_password, hashed_password):
    # パスワードが合ってるかをT/Fで返す
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    # パスワードをハッシュ化する。
    # bcryptは、毎回同じ値にならない
    return pwd_context.hash(password)

def get_user(_id: str):
    user = users.find_one({'_id': ObjectId(_id)})
    if user:
        # 展開してUserInDBインスタンスを作り出す
        user['id'] = str(user['_id'])
        user.pop('_id')
        newUser = UserInDB(**user)
        return newUser


def create_access_token(data: dict, SECRET_KEY: str, ALGORITHM: str):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=10)
    
    # {"sub":"username","expire":datetime.datetime(期限)}
    to_encode.update({"exp": expire})

    # Tokenの生成
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
