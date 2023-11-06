from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.repositories.user_repo import UserRepository
from db.models.user import User
from config.authentication import AccessToken
from config.logs import logger
from redis.exceptions import ConnectionError



class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_data: dict):
        return self.user_repository.get_user(user_data)
    
    def get_all_users(self, request:Request):
        return self.user_repository.get_all_users(request=request)
    
    def create_user(self, user_data: dict):
        return self.user_repository.create_user(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            mobile=user_data["mobile"], 
            password=user_data["password"],
            email=user_data["email"]
            )

    async def login_user(self, user_data: dict, request):
        user = await self.user_repository.get_user(user_data)
        if not User.check_password(provided_password=user_data["password"],stored_password=user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"Authenticate": "Bearer"},
            )
        
        token = AccessToken()
        access_token = token.create_access_token(data={"sub": str(user.id)})
        try:
            redis = request.app.state.redis
            await redis.set(access_token,user.id,ex=1800)
        except ConnectionError as e:
            logger.exception(e)
            # raise Exception
            return JSONResponse({"error":"redis connection failed"}, status_code=404)
        return {"access_token": access_token, "token_type": "bearer", "user_id":user.id}
    

    async def log_out(self,request:Request):
        token = request.state.token
        redis = request.app.state.redis
        AccessToken().expire_token(token,redis)
