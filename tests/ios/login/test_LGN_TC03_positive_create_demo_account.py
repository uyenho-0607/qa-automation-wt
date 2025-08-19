import random

import pytest

from src.data.enums import AccountType
from src.data.objects.account_obj import ObjDemoAccount
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_live, pytest.mark.not_crm]


def test(ios):
    account_info = ObjDemoAccount().full_params()
    use_default_deposit = random.randint(0, 1)

    logger.info("Step 1: Open demo account modal")
    ios.login_screen.click_open_demo_account()

    logger.info("Step 2: Fill in demo account details")
    ios.login_screen.demo_account_modal.fill_demo_account_creation_form(account_info,
                                                                        default_deposit=use_default_deposit)

    logger.info("Verify demo account ready message")
    ios.login_screen.demo_account_modal.verify_ready_message()

    logger.info("Verify demo account username is correct")
    ios.login_screen.demo_account_modal.verify_account_info(account_info.name)
    # save userid and password for validation
    user_id, password, *_ = ios.login_screen.demo_account_modal.get_account_details().values()

    logger.info("Step 3: Click Sign in button")
    ios.login_screen.demo_account_modal.sign_in_from_completion()

    logger.info("Verify autofill values of account ID and password is correct")
    ios.login_screen.verify_account_autofill_value(user_id, password)

    logger.info("Step 4: Click Sign in button")
    ios.login_screen.click_sign_in()

    logger.info("Verify login successfully")
    ios.home_screen.feature_anm_modal.got_it()
    ios.home_screen.verify_account_info_displayed()