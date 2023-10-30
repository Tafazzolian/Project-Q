from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import secrets

def generate_secret_key(length: int = 32) -> str:
    return secrets.token_hex(length)

random_secret_key = generate_secret_key()

secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

class AccessToken:

    def __init__(self, SECRET_KEY = secret_key ,ALGORITHM = "HS256", ACCESS_TOKEN_EXPIRE_MINUTES = 30):
        self.SECRET_KEY = SECRET_KEY
        self.ALGORITHM = ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

    def create_access_token(self, data: dict):
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
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
            print("check_token: token approved - user_id returend")
            return user_id
        except:
            print("check_token: token failed - None returned")
            return None