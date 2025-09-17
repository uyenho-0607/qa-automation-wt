import pytest


@pytest.fixture(autouse=True, scope="package")
def setup_oct_test(enable_OCT, swap_to_volume):
    pass