import pytest


@pytest.fixture(scope="package", autouse=True)
def disable_OCT(disable_OCT):
    pass
