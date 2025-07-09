import random
import pytest
from src.utils.logging_utils import logger


def test(web, get_search_signal):
    signal = get_search_signal
    wildcard = signal[:random.randint(2, len(signal) - 2)]

    logger.info(f"Step 1: Search with text: {signal!r}")
    web.signal_page.search_signal(signal)

    logger.info(f"Verify search result matches {signal!r}")
    web.signal_page.verify_search_result(signal, check_contains=True)

    logger.info(f"Step 1: Search with text: {wildcard!r}")
    web.signal_page.search_signal(wildcard)

    logger.info(f"Verify search result matches {wildcard!r}")
    web.signal_page.verify_search_result(wildcard, check_contains=True)


@pytest.fixture
def get_search_signal(web):
    available_signals = web.signal_page.get_current_symbols()
    yield random.choice(available_signals)
