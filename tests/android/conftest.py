import pytest


@pytest.fixture
def cancel_delete_order(android):
    yield
    android.trade_screen.modals.cancel_delete_order()


@pytest.fixture
def cancel_bulk_delete(android):
    yield
    android.trade_screen.modals.cancel_bulk_delete()


@pytest.fixture
def cancel_bulk_close(android):
    yield
    android.trade_screen.modals.cancel_bulk_close()


@pytest.fixture
def cancel_edit_order(android):
    yield
    android.trade_screen.modals.cancel_edit_order()
