import pytest


@pytest.fixture(scope="package", autouse=True)
def setup(login_wt_app):
    pass


@pytest.fixture(autouse=True, scope="package")
def disable_OCT(disable_OCT):
    pass
