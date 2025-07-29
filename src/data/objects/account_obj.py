from src.data.enums import CountryDialCode, DepositAmount
from src.data.objects.base_obj import BaseObj
from src.utils.random_utils import random_username, random_email, random_phone_number, random_invalid_email, \
    random_number_by_length


class ObjDemoAccount(BaseObj):
    """A class representing a demo account with user information.

    Attributes:
        name (str): The username of the account
        email (str): The email address of the account
        dial_code (CountryDialCode): The country dial code for phone number
        phone_number (str): The phone number of the account
        deposit (DepositAmount): The deposit amount for the account
        agreement (bool): Whether the user has agreed to terms
    """

    def __init__(
            self,
            name: str = None,
            email: str = None,
            dial_code: CountryDialCode = None,
            phone_number: str = None,
            deposit: DepositAmount = None,
            agreement: bool = True,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.dial_code = dial_code
        self.phone_number = phone_number
        self.deposit = deposit
        self.agreement = agreement

    def full_params(self, **kwargs):
        self.name = self.name or "MT5 Automation"
        self.email = self.email or random_email()
        self.dial_code = self.dial_code or CountryDialCode.sample_values()
        self.phone_number = self.phone_number or random_phone_number(self.dial_code)
        self.deposit = self.deposit or DepositAmount.FIVE_MILLION
        self.agreement = self.agreement or True
        return self._update_attributes(**kwargs)

    def invalid_format(self, **kwargs):
        self.full_params(**kwargs)
        self.email = random_invalid_email()
        self.phone_number = random_number_by_length()
        return self._update_attributes(**kwargs)
