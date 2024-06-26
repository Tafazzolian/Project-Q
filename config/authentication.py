from functools import wraps
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import timedelta

import secrets

from utils.tools import Tools
from .configs import config
from threading import Lock
lock = Lock()


def login_check(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.state.status == "Good_token":
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        return await func(request, *args, **kwargs)
    return wrapper


def admin_check(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        
        user_id = await AccessToken().check_token(request=request, token=request.state.token)
        if user_id:
            user = await kwargs["user_service"].get_user(user_data={"user_id": int(user_id)})
            print(f'admin status:{user.is_admin}')
        else:
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        if not user.is_admin:
            Tools.red(text="U R No Admin")
            raise HTTPException(status_code=401, detail="Unauthorized Access")
        return await func(request, *args, **kwargs)
    return wrapper


# es = Elasticsearch("http://localhost:9200")

# def generate_secret_key(length: int = 32) -> str:
#     return secrets.token_hex(length)
# random_secret_key = generate_secret_key()

class AccessToken:

    def __init__(
            self,
            SECRET_KEY = config.SECRET_KEY,
            ALGORITHM = config.ALGORITHM,
            ACCESS_TOKEN_EXPIRE_MINUTES = int(config.ACCESS_TOKEN_EXPIRE_MINUTES)
            ):
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

        self.credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authenticate": "Bearer"}
    )

    def create_access_token(self, data: dict):
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        expire = Tools.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    async def check_token(self, token, request):
        redis = request.app.state.redis
        
        if await redis.get(token):
            try:
                OAuth2PasswordBearer(tokenUrl=token)
                payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])#, options={"verify_exp": False})
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise self.credentials_exception
                Tools.green(key="check_token:",text="token approved")
                return user_id
            except:
                Tools.red(key="check_token:",text="failed to approve token")
                return None
        else:
            return None
        

    async def expire_token(self, token, redis):
        if lock.acquire(blocking=False):
            try:
                await redis.delete(token)
                Tools.green(key="expire_token:",text="token expired")
            except:
                Tools.red(key="expire_token:",text="failed to expire token")
            finally:    
                lock.release()
        pass