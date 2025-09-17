import pytest

from src.apis.api_client import APIClient


@pytest.fixture(autouse=True, scope="package")
def disable_OCT():
    # todo: update use UI toggle
    APIClient().user.patch_oct(enable=False)
