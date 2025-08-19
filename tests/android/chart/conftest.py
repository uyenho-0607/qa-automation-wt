import pytest


@pytest.fixture(scope="package", autouse=True)
def setup(login_wt_app):
    pass
