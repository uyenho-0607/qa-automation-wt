import pytest

from src.data.enums import Language
from src.utils.logging_utils import logger


def test(android):
    language = Language.sample_values()
    logger.info(f"Step: Change language to {language.capitalize()!r}")
    android.home_screen.settings.change_language(language)

    logger.info(f"Verify language is changed to {language.capitalize()}")
    android.home_screen.settings.verify_language_changed(language)


@pytest.fixture(autouse=True)
def cleanup(android):
    yield
    logger.info("[Cleanup] Change Language back to English")
    android.home_screen.settings.change_language(Language.ENGLISH)