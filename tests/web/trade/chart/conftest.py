import pytest


@pytest.fixture
def teardown_test(web):
    yield
    web.trade_page.chart.toggle_chart(fullscreen=False, timeout=1)
