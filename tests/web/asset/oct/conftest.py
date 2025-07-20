import pytest

from src.apis.api_client import APIClient


@pytest.fixture(autouse=True, scope="package")
def enable_OCT():
    APIClient().user.patch_oct(enable=True)
