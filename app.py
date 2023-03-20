from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel

from module import Token, TokenData, User, UserInDB
from module import verify_password, get_password_hash, get_user, create_access_token

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "5d529dee94d237dd6c8d2ab8284e2e56582a20379b545f1e797a45629b5549d4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# AccesTokenと同じ感じでRefleshTokenを作成する
# DBにリフレッシュトークンを保存

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

def authenticate_user(_id: str, password: str):
    # UserInDBインスタンスをuserに突っ込む
    user = get_user(_id)

    # ユーザーが存在している&パスワードが合っているときにUserInDBのインスタンスを返す
    # そうじゃなければFalseらしい
    if not user:
        print('not user')
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        # 解読してみる
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("sub") is None:
            raise credentials_exception

        token_data = TokenData(id=payload.get("sub"))
    except ExpiredSignatureError:
        print('ki☆ge☆n☆gi☆re')
        raise HTTPException(status_code=403, detail="token has been expired")
    except JWTError:
        raise credentials_exception

    # UserIdDBインスタンスを作って返す
    user = get_user(_id=token_data.id)

    # 実はそんなユーザーがいなかった場合
    if user is None:
        raise credentials_exception
    
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    print(form_data.username)
    # ユーザーの検証(False or UserInDB)
    user = authenticate_user(_id=form_data.username, password=form_data.password)
    
    # ログイン失敗
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="LoginError",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # tokenの生成
    print(user)
    access_token = create_access_token(data={"sub": user.id}, SECRET_KEY=SECRET_KEY, ALGORITHM=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    # TokenからUserInDBをいただく
    return current_user

