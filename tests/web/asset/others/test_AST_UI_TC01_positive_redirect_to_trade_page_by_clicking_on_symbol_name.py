import pytest

from src.data.enums import Features, AssetTabs
from src.utils.logging_utils import logger


@pytest.mark.parametrize("tab", AssetTabs.list_values())
def test(web, pre_setup_order, tab):
    table_type = pre_setup_order

    logger.info("Step 1: Navigate to Asset Page")
    web.home_page.navigate_to(Features.ASSETS)

    logger.info(f"Step 2: Select tab: {tab}")
    web.assets_page.asset_tab.select_tab(tab)

    logger.info("Step 3: Select latest item by symbol")
    web.assets_page.asset_tab.select_last_symbol(table_type)

    logger.info("Verify page is redirect to Trade/Home Page")
    web.trade_page.verify_page_url()
