import pytest

from src.apis.api_client import APIClient
from src.core.driver.driver_manager import DriverManager
from src.core.page_container.web_app_container import WebAppContainer
from src.utils.logging_utils import logger


@pytest.fixture(scope="package")
def web_app():
    logger.info("- Init Web Driver")
    DriverManager.get_driver()

    yield WebAppContainer()

    logger.info("- Clean up Web Driver")
    DriverManager.quit_driver()


@pytest.fixture(scope="package")
def login_member_site(web_app):
    logger.info("- Navigate to WT Member Site")
    web_app.login_page.goto()
    web_app.login_page.wait_for_spin_loader(timeout=5)

    logger.info("- Login to Member Site")
    web_app.login_page.login(wait=True)
    web_app.home_page.feature_anm_modal.got_it(timeout=3)

    # Fall back
    if not web_app.home_page.is_logged_in():

        logger.info("- Retry login")
        web_app.login_page.login(wait=True)
        web_app.home_page.feature_anm_modal.got_it(timeout=3)



@pytest.fixture(scope="package")
def disable_OCT():
    logger.info("- Check and disable OCT")
    APIClient().user.patch_oct(enable=False)


@pytest.fixture(scope="package")
def enable_OCT():
    logger.info("- Check and enable OCT")
    APIClient().user.patch_oct(enable=True)


# cleanup trade test
@pytest.fixture
def cancel_all(web_app):
    yield
    web_app.trade_page.click_cancel_btn()
