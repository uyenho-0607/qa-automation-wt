from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self):
        return self.value  # Automatically return .value when converted to a string


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API ENVIRONMENT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class API_Environment(BaseEnum):
    MT4_SIT = "https://lirunex-mb.webtrader-sit.s20ip12.com/api/trade/v2/market"
    MT4_UAT = "https://lirunex-mb.webtrader-uat.s20ip12.com/api/trade/v2/market"
    

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SERVER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class Server(BaseEnum):
    MT4 = "MT4"
    MT5 = "MT5"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PLATFORM
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class Platform(BaseEnum):
    DESKTOP = "Desktop"
    MOBILE = "Mobile"
    BACKOFFICE = "Backoffice"
    ROOTADMIN = "RootAdmin"
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLIENT NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class ClientName(BaseEnum):
    LIRUNEX = "Lirunex"
    TRANSACTCLOUDMT5 = "Transactcloudmt5"
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ENVIRONMENT TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
    
class EnvironmentType(BaseEnum):
    RELEASE_SIT = "Release_SIT"
    UAT = "UAT"
    SIT = "SIT"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOGIN RESULT STATUS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class AlertType(BaseEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    NO_ALERT = "no_alert"
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ACCOUNT TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class AccountType(BaseEnum):
    CRM = "crm"
    LIVE = "live"
    DEMO = "demo"
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CREDENTIAL TYPE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class CredentialType(BaseEnum):
    INVESTOR_ACCOUNT = "investor_account"
    READ_ONLY_ACCESS = "read_only_access"
    TOGGLE_REMEMBER_ME = "toggle_remember_me"
    CRM_CREDENTIAL = "crm_credential"
    DEFAULT = "credential"
    DEMO_CREDENTIAL = "demo_credential"
    INVALID_CREDENTIAL = "invalid_credential"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LANGUAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
    

class LoginLanguageMap(Enum):
    ENGLISH = ("English", "Sign in")
    CHINESE_SIMPLIFIED = ("简体中文", "登录")
    CHINESE_TRADITIONAL = ("繁体中文", "登錄")
    THAI = ("ภาษาไทย", "เปิดบัญชีซื้อขายจริง")
    VIETNAMESE = ("Tiếng Việt", "Đăng nhập")
    MELAYU = ("Melayu", "Log masuk")
    INDONESIAN = ("Bahasa Indonesia", "Masuk")
    JAPANESE = ("Japanese", "ログイン")
    KOREAN = ("Korean", "로그인")

    @classmethod
    def get_expected_text(cls, language: str):
        for lang in cls:
            if lang.value[0] == language:
                return lang.value[1]
        return None  # Return None if the language is not found


class SettingLanguageMap(Enum):
    ENGLISH = ("English", "Trade")
    CHINESE_SIMPLIFIED = ("简体中文", "交易")
    CHINESE_TRADITIONAL = ("繁体中文", "交易")
    THAI = ("ภาษาไทย", "เทรด")
    VIETNAMESE = ("Tiếng Việt", "Giao dịch")
    MALAY = ("Melayu", "Perdagangan")
    INDONESIAN = ("Bahasa Indonesia", "Berdagang")
    JAPANESE = ("Japanese", "取引")
    KOREAN = ("Korean", "거래")
    ARABIC = ("Arabic", "التداول.")

    @classmethod
    def get_expected_text(cls, language: str):
        for lang in cls:
            if lang.value[0] == language:
                return lang.value[1]
        return None  # Return None if the language is not found



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MENU
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class Menu(BaseEnum):
    HOME = "home"
    MARKET = "market"
    TRADE = "trade"
    INFO = "info"
    SIGNAL = "signal"
    NEWS = "news"
    ASSETS = "assets"
    DEALER = "dealer"
    EDUCATION = "education"
    COPY_TRADE = "copy-trade"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ANNOUNCEMENT MODAL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class AnnouncementModal(BaseEnum):
    GOT_IT = "got-it"
    TRY_IT = "try-it"
    MEDIA_LEFT = "media-left"
    MEDIA_RIGHT = "media-right"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SYMBOLS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class SymbolsList(BaseEnum):
    SYMBOLS = "Symbols"
    SYMBOLS_PRICE = "Symbols_Price"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PLACING WINDOW
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class ModuleType(BaseEnum):
    TRADE = "trade"
    EDIT = "edit"
    CLOSE = "close"
    DELETE = "delete"
    ONE_CLICK_TRADING = "oct"
    SPECIFICATION = "specification"

class TradeType(BaseEnum):
    BUY = "buy"
    SELL = "sell"

class TradeOption(BaseEnum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop-limit"
    
    
class SLTPType(BaseEnum):
    POINTS = "points"
    PRICE = "price"


class ExpiryType(BaseEnum):
    GOOD_TILL_CANCELLED = "good-till-cancelled"
    GOOD_TILL_DAY = "good-till-day"
    SPECIFIED_DATE = "specified-date"
    SPECIFIED_DATE_AND_TIME = "specified-date-and-time"


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

class OrderPanel(BaseEnum):
    OPEN_POSITIONS = "open-positions"
    PENDING_ORDERS = "pending-orders"
    HISTORY = "history"
    POSITION_HISTORY = "positions-history"
    ORDER_AND_DEALS = "orders-and-deals"


# Bulk related functions    
class BulkActionType(BaseEnum):
    BULK_CLOSE = "bulk-close"
    BULK_DELETE = "bulk-delete"
    ALL = "all"
    PROFIT = "profit"
    LOSS = "loss"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

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
    CONTACT_INFORMATION = "contact-information"
    HELP_SUPPORT = "help-support"
    LOGOUT = "logout"