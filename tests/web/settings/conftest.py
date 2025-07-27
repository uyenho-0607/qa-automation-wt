import pytest


@pytest.fixture(scope="package", autouse=True)
def setup(login_member_site):
    pass
