from src.data.enums import BaseEnum


class AccountType(BaseEnum):
    """Enum representing different types of trading accounts."""
    DEMO = "demo"
    CRM = "crm"
    LIVE = "live"


class Language(BaseEnum):
    """Enum representing supported languages in the application."""
    ENGLISH = "English"
    SIMPLIFIED_CHINESE = "简体中文"
    TRADITIONAL_CHINESE = "繁体中文"
    THAILAND = "ภาษาไทย"
    VIETNAM = "Tiếng Việt"
    MELAYU = "Melayu"
    BAHASA_INDONESIA = "Bahasa Indonesia"
    JAPANESE = "Japanese"
    KOREAN = "Korean"


class CountryDialCode(BaseEnum):
    """Enum representing country dial codes for phone numbers."""
    SINGAPORE = 65
    UNITED_STATES = 1
    VIETNAM = 84
    CHINA = 86
    THAILAND = 66
    KOREA = 82


class DepositAmount(BaseEnum):
    THREE_THOUSAND = 3000
    FIVE_THOUSAND = 5000
    TEN_THOUSAND = 10000
    TWENTY_FIVE_THOUSAND = 25000
    FIFTY_THOUSAND = 50000
    ONE_HUNDRED_THOUSAND = 100000
    FIVE_HUNDRED_THOUSAND = 500000
    ONE_MILLION = 1000000
    FIVE_MILLION = 5000000
