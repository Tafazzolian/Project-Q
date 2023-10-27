from abc import ABC, abstractmethod
from fastapi.exceptions import ValidationException

class AbstractValidator(ABC):

    def __init__(self, loc: str) -> None:
        self._loc = loc

    @abstractmethod
    def type(self) -> str:
        pass

    def message(self) -> str:
        return f"validation.{self.type()}"

    @abstractmethod
    def passes(self) -> bool:
        pass

    def validate(self) -> None:
        if not self.passes():
            raise ValidationException(message=self.message(), location=self._loc, type_=self.type())
