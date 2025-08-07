import pytest


@pytest.fixture(scope="package", autouse=True)
def enable_OCT(enabl_OCT):
    pass
