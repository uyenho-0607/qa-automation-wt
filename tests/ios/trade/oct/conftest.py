import pytest


@pytest.fixture(scope="package", autouse=True)
def setup_enable_OCT(enable_OCT):
    pass
