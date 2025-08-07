import pytest

from src.data.enums import WatchListTab


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site):
    pass


@pytest.fixture
def get_current_symbol(web):
    def _handler(tab: WatchListTab = WatchListTab.ALL):
        symbols = web.trade_page.watch_list.get_current_symbols(tab)
        return symbols

    return _handler
