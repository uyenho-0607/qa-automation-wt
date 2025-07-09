import pytest

from src.data.enums import Language
from src.utils.logging_utils import logger


def test(web):
    language = Language.sample_values()
    logger.info(f"Step: Change language to {language.capitalize()!r}")
    web.home_page.settings.change_language(language)

    logger.info(f"Verify language is changed to {language.capitalize()}")
    web.home_page.settings.verify_language_changed(language)


@pytest.fixture(autouse=True)
def cleanup(web):
    yield
    logger.info("- Change Language back to English")
    web.home_page.settings.change_language(Language.ENGLISH)
