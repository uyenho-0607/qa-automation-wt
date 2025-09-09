import pytest

from src.data.enums import AssetTabs


@pytest.fixture(autouse=True, scope="package")
def select_pending_order_tab(web, disable_OCT):
    web.trade_page.asset_tab.select_tab(AssetTabs.PENDING_ORDER)

