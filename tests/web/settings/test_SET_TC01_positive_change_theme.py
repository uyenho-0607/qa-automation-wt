from src.data.enums import ThemeOptions

from src.utils.logging_utils import logger


def test(web):
    theme = ThemeOptions.sample_values()
    logger.info(f"Step: Change theme to {theme.capitalize()!r}")
    web.home_page.settings.change_theme(theme)

    logger.info(f"Verify theme is changed to {theme.capitalize()!r}")
    web.home_page.settings.verify_theme_changed(theme)
