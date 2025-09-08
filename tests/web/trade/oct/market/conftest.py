import pytest

from src.data.enums import AssetTabs


@pytest.fixture(autouse=True, scope="package")
def select_open_positions_tab(web):
    web.trade_page.asset_tab.select_tab(AssetTabs.OPEN_POSITION)
