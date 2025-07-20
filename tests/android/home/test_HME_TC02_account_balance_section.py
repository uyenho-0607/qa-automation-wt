import pytest

from src.utils.logging_utils import logger


def test(android, teardown):
    logger.info("Step 1: Open My Account modal")
    android.home_screen.open_my_account()

    logger.info("Step 2: Close Balance section")
    android.home_screen.my_account_modal.toggle_balance(open=False)

    logger.info("Verify Balance section is closed")
    android.home_screen.my_account_modal.verify_balance_items_displayed(is_display=False)

    logger.info("Step 3: Open Balance section")
    android.home_screen.my_account_modal.toggle_balance(open=True)

    logger.info("Verify Balance section is opened")
    android.home_screen.my_account_modal.verify_balance_items_displayed(is_display=True)

    logger.info("Step 4: Close Notes section")
    android.home_screen.my_account_modal.toggle_note(open=False)

    logger.info("Verify Balance section is closed")
    android.home_screen.my_account_modal.verify_note_items_displayed(is_display=False)

    logger.info("Step 5: Open Notes section")
    android.home_screen.my_account_modal.toggle_note(open=True)

    logger.info("Verify Balance section is closed")
    android.home_screen.my_account_modal.verify_note_items_displayed(is_display=True)


@pytest.fixture
def teardown(android):
    yield
    logger.info("- Close My Account modal")
    android.home_screen.my_account_modal.close()
