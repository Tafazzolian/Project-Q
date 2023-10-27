import re
from .abstract_validator import AbstractValidator
from password_strength import PasswordPolicy

class PhoneNumberValidator(AbstractValidator):
    def __init__(self, loc: str, phone_number: str):
        self.phone_number = phone_number
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_phone_number"

    def passes(self) -> bool:
        return re.match(r"^(0)?9\d{9}$", self.phone_number) is not None


class EmailValidator(AbstractValidator):
    def __init__(self, loc: str, email: str):
        self.email = email
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_email"

    def passes(self) -> bool:
        return re.match(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", self.email) is not None


class PostalCodeValidator(AbstractValidator):
    def __init__(self, loc: str, postal_code: str):
        self.postal_code = postal_code
        super().__init__(loc)

    def type(self) -> str:
        return "invalid_postal_code"

    def passes(self) -> bool:
        return re.match(r"\b(?!(\d)\1{3})[13-9]{4}[1346-9][013-9]{5}\b", self.postal_code) is not None



class PasswordStrentghCheck(AbstractValidator):
    policy = PasswordPolicy.from_names(
    length=8,  # min length
    uppercase=1,  # need 1 uppercase letters
    numbers=1,  # need 2 digits
    special=0,  # need 2 special characters
)
    def __init__(self, loc: str, password: str):
        self.password = password
        super().__init__(loc)

    def type(self) -> str:
        return "password_too_weak"
    
    def passes(self) -> bool:
        errors = self.policy.test(self.password)
        if errors:
            error_messages = [str(error) for error in errors]
            return False, error_messages
        return True, []




