import random

import pytest

from src.data.objects.account_object import ObjectDemoAccount
from src.page_object.web.components.modals.demo_account_modals import DemoAccountModal
from src.utils.logging_utils import logger

pytestmark = [pytest.mark.not_live, pytest.mark.not_crm]


def test_missing_all_required_fields(web):
    account_info = ObjectDemoAccount(agreement=False)
    validation_fields = list(DemoAccountModal.validation_fields.values())

    logger.info("Step 1: Open demo account modal")
    web.login_page.click_open_demo_account()

    logger.info(f"Step 2: Submit demo account creation form without input any field")
    web.login_page.demo_account_modal.fill_demo_account_creation_form(account_info)

    logger.info(f"Verify validation error messages for fields: {validation_fields!r}")
    web.login_page.demo_account_modal.verify_field_validation(fields=validation_fields)


def test_invalid_email_and_phone_number_format(web):
    account_info = ObjectDemoAccount().invalid_format()
    validation_fields = [DemoAccountModal.validation_fields.email, DemoAccountModal.validation_fields.phone_number]

    logger.info("Step 1: Open demo account modal")
    web.login_page.click_open_demo_account()

    logger.info(f"Step 2: Submit demo account creation form without invalid email and phone number format")
    web.login_page.demo_account_modal.fill_demo_account_creation_form(account_info)

    logger.info(f"Verify validation error messages for fields: {validation_fields!r}")
    web.login_page.demo_account_modal.verify_field_validation(fields=validation_fields, validation_type="invalid")


@pytest.mark.parametrize("missing_field", random.choices(list(DemoAccountModal.validation_fields.keys())))
def test_single_missing_field(web, missing_field):
    account_info = ObjectDemoAccount().full_params()
    account_info[missing_field] = None

    logger.info("Step 1: Open demo account modal")
    web.login_page.click_open_demo_account()

    logger.info(f"Step 3: Submit demo account creation form without input field: {missing_field!r}")
    web.login_page.demo_account_modal.fill_demo_account_creation_form(account_info)

    logger.info(f"Verify validation message for missing {missing_field}")
    web.login_page.demo_account_modal.verify_field_validation(fields=[missing_field])
