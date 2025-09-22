import pytest


@pytest.fixture(scope="package", autouse=True)
def setup_disable_OCT(disable_OCT):
    pass