from azbankintro import *


class BankService:

    def card_validator(card_number:str):
        try:
            card_validate(card_number)
            return True
        except CardValidationException:
            return False
        

    def shaba_validator(shaba_number:str):
        try:
            iban_validate(shaba_number)
            return True    
        except IBANValidationException:
            return False
        

    def bank_account_to_shaba(bank:str,account_number:str):
        s = bank if bank else 'BMI'
        bank_type = BankEnum(s)
        iban = IBAN.calculate_iban(bank_type, account_number)
        return iban.format('-') if iban.validate() else False