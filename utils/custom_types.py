from sqlalchemy.types import TypeDecorator, LargeBinary
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

class EncryptedType(TypeDecorator):
    impl = LargeBinary

    def __init__(self, *args, **kwargs):
        key = os.getenv('ENCRYPTION_KEY')
        if key is None:
            raise ValueError("ENCRYPTION_KEY environment variable not set")
        self.fernet = Fernet(key.encode())
        super().__init__(*args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return self.fernet.encrypt(value.encode())
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.fernet.decrypt(value).decode()
        return value
