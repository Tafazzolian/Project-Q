from fastapi import HTTPException, status
from app.repositories.user_repo import UserRepository
from db.models.user import User
from config.Auth import AccessToken


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_data: dict):
        return self.user_repository.get_user(user_data)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def create_user(self, user_data: dict):
        return self.user_repository.create_user(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            mobile=user_data["mobile"], 
            password=user_data["password"],
            email=user_data["email"]
            )

    def login_user(self, user_data: dict):
        user = self.user_repository.get_user(user_data)

        if not user or not User.check_password(provided_password=user_data["password"],stored_password=user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = AccessToken()
        access_token = token.create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer", "user_id":user.id}
