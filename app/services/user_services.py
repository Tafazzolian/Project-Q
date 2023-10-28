from app.repositories.user_repo import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_data: dict):
        return self.user_repository.get_user(user_data)
    
    def get_all_users(self):
        return self.user_repository.get_all_users()
    
    def create_user(self, first_name: str, last_name: str, mobile: str, membership: str, password: str, email: str = None):
        return self.user_repository.create_user(first_name, last_name, mobile, membership, password, email)


    
    def login_user(self):
        return
