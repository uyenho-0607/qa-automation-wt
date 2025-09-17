import pytest


@pytest.fixture(scope="package", autouse=True)
def setup_markets_test(ios, login_wt_app):
    pass
