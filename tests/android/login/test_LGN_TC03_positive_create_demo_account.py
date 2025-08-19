import random

import pytest

from src.data.objects.account_obj import ObjDemoAccount
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_live, pytest.mark.not_crm]


def test(android):
    account_info = ObjDemoAccount().full_params()
    use_default_deposit = random.randint(0, 1)

    logger.info("Step 1: Open demo account modal")
    android.login_screen.click_open_demo_account()

    logger.info("Step 2: Fill in demo account details")
    android.login_screen.demo_account_modal.fill_demo_account_creation_form(account_info, default_deposit=use_default_deposit)

    logger.info("Verify demo account ready message")
    android.login_screen.demo_account_modal.verify_ready_message()

    logger.info("Verify demo account username is correct")
    android.login_screen.demo_account_modal.verify_account_info(account_info.name)
    # save userid and password for validation
    user_id, password, *_ = android.login_screen.demo_account_modal.get_account_details().values()

    logger.info("Step 3: Click Sign in button")
    android.login_screen.demo_account_modal.sign_in_from_completion()

    logger.info("Verify autofill values of account ID and password is correct")
    android.login_screen.verify_account_autofill_value(user_id, password)

    logger.info("Step 4: Click Sign in button")
    android.login_screen.click_sign_in()

    logger.info("Verify login successfully")
    android.home_screen.feature_anm_modal.got_it()
    android.home_screen.verify_account_info_displayed()
