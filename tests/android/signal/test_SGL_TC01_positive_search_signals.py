import random

import pytest

from src.apis.api_client import APIClient
from src.utils.logging_utils import logger


def test(android, get_search_signal):
    signal, wildcard = get_search_signal

    logger.info(f"Step 1: Search with exact text: {signal!r}")
    android.signal_screen.search_signal(signal)

    logger.info(f"Verify search result is exact matches {signal!r}")
    android.signal_screen.verify_search_result(signal, check_contains=True)

    logger.info(f"Step 2: Search with wildcard text: {wildcard!r}")
    android.signal_screen.search_signal(wildcard)

    logger.info(f"Verify search result wildcard matches {wildcard!r}")
    android.signal_screen.verify_search_result(wildcard, check_contains=True)


@pytest.fixture(scope="function")
def get_search_signal(android):
    # Get the product subscription
    subscription = APIClient().config.get_product_subscription()

    if subscription != "PREMIUM":
        pytest.skip("Skipping test: Search box not present for Freemium subscription")

    # Get random signal from available signals
    available_signals = android.signal_screen.get_current_symbols()
    signal = random.choice(available_signals)
    wildcard = signal[:random.randint(2, len(signal) - 2)]

    return signal, wildcard
