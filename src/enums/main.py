from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value  # Automatically return .value when converted to a string


class Server(BaseEnum):
    MT4 = "MT4"
    MT5 = "MT5"
    
    
class EnvironmentType(BaseEnum):
    RELEASE_SIT = "Release_SIT"
    UAT = "UAT"
    SIT = "SIT"


class LoginResultState(BaseEnum):
    SUCCESS = "success"
    FAILURE = "failure"


class AccountType(BaseEnum):
    CRM = "crm"
    LIVE = "live"
    DEMO = "demo"


class CredentialType(BaseEnum):
    INVESTOR_ACCOUNT = "investor_account"
    READ_ONLY_ACCESS = "read_only_access"
    TOGGLE_REMEMBER_ME = "toggle_remember_me"
    CRM_CREDENTIAL = "crm_credential"
    DEFAULT = "credential"
    INVALID_CREDENTIAL = "invalid_credential"
    

class Menu(BaseEnum):
    HOME = "home"
    MARKET = "market"
    TRADE = "trade"
    INFO = "info"
    ASSETS = "assets"


class SymbolsList(BaseEnum):
    SYMBOLS = "Symbols"
    SYMBOLS_PRICE = "Symbols_Price"


class Setting(BaseEnum):
    SWITCH_TO_LIVE = "switch-to-live"
    SWITCH_TO_DEMO = "switch-to-demo"
    OPEN_DEMO_ACCOUNT = "open-demo-account"
    PAYMENT_METHOD = "payment-method"
    ONE_CLICK_TRADING = "one-click-trading"
    LANGUAGE = "language"
    APPEARANCE = "appearance"
    NOTIFICATION_SETTING = "notification-setting"
    CHANGE_PASSWORD = "change-password"
    LINKED_DEVICE = "linked-device"
    BIOMETRICS_SETTING = "biometrics-setting"
    REQUEST_CANCEL_ACCOUNT = "request-cancel-account"
    HELP_SUPPORT = "help-support"
    LOGOUT = "logout"
    
    
class API_Environment(BaseEnum):
    MT4_SIT = "https://lirunex-mb.webtrader-sit.s20ip12.com/api/trade/v2/market"
    MT4_UAT = "https://lirunex-mb.webtrader-uat.s20ip12.com/api/trade/v2/market"