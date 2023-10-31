from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import timedelta
import secrets
from utils.tools import Tools
from .configs import config

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

    def create_access_token(self, data: dict):
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        expire = Tools.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    def check_token(self, token):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        try:
            OAuth2PasswordBearer(tokenUrl=token)
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])#, options={"verify_exp": False})
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            Tools.green(key="check_token:",text="token approved - user_id returend")
            return user_id
        except:
            Tools.red(key="check_token:",text="token failed - None returned")
            return None