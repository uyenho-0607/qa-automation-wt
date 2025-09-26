import random
import time

import pytest

from src.data.objects.account_obj import ObjDemoAccount
from src.page_object.android.components.modals.demo_acc_modals import DemoAccountModal
from src.utils.logging_utils import logger
from src.utils.random_utils import random_invalid_email, random_number_by_length

pytestmark = [pytest.mark.not_live, pytest.mark.not_crm]


def test_missing_all_required_fields(android):
    account_info = ObjDemoAccount(agreement=False)
    validation_fields = list(DemoAccountModal.validation_fields.values())

    logger.info("Step 1: Open demo account modal")
    android.login_screen.select_open_demo_account()

    logger.info(f"Step 2: Submit demo account creation form without input any field")
    time.sleep(1)  # wait a bit for loading deposit value
    android.login_screen.demo_account_modal.fill_demo_account_creation_form(account_info)
    android.login_screen.demo_account_modal.tap_agree_and_continue()

    logger.info(f"Verify validation error messages for fields: {validation_fields!r}")
    android.login_screen.demo_account_modal.verify_field_validation(fields=validation_fields)


def test_invalid_email_and_phone_number_format(android):
    account_info = ObjDemoAccount().invalid_format()
    validation_fields = [DemoAccountModal.validation_fields.email, DemoAccountModal.validation_fields.phone_number]

    logger.info("Step 1: Open demo account modal")
    android.login_screen.select_open_demo_account()

    logger.info(f"Step 2: Submit demo account creation form without invalid email and phone number format")
    time.sleep(1)  # wait a bit for loading deposit value
    android.login_screen.demo_account_modal.fill_demo_account_creation_form(account_info)
    android.login_screen.demo_account_modal.tap_agree_and_continue()

    logger.info(f"Verify validation error messages for fields: {validation_fields!r}")
    android.login_screen.demo_account_modal.verify_field_validation(fields=validation_fields, validation_type="invalid")


@pytest.mark.parametrize("missing_field", random.choices(list(DemoAccountModal.validation_fields.keys())))
def test_single_missing_field(android, missing_field):
    account_info = ObjDemoAccount().full_params()
    account_info[missing_field] = None

    logger.info("Step 1: Open demo account modal")
    android.login_screen.select_open_demo_account()

    logger.info(f"Step 3: Submit demo account creation form without input field: {missing_field!r}")
    time.sleep(1)
    android.login_screen.demo_account_modal.fill_demo_account_creation_form(account_info)

    logger.info(f"Verify validation message for missing {missing_field}")
    android.login_screen.demo_account_modal.verify_field_validation(fields=[missing_field])
