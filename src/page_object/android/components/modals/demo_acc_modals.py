from typing import List, Literal

from appium.webdriver.common.appiumby import AppiumBy

from src.core.actions.mobile_actions import MobileActions
from src.data.enums import SettingOptions, CountryDialCode, DepositAmount
from src.data.objects.account_obj import ObjDemoAccount
from src.data.ui_messages import UIMessages
from src.page_object.android.base_screen import BaseScreen
from src.utils import DotDict
from src.utils.assert_utils import soft_assert
from src.utils.common_utils import cook_element
from src.utils.format_utils import locator_format, format_str_price
from src.utils.logging_utils import logger


class DemoAccountModal(BaseScreen):
    validation_fields = DotDict(
        name="name",
        email="email",
        dial_code="dial code",
        phone_number="phone number"
    )

    def __init__(self, actions: MobileActions):
        super().__init__(actions)

    # ------------------------ LOCATORS ------------------------ #
    __opt_setting = (AppiumBy.ID, 'setting-option-{}')

    # ======================== DEMO ACCOUNT CREATION LOCATORS ======================== #
    __txt_name = (AppiumBy.ID, 'demo-account-creation-modal-name')
    __txt_email = (AppiumBy.ID, 'demo-account-creation-modal-email')

    __drp_country_dial_code = (AppiumBy.ID, 'demo-account-creation-modal-dial-code')
    __txt_country_search = (AppiumBy.ID, 'country-dial-code-search')
    __item_country_dial_code = (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("country-dial-code-item").descriptionContains("(+{})")')
    __txt_phone_number = (AppiumBy.ID, 'demo-account-creation-modal-phone')
    __deposit = (AppiumBy.ID, 'demo-account-creation-modal-deposit')
    __item_deposit = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("deposit-dropdown-item").description("{}")')
    __btn_agree_and_continue = (AppiumBy.ID, 'demo-account-creation-modal-confirm')
    __field_validation = (AppiumBy.ID, 'input-field-validation')

    # Actions
    def input_name(self, name: str):
        self.actions.send_keys(self.__txt_name, name)

    def input_email(self, email: str):
        self.actions.send_keys(self.__txt_email, email)

    def select_dial_code(self, dial_code: CountryDialCode):
        logger.debug(f"- Dial Code: {dial_code!r}")
        self.actions.click(self.__drp_country_dial_code)
        self.actions.send_keys(self.__txt_country_search, dial_code.name.replace("_", " ").title())
        self.actions.click(cook_element(self.__item_country_dial_code, dial_code))

    def input_phone_number(self, phone_number: int | str = None):
        logger.debug(f"- Phone number: {phone_number!r}")
        self.actions.send_keys(self.__txt_phone_number, str(phone_number))

    def select_deposit(self, deposit: DepositAmount = None, use_default=False):
        if use_default:
            return

        if deposit:
            self.actions.click(self.__deposit)
            self.actions.click(cook_element(self.__item_deposit, format_str_price(deposit, 0)))

    def tap_agree_and_continue(self):
        self.actions.click(self.__btn_agree_and_continue)

    def fill_demo_account_creation_form(self, account_info: ObjDemoAccount, default_deposit=False):
        if account_info.name:
            self.input_name(account_info.name)

        if account_info.email:
            self.input_email(account_info.email)

        if account_info.dial_code:
            self.select_dial_code(account_info.dial_code)

        if account_info.phone_number:
            self.input_phone_number(account_info.phone_number)

        self.select_deposit(account_info.deposit, use_default=default_deposit)

        if account_info.agreement:
            self.tap_agree_and_continue()

    # Verify
    def verify_field_validation(
            self,
            fields: List[str],
            validation_type: Literal["required", "invalid"] = "required"
    ):
        """
        Verify error messages for form fields.
        Args:
            fields: List of field names to verify - ["name", "email", "phone number", "dial code", "agreement"]
            validation_type: Type of validation to verify ("required" or "invalid")
        """
        # Validate input fields
        valid_fields = (
            self.validation_fields.values() if validation_type == "required"
            else [self.validation_fields.email, self.validation_fields.phone_number]
        )

        fields = [" ".join(field.split("_")) for field in fields]
        invalid_fields = [field for field in fields if field not in valid_fields]
        if invalid_fields:
            raise ValueError(f"Invalid fields: {invalid_fields}. Must be one of {valid_fields}")

        # Build expected error messages
        error_list = []
        if validation_type == "required":
            error_list.extend(UIMessages.IS_REQUIRED.format(field.capitalize()) for field in fields)

        else:
            error_dict = {
                self.validation_fields.email: UIMessages.EMAIL_FORMAT_INVALID,
                self.validation_fields.phone_number: UIMessages.PHONE_NUMBER_INVALID
            }
            error_list = [error_dict[field] for field in fields]

        # Get actual error messages
        error_messages = [element.text.strip() for element in self.actions.find_elements(self.__field_validation)]

        # Verify expected errors are present
        for expected_error in error_list:
            logger.debug(f"Check value: {expected_error!r}")
            soft_assert(
                expected_error in error_messages, True,
                error_message=f"Expected error message {expected_error!r} not found in {error_messages!r}"
            )

        # Verify no unexpected errors
        logger.debug("Checking for unexpected error messages")
        soft_assert(
            len(error_messages) == len(error_list), True,
            error_message=f"Redundant errors: {[item for item in error_messages if item not in error_list]}"
        )


    # ======================== DEMO ACCOUNT COMPLETION ======================== #
    # Locators
    __demo_acc_completion_title = (AppiumBy.ID, 'demo-account-completion-modal-title')
    __demo_acc_userid = (AppiumBy.XPATH, "//*[@resource-id='demo-completion-value'][1]")
    __demo_acc_password = (AppiumBy.XPATH, "//*[@resource-id='demo-completion-value'][2]")
    __demo_acc_name = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Name']/following-sibling::*[@resource-id='demo-completion-value'][1]"
    )
    __btn_sign_in_demo_acc_completion = (AppiumBy.ID, 'demo-completion-sign-in')
    __btn_switch_to_demo_acc = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("SWITCH TO DEMO ACCOUNT")')
    __btn_demo_acc_completion_done = (AppiumBy.ID, 'demo-completion-done')

    # Actions
    def get_account_details(self) -> DotDict:
        """
        Gets the demo account details from the completion modal.
        Returns:
            dict: Dictionary containing userid, name, and deposit
        """
        return DotDict(
            userid=self.actions.get_text(self.__demo_acc_userid),
            password=self.actions.get_text(self.__demo_acc_password),
            username=self.actions.get_text(self.__demo_acc_name),
        )

    def sign_in_from_completion(self):
        """Clicks the sign-in button on the demo account completion modal."""
        self.actions.click(self.__btn_sign_in_demo_acc_completion)

    def switch_to_demo_account(self):
        self.actions.click(self.__btn_switch_to_demo_acc)

    def demo_creation_done(self):
        self.actions.click(self.__btn_demo_acc_completion_done)
        self.actions.verify_element_displayed(cook_element(
            self.__opt_setting, locator_format(SettingOptions.OPEN_DEMO_ACCOUNT))
        )

    # Verify
    def verify_ready_message(self):
        actual_message = self.actions.get_text(self.__demo_acc_completion_title)
        soft_assert(actual_message, UIMessages.DEMO_ACCOUNT_OPEN_SUCCESS)

    def verify_account_info(self, expected_username):
        actual_username = self.get_account_details().username
        soft_assert(actual_username, expected_username)
