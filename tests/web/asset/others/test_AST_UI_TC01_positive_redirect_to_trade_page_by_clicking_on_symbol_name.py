from src.data.enums import Features
from src.utils.logging_utils import logger


def test(web, pre_setup_order):
    table_type = pre_setup_order

    logger.info("Step 1: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info("Step 2: Select latest item by symbol")
    web.assets_page.asset_tab.select_last_symbol(table_type)

    logger.info("Verify page is redirect to Trade Page")
    web.trade_page.verify_page_url()
