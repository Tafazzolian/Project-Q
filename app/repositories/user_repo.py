from sqlalchemy.orm import Session
from db.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from sqlalchemy import or_, text



class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self,user_data):
#         query = text("""
# SELECT * FROM account.users WHERE id=1
# """)
#         user = self.db.execute(query).fetchone()
        conditions = []
        if "mobile" in user_data:
            conditions.append(User.mobile == user_data["mobile"])
        if "last_name" in user_data:
            conditions.append(User.last_name == user_data["last_name"])
        if "user_id" in user_data:
            conditions.append(User.id == user_data["user_id"])
        if "email" in user_data:
            conditions.append(User.id == user_data["email"])
        
        if not conditions:
            return None  # or raise an exception if you prefer
        
        user = self.db.query(User).filter(or_(*conditions)).first()
        
        return user
    
    def get_all_users(self):
        return self.db.query(User).all()
    
    def create_user(self, first_name, last_name, mobile, membership, password, email=None):
        user = User(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            membership=membership,
            email=email,
            hashed_password=User.hash_password(password)
        )
        self.db.add(user)
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            error_info = str(e.__dict__['orig'])
            self.db.rollback()
            return JSONResponse(content={"error": "Something went wrong", "detail": error_info},
                                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def login_user(self, mobile, password, email=None):
         user = self.db.query(User).filter(mobile=mobile,hash_password= User.check_password(password), email= email)
         if not user:
              raise 'user not found'
         return 'we found ya'
        

