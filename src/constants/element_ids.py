from enum import Enum

class DataTestID(Enum):
    
    IN_APP_BROWSER_URL_bar = '//android.widget.TextView[@resource-id="com.android.chrome:id/url_bar"]'
    IN_APP_BROWSER_CLOSE_BUTTON = '//android.widget.ImageButton[@content-desc="Close tab"]'
    APP_NAVIGATION_BACK_BUTTON = "navigation-back-button"
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    LOGIN PAGE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    # LOGIN PAGE
    APP_LOGIN_LOGO = '//android.widget.ImageView'
    ADS_SKIP_BUTTON = 'ads-skip-button' # SPLASH SCREEN SKIP
    LOGIN_ACCOUNT_TYPE = 'login-account-type'
    LOGIN_PASSWORD = 'login-password'
    APP_LOGIN_PASSWORD_UNMASKED = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup'
    LOGIN_SUBMIT = 'login-submit'
    LOGIN_USER_ID = 'login-user-id'
    ALERT_ERROR = 'alert-error'
    ALERT_SUCCESS = 'alert-success'
    LOGIN_ACCOUNT_SIGNUP = 'login-account-signup' # open a demo account button
    APP_OPEN_DEMO_ACCOUNT = '//android.widget.TextView[@text="Open a Demo Account"]'
    
    APP_RMB_ME_CHECKBOX = '//android.view.ViewGroup[contains(@content-desc, "Remember me")]/android.view.ViewGroup/android.widget.TextView'
    APP_RMB_ME_UNCHECKBOX = '//android.view.ViewGroup[contains(@content-desc, "Remember me")]/android.view.ViewGroup'
    TAB_LOGIN_ACCOUNT_TYPE_CRM = 'tab-login-account-type-crm'
    TAB_LOGIN_ACCOUNT_TYPE_LIVE = 'tab-login-account-type-live'
    TAB_LOGIN_ACCOUNT_TYPE_DEMO = 'tab-login-account-type-demo'
    
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    LOGIN PAGE -  FORGOT PASSWORD
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    # APP - FORGOT PASSWORD MODULE
    APP_FORGOT_PASSWORD = '//android.widget.TextView[@text="Forgot password?"]'
    APP_RESET_PASSWORD = '//android.widget.TextView[@text="Reset Password"]'
    APP_RESET_PASSWORD_EMAIL_ADDRESS = '//android.widget.EditText[@text="Enter your email address"]' # placeholder
    APP_RESET_PASSWORD_ACCOUNT_ID = '//android.widget.EditText[@text="Enter your account ID"]'
    APP_RESET_PASSWORD_SUBMIT = '//android.view.ViewGroup[@content-desc="Submit"]'
    APP_HELP_IS_ON_THE_WAY = '//android.widget.TextView[@text="Help is on the way!"]'
    APP_CONTACT_SUPPORT = '//android.widget.TextView[@text="Contact Support"]'
    APP_BACK_TO_LOGIN_SCREEN = '//android.widget.TextView[@text="Back to login screen"]'
    
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    LOGIN PAGE -  SIGN UP
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    APP_SIGN_UP = '//android.widget.TextView[@text="Sign up"]'
    APP_SIGN_UP_USERNAME = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText'
    APP_SIGN_UP_TITLE = '(//android.widget.ScrollView//android.widget.TextView)[6]'
    APP_SIGN_UP_TITLE_DROPDOWN = '//android.widget.ScrollView//android.view.ViewGroup//android.view.ViewGroup'
    APP_SIGN_UP_TITLE_CANCEL = '//android.widget.TextView[@text="Cancel"]'

    APP_SIGN_UP_FIRST_NAME = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.EditText'
    APP_SIGN_UP_LAST_NAME = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[5]/android.widget.EditText'
    APP_SIGN_UP_EMAIL = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[6]/android.widget.EditText'
    APP_SIGN_UP_PASSWORD = '//android.widget.EditText[@text="Password length between 6-20 characters"]'
    APP_SIGN_UP_COUNTRY_OF_RESIDENCE = '(//android.widget.ScrollView//android.view.ViewGroup)[13]'
    APP_SIGN_UP_COUNTRY_OF_RESIDENCE_TEXT = '//android.widget.TextView[@text="Country of Residence"]'
    APP_SIGN_UP_COUNTRY_OF_RESIDENCE_SEARCH = '//android.widget.EditText[@text="Search"]'
    APP_SIGN_UP_COUNTRY_OF_RESIDENCE_OPTIONS = '//android.widget.ScrollView//android.view.ViewGroup/android.view.ViewGroup'
    APP_SIGN_UP_PHONE_NUMBER = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup[9]/android.widget.EditText'
    APP_SIGN_UP_CHECKBOX = '//android.view.ViewGroup[contains(@content-desc, "I hereby acknowledge")]/android.view.ViewGroup'
    APP_SIGN_UP_PROCEED_KYC = '//android.widget.TextView[@text="Proceed to KYC"]'
        
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    LOGIN PAGE - LANGUAGE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    # LOGIN - LANGUAGE
    LANGUAGE_DROPDOWN = 'language-dropdown'
    LANGUAGE_OPTION = 'language-option'
    
    
    LANGUAGE_OPTION_APP = '//android.widget.ScrollView//android.view.ViewGroup'
    LANGUAGE_ENGLISH = '//android.view.ViewGroup[@content-desc="English"]'
    LANGUAGE_SIMPLIFIED_CHINESE = '//android.view.ViewGroup[@content-desc="简体中文"]'
    LANGUAGE_TRADICTIONAL_CHINESE = '//android.view.ViewGroup[@content-desc="繁体中文"]'
    LANGUAGE_THAILAND = '//android.view.ViewGroup[@content-desc="ภาษาไทย"]'
    LANGUAGE_VIET = '//android.view.ViewGroup[@content-desc="Tiếng Việt"]'
    LANGUAGE_MELAYU = '//android.view.ViewGroup[@content-desc="Melayu"]'
    LANGUAGE_INDONESIA = '//android.view.ViewGroup[@content-desc="Bahasa Indonesia"]'
    LANGUAGE_JAPANESE = '//android.view.ViewGroup[@content-desc="Japanese"]'
    LANGUAGE_KOREAN = '//android.view.ViewGroup[@content-desc="Korean"]'
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    LOGIN LANGUAGE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    FEATURE_ANNOUNCEMENT_MODAL = 'feature-announcement-modal'
    FEATURE_ANNOUNCEMENT_MODAL_GOT_IT_BUTTON = 'feature-announcement-modal-got-it-button'
    FEATURE_ANNOUNCEMENT_MODAL_TRY_IT_NOW_BUTTON = 'feature-announcement-modal-try-it-now-button'
    FEATURE_ANNOUNCEMENT_MODAL_MEDIA_LEFT_BUTTON = 'feature-announcement-modal-media-left-button'
    FEATURE_ANNOUNCEMENT_MODAL_MEDIA_RIGHT_BUTTON = 'feature-announcement-modal-media-right-button'

    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    MENU
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    # MENU
    SIDE_BAR_OPTION_TRADE = 'side-bar-option-trade'
    SIDE_BAR_OPTION_MARKETS = 'side-bar-option-markets'
    SIDE_BAR_OPTION_ASSETS = 'side-bar-option-assets'
    SIDE_BAR_OPTION_SIGNAL = 'side-bar-option-signal'
    SIDE_BAR_OPTION_NEWS = 'side-bar-option-news'
    SPIN_LOADER = 'spin-loader'
    
    
    APP_SIDE_BAR_OPTION_HOME = '//android.widget.TextView[@text="Home"]'
    APP_SIDE_BAR_OPTION_MARKET = '(//android.widget.TextView[@text="Markets"])[2]'
    APP_SIDE_BAR_OPTION_TRADE = '//android.widget.TextView[@text="Trade"]'
    APP_SIDE_BAR_OPTION_INFO = '//android.widget.TextView[@text="Info"]'
    APP_SIDE_BAR_OPTION_ASSETS = '//android.widget.TextView[@text="Assets"]'
        
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    MARKET
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    WATCHLIST_TABS = 'watchlist-tabs'
    WATCHLIST_LIST = 'watchlist-list'
    WATCHLIST_LIST_ITEM = 'watchlist-list-item'
    WATCHLIST_SYMBOL = 'watchlist-symbol'
    SYMBOL_PREFERENCE = 'symbol-preference'
    SYMBOL_PREFERENCE_LABEL = 'symbol-preference-label'
    SYMBOL_PREFERENCE_TABS = 'symbol-preference-tabs'
    SYMBOL_PREFERENCE_OPTION_UNCHECKED = 'symbol-preference-option-unchecked'
    SYMBOL_PREFERENCE_OPTION_CHECKED = 'symbol-preference-option-checked'
    SYMBOL_PREFERENCE_SAVE = 'symbol-preference-save'
    SYMBOL_PREFERENCE_CLOSE = 'symbol-preference-close'
    TAB_ALL = 'tab-all'
    TAB_FAVOURITES = 'tab-favourites'
    TAB_FOREX = 'tab-forex'
    TAB_COMMS = 'tab-comms'
    TAB_INDEX = 'tab-index'
    TAB_CRYPTO = 'tab-crypto'
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    SIGNAL
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    SIGNAL_FILTER_FAVOURITE = 'signal-filter-favourite'
    SIGNAL_FILTER_ALL = 'signal-filter-all'
    SIGNAL_LIST = 'signal-list'
    SIGNAL_ROW_SYMBOL = 'signal-row-symbol'
    SIGNAL_ROW_ORDER_STATUS = 'signal-row-order-status'
    ANALYSIS_ACTION_VALUE = 'analysis-action-value'
    COPY_TO_ORDER_ONE = 'copy-to-order-1'
    COPY_TO_ORDER_TWO = 'copy-to-order-2'
    CONFIRMATION_MODAL = 'confirmation-modal'
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    ORDER PANEL TABLE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    # ORDER PANEL TABLE
    ASSET_ORDER_TYPE = 'asset-order-type'
    TAB_ASSET_ORDER_TYPE_OPEN_POSITIONS = 'tab-asset-order-type-open-positions'
    TAB_ASSET_ORDER_TYPE_PENDING_ORDERS = 'tab-asset-order-type-pending-orders'
    TAB_ASSET_ORDER_TYPE_HISTORY = 'tab-asset-order-type-history'
    TAB_ASSET_ORDER_TYPE_HISTORY_POSITIONS_HISTORY = 'tab-asset-order-type-history-positions-history'
    TAB_ASSET_ORDER_TYPE_HISTORY_ORDERS_AND_DEALS = 'tab-asset-order-type-history-orders-and-deals'


    # ORDER HISTORY TABLE ID
    ASSET_HISTORY_POSITION_TABLE = 'asset-history-position-table'
    ASSET_HISTORY_ORDER_DEAL_TABLE = 'asset-history-order-deal-table'
    ASSET_HISTORY_POSITION_TABLE_HEADER = 'asset-history-position-table-header'
    ASSET_HISTORY_ORDER_DEAL_TABLE_HEADER = 'asset-history-order-deal-table-header'
    CALENDAR_BUTTON_ASSETS_CONTENT = 'calender-button-assets-content'
    ASSET_HISTORY_COLUMN_CLOSE_DATE = 'asset-history-column-close-date'
    ASSET_HISTORY_COLUMN_CLOSE_PRICE = 'asset-history-column-close-price'
    ASSET_HISTORY_COLUMN_COMMISSION = 'asset-history-column-commission'
    ASSET_HISTORY_COLUMN_ENTRY_PRICE = 'asset-history-column-entry-price'
    ASSET_HISTORY_COLUMN_OPEN_DATE = 'asset-history-column-open-date'
    ASSET_HISTORY_COLUMN_SYMBOL = 'asset-history-column-symbol'
    ASSET_HISTORY_COLUMN_ORDER_ID = 'asset-history-column-order-id'
    ASSET_HISTORY_COLUMN_ORDER_TYPE = 'asset-history-column-order-type'
    ASSET_HISTORY_COLUMN_PROFIT = 'asset-history-column-profit'
    ASSET_HISTORY_COLUMN_REMARKS = 'asset-history-column-remarks'
    ASSET_HISTORY_COLUMN_SIZE = 'asset-history-column-size'
    ASSET_HISTORY_COLUMN_STATUS = 'asset-history-column-status'
    ASSET_HISTORY_COLUMN_STOP_LOSS = 'asset-history-column-stop-loss'
    ASSET_HISTORY_COLUMN_SWAP = 'asset-history-column-swap'
    ASSET_HISTORY_COLUMN_TAKE_PROFIT = 'asset-history-column-take-profit'
    ASSET_HISTORY_COLUMN_UNITS = 'asset-history-column-units'


    # OPEN POSITION TABLE ID
    ASSET_OPEN_TABLE = 'asset-open-table'
    ASSET_OPEN_TABLE_HEADER = 'asset-open-table-header'
    ASSET_OPEN_BUTTON_CLOSE = 'asset-open-button-close'
    ASSET_OPEN_BUTTON_EDIT = 'asset-open-button-edit'
    ASSET_OPEN_BUTTON_TRACK = 'asset-open-button-track'
    ASSET_OPEN_COLUMN_COMMISSION = 'asset-open-column-commission'
    ASSET_OPEN_COLUMN_CURRENT_PRICE = 'asset-open-column-current-price'
    ASSET_OPEN_COLUMN_ENTRY_PRICE = 'asset-open-column-entry-price'
    ASSET_OPEN_COLUMN_OPEN_DATE = 'asset-open-column-open-date'
    ASSET_OPEN_COLUMN_COLUMN_SYMBOL = 'asset-open-column-symbol'
    ASSET_OPEN_COLUMN_ORDER_ID = 'asset-open-column-order-id'
    ASSET_OPEN_COLUMN_ORDER_TYPE = 'asset-open-column-order-type'
    ASSET_OPEN_COLUMN_PROFIT = 'asset-open-column-profit'
    ASSET_OPEN_COLUMN_STOP_LOSS = 'asset-open-column-stop-loss'
    ASSET_OPEN_COLUMN_SWAP = 'asset-open-column-swap'
    ASSET_OPEN_COLUMN_TAKE_PROFIT = 'asset-open-column-take-profit'
    ASSET_OPEN_COLUMN_UNITS = 'asset-open-column-units'
    ASSET_OPEN_COLUMN_VOLUME = 'asset-open-column-volume'
    ASSET_OPEN_LIST = 'asset-open-list'
    

    # PENDING ORDER TABLE ID
    ASSET_PENDING_TABLE = 'asset-pending-table'
    ASSET_OPENDING_TABLE_HEADER = 'asset-pending-table-header'
    ASSET_PENDING_BUTTON_CLOSE = 'asset-pending-button-close'
    ASSET_PENDING_BUTTON_EDIT = 'asset-pending-button-edit'
    ASSET_PENDING_BUTTON_TRACK = 'asset-pending-button-track'
    ASSET_PENDING_COLUMN_CURRENT_PRICE = 'asset-pending-column-current-price'
    ASSET_PENDING_COLUMN_ENTRY_PRICE = 'asset-pending-column-entry-price'
    ASSET_PENDING_COLUMN_EXPIRY = 'asset-pending-column-expiry'
    ASSET_PENDING_COLUMN_EXPIRY_DATE = 'asset-pending-column-expiry-date'
    ASSET_PENDING_COLUMN_FILL_POLICY = 'asset-pending-column-fill-policy'
    ASSET_PENDING_COLUMN_OPEN_DATE = 'asset-pending-column-open-date'
    ASSET_PENDING_COLUMN_SYMBOL = 'asset-pending-column-symbol'
    ASSET_PENDING_COLUMN_ORDER_ID = 'asset-pending-column-order-id'
    ASSET_PENDING_COLUMN_ORDER_TYPE = 'asset-pending-column-order-type'
    ASSET_PENDING_COLUMN_PENDING_PRICE = 'asset-pending-column-pending-price'
    ASSET_PENDING_COLUMN_STOP_LOSS = 'asset-pending-column-stop-loss'
    ASSET_PENDING_COLUMN_TAKE_PROFIT = 'asset-pending-column-take-profit'
    ASSET_PENDING_COLUMN_UNITS = 'asset-pending-column-units'
    ASSET_PENDING_COLUMN_VOLUME = 'asset-pending-column-volume'
    ASSET_PENDING_LIST = 'asset-pending-list'


    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    CHART
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    CHART_STAR_SYMBOL = 'chart-star-symbol'
    CHART_TRADE_BUTTON_CLOSE = 'chart-trade-button-close'
    CHART_TOGGLE_FULLSCREEN = 'chart-toggle-fullscreen'
    CHART_EXIT_FULLSCREEN ='chart-exit-fullscreen'
    
    # MAIN INDICATOR
    CHART_INDICATOR = 'chart_indicator'
    CHART_INDICATOR_MA = 'chart-indicator-ma'
    CHART_INDICATOR_SAR = 'chart-indicator-sar'
    CHART_INDICATOR_BOLL = 'chart-indicator-boll'
    CHART_INDICATOR_EMA = 'chart-indicator-ema'
    CHART_INDICATOR_WMA = 'chart-indicator-wma'
    
    #SUB INDICATOR
    CHART_INDICATOR_MACD = 'chart-indicator-macd'
    CHART_INDICATOR_CCI = 'chart-indicator-cci'
    CHART_INDICATOR_RSI = 'chart-indicator-rsi'
    CHART_INDICATOR_SD = 'chart-indicator-sd'
    CHART_INDICATOR_SO = 'chart-indicator-so'
    CHART_INDICATOR_ATR = 'chart-indicator-atr'
    
    # CHART SETTING
    DROPDOWN_CHART_SETTING = 'dropdown-chart-setting'
    DROPDOWN_CHART_SETTING_REMOVE_ALL_DRAWING = 'dropdown-chart-setting-remove-all-drawing'
    DROPDOWN_CHART_SETTING_REMOVE_ALL_INDICATORS = 'dropdown-chart-setting-remove-all-indicators'
    DROPDOWN_CHART_SETTING_REMOVE_ALL_INDICATORS_AND_DRAWING = 'dropdown-chart-setting-remove-all-indicators-and-drawings'
    DROPDOWN_CHART_SETTING_SHOW_ASK_PRICE_ON_Y_AXIS = 'dropdown-chart-setting-show-ask-price-on-y-axis'
    DROPDOWN_CHART_SETTING_CLEAR_ALL_TRACK_DETAILS = 'dropdown-chart-setting-clear-all-track-details'
    DROPDOWN_CHART_SETTING_RESET_CHART = 'dropdown-chart-setting-reset-chart'

    # SEARCH SYMBOL RELATED
    SYMBOL_SEARCH_SELECTOR = 'symbol-search-selector'
    SYMBOL_DROPDOWN_RESULT = 'symbol-dropdown-result'
    SYMBOL_INPUT_SEARCH = 'symbol-input-search'
    SYMBOL_OVERVIEW_ID = 'symbol-overview-id'
    SYMBOL_INPUT_SEARCH_ITEMS = 'symbol-input-search-items'
    SYMBOL_INPUT_SEARCH_HISTORY_DELETE = 'symbol-input-search-history-delete'
    SYMBOL_INPUT_SEARCH_ITEMS_DELETE = 'symbol-input-search-items-delete'
    SYMBOL_INPUT_SEARCH_ITEMS_SYMBOL = 'symbol-input-search-items-symbol'

    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    TRADE MODULE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    # Buy / Sell Price
    TRADE_LIVE_BUY_PRICE = 'trade-live-buy-price'
    TRADE_LIVE_SELL_PRICE = "trade-live-sell-price"
    
    # OCT BUTTON
    TOGGLE_OCT = 'toggle-oct'
    TOGGLE_OCT_CHECKED = 'toggle-oct-checked'
    OCT_MODAL_BUTTON_CONFIRM = 'oct-modal-button-confirm'

    #TRADING COMPONENT
    TAB_ONE_CLICK_TRADING = 'tab-one-click-trading'
    TAB_TRADE = 'tab-trade'
    TAB_SPECIFICATION = 'tab-specification'
    
    # SWAP TO UNITS
    TRADE_SWAP_TO_VOLUME = 'trade-swap-to-volume'
    TRADE_SWAP_TO_UNITS = 'trade-swap-to-units'
    TRADE_VOLUME_INFO_LABEL = 'trade-volume-info-label'
    TRADE_VOLUME_INFO_MIN_VALUE = 'trade-volume-info-min-value'
    
    # TRADE ORDER - BUY / SELL
    TRADE_BUTTON_ORDER_BUY = 'trade-button-order-buy'
    TRADE_BUTTON_ORDER_SELL = 'trade-button-order-sell'
    TRADE_BUTTON_OCT_ORDER_BUY = 'trade-button-oct-order-buy'
    TRADE_BUTTON_OCT_ORDER_SELL = 'trade-button-oct-order-sell'
    
    # ORDER TYPE SELECTION
    TRADE_DROPDOWN_ORDER_TYPE = 'trade-dropdown-order-type'
    TRADE_DROPDOWN_ORDER_TYPE_Market = 'trade-dropdown-order-type-market'
    TRADE_DROPDOWN_ORDER_TYPE_Limit = 'trade-dropdown-order-type-limit'
    TRADE_DROPDOWN_ORDER_TYPE_Stop = 'trade-dropdown-order-type-stop'
    
    # SIZE / VOLUME
    TRADE_INPUT_VOLUME = 'trade-input-volume'
    TRADE_INPUT_VOLUME_DECREASE = 'trade-input-volume-decrease'
    TRADE_INPUT_VOLUME_INCREASE = 'trade-input-volume-increase'
    
    # ONE POINT EQUAL LABEL
    TRADE_ONE_POINT_EQUAL_LABEL = 'trade-one-point-equal-label'
    
    # FILL POLICY
    TRADE_ORDER_DROPDOWN_FILL_POLICY = 'trade-order-dropdown-fill-policy'
    TRADE_DROPDOWN_FILL_POLICY_FILL_OR_KILL = 'trade-dropdown-fill-policy-fill-or-kill'
    TRADE_DROPDOWN_FILL_POLICY_IMMEDIATE_OR_CANCEL = 'trade-dropdown-fill-policy-immediate-or-cancel'
    TRADE_DROPDOWN_FILL_POLICY_RETURN = 'trade-dropdown-fill-policy-return'
    
    # PRICE
    TRADE_INPUT_PRICE = 'trade-input-price'
    TRADE_INPUT_PRICE_INCREASE = 'trade-input-price-increase'
    TRADE_INPUT_PRICE_DECREASE = 'trade-input-price-decrease'

    # PLACE TAKE PROFIT BY POINTS
    TRADE_INPUT_TAKEPROFIT_POINTS = 'trade-input-takeprofit-points'
    TRADE_INPUT_TAKEPROFIT_POINTS_DECREASE = 'trade-input-takeprofit-points-decrease'
    TRADE_INPUT_TAKEPROFIT_POINTS_INCREASE = 'trade-input-takeprofit-points-increase'
    
    # PLACE TAKE PROFIT BY PRICE
    TRADE_INPUT_TAKEPROFIT_PRICE = 'trade-input-takeprofit-price'
    TRADE_INPUT_TAKEPROFIT_PRICE_INCREASE = 'trade-input-takeprofit-price-increase'
    TRADE_INPUT_TAKEPROFIT_PRICE_DECREASE = 'trade-input-takeprofit-price-decrease'
    
    # PLACE STOP LOSS BY POINTS
    TRADE_INPUT_STOPLOSS_POINTS = 'trade-input-stoploss-points'
    TRADE_INPUT_STOPLOSS_POINTS_DECREASE = 'trade-input-stoploss-points-decrease'
    TRADE_INPUT_STOPLOSS_POINTS_INCREASE = 'trade-input-stoploss-points-increase'

    # PLACE STOP LOSS BY POINTS
    TRADE_INPUT_STOPLOSS_PRICE = 'trade-input-stoploss-price'
    TRADE_INPUT_STOPLOSS_PRICE_INCREASE = 'trade-input-stoploss-price-increase'
    TRADE_INPUT_STOPLOSS_PRICE_DECREASE = 'trade-input-stoploss-price-decrease'
    
    # EXPIRY
    TRADE_DROPDOWN_EXPIRY = 'trade-dropdown-expiry'
    TRADE_DROPDOWN_EXPIRY_GOOD_TILL_CANCELLED = 'trade-dropdown-expiry-good-till-cancelled'
    TRADE_DROPDOWN_EXPIRY_GOOD_TILL_DAY = 'trade-dropdown-expiry-good-till-day'
    TRADE_DROPDOWN_EXPIRY_SPECIFIED_DATE = 'trade-dropdown-expiry-specified-date'
    TRADE_DROPDOWN_EXPIRY_SPECIFIED_DATE_AND_TIME = 'trade-dropdown-expiry-specified-date-and-time'
    TRADE_DROPDOWN_EXPIRY_DATE = 'trade-input-expiry-date'
    TRADE_DROPDOWN_EXPIRY_TIME = 'trade-input-expiry-time'
    TRADE_DROPDOWN_EXPIRY_TIME_HOUR = 'trade-input-expiry-time-hour'
    TRADE_DROPDOWN_EXPIRY_TIME_MINUTE = 'trade-input-expiry-time-minute'
    
    # PLACE / UPDATE
    TRADE_BUTTON_ORDER = 'trade-button-order'
    
    # EDIT CONFIRMATION DIALOG
    TRADE_CONFIRMATION_DIALOG = 'trade-confirmation-modal'
    TRADE_CONFIRMATION_ORDER_TYPE = 'trade-confirmation-order-type'
    TRADE_CONFIRMATION_SYMBOL = 'trade-confirmation-symbol'
    TRADE_CONFIRMATION_LABEL = 'trade-confirmation-label'
    TRADE_CONFIRMATION_VALUE = 'trade-confirmation-value'
    TRADE_CONFIRMATION_BUTTON_CONFIRM = 'trade-confirmation-button-confirm'
    

    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    EDIT MODULE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    #EDIT MODULE LABEL
    EDIT_STATIC_ENTRY_PRICE = 'edit-static-entry-price'
    EDIT_STATIC_VOLUME = 'edit-static-volume'
    EDIT_SYMBOL_PRICE = 'edit-symbol-price'
    
    # ONE POINT EQUAL LABEL
    EDIT_ONE_POINT_EQUAL_LABEL = 'edit-one-point-equal-label'
    
    # EDIT SIZE / VOLUME + / - BUTTON
    EDIT_INPUT_VOLUME_DECREASE = 'edit-input-price-decrease'
    EDIT_INPUT_VOLUME_INCREASE = 'edit-input-price-increase'
    
    # MODIFY PRICE
    EDIT_INPUT_PRICE = 'edit-input-price'
    EDIT_INPUT_PRICE_INCREASE = 'edit-input-price-increase'
    EDIT_INPUT_PRICE_DECREASE = 'edit-input-price-decrease'

    # MODIFY STOP LOSS BY POINTS
    EDIT_INPUT_STOPLOSS_POINTS = 'edit-input-stoploss-points'
    EDIT_INPUT_STOPLOSS_POINTS_DECREASE = 'edit-input-stoploss-points-decrease'
    EDIT_INPUT_STOPLOSS_POINTS_INCREASE = 'edit-input-stoploss-points-increase'
    
    # MODIFY STOP LOSS BY PRICE
    EDIT_INPUT_STOPLOSS_PRICE = 'edit-input-stoploss-price'
    EDIT_INPUT_STOPLOSS_PRICE_INCREASE = 'edit-input-stoploss-price-increase'
    EDIT_INPUT_STOPLOSS_PRICE_DECREASE = 'edit-input-stoploss-price-decrease'
    
    # MODIFY TAKE PROFIT BY PRICE
    EDIT_INPUT_TAKEPROFIT_PRICE = 'edit-input-takeprofit-price'
    EDIT_INPUT_TAKEPROFIT_PRICE_DECREASE = 'edit-input-takeprofit-price-increase'
    EDIT_INPUT_TAKEPROFIT_PRICE_INCREASE = 'edit-input-takeprofit-price-decrease'
    
    # MODIFY TAKE PROFIT BY POINTS
    EDIT_INPUT_TAKEPROFIT_POINTS = 'edit-input-takeprofit-points'
    EDIT_INPUT_TAKEPROFIT_POINTS_DECREASE = 'edit-input-takeprofit-points-decrease'
    EDIT_INPUT_TAKEPROFIT_POINTS_INCREASE = 'edit-input-takeprofit-points-increase'
    
    # MODIFY EXPIRY
    EDIT_DROPDOWN_EXPIRY = 'edit-dropdown-expiry'
    EDIT_DROPDOWN_EXPIRY_GOOD_TILL_CANCELLED = 'edit-dropdown-expiry-good-till-cancelled'
    EDIT_DROPDOWN_EXPIRY_GOOD_TILL_DAY = 'edit-dropdown-expiry-good-till-day'
    EDIT_DROPDOWN_EXPIRY_SPECIFIED_DATE = 'edit-dropdown-expiry-specified-date'
    EDIT_DROPDOWN_EXPIRY_SPECIFIED_DATE_AND_TIME = 'edit-dropdown-expiry-specified-date-and-time'
    EDIT_DROPDOWN_EXPIRY_DATE = 'edit-input-expiry-date'
    EDIT_DROPDOWN_EXPIRY_TIME = 'edit-input-expiry-time'
    EDIT_DROPDOWN_EXPIRY_TIME_HOUR = 'edit-input-expiry-time-hour'
    EDIT_DROPDOWN_EXPIRY_TIME_MINUTE = 'edit-input-expiry-time-minute'

    # UPDATE BUTTON
    EDIT_BUTTON_ORDER = 'edit-button-order'
    
    # EDIT CONFIRMATION DIALOG
    EDIT_CONFIRMATION_DIALOG = 'edit-confirmation-modal'
    EDIT_CONFIRMATION_ORDER_ID = 'edit-confirmation-order-id'
    EDIT_CONFIRMATION_ORDER_TYPE = 'edit-confirmation-order-type'
    EDIT_CONFIRMATION_SYMBOL = 'edit-confirmation-symbol'
    EDIT_CONFIRMATION_LABEL = 'edit-confirmation-label'
    EDIT_CONFIRMATION_VALUE = 'edit-confirmation-value'
    EDIT_CONFIRMATION_BUTTON_CONFIRM = 'edit-confirmation-button-confirm'

    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    CLOSE MODULE
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    # CLOSE ORDER
    CLOSE_ORDER_INPUT_VOLUME = 'close-order-input-volume'
    'close-order-input-volume-max-value'
    CLOSE_ORDER_INPUT_VOLUME_STATIC_MIN = 'close-order-input-volume-static-min'
    CLOSE_ORDER_INPUT_VOLUME_STATIC_MAX = 'close-order-input-volume-static-max'
    CLOSE_ORDER_INPUT_VOLUME_DECREASE = 'close-order-input-volume-decrease'
    CLOSE_ORDER_INPUT_VOLUME_INCREASE = 'close-order-input-volume-increase'
    CLOSE_ORDER_DROPDOWN_FILL_POLICY = 'close-order-dropdown-fill-policy'
    CLOSE_ORDER_DROPDOWN_FILL_POLICY_FILL_OR_KILL = 'close-order-dropdown-fill-policy-fill-or-kill'
    CLOSE_ORDER_DROPDOWN_FILL_POLICY_IMMEDIATE_OR_CANCEL = 'close-order-dropdown-fill-policy-immediate-or-cancel'
    CLOSE_BUTTON_SUBMIT = 'close-button-submit'
    CLOSE_BUTTON_CANCEL = 'close-order-cancel'


    # BULK CLOSE MODULE
    BULK_CLOSE = 'bulk-close'
    BULK_DELETE = 'bulk-delete'
    
    # DEOP DOWN BULK CLOSE SELECTON
    DROPDOWN_BULK_CLOSE_ALL = 'dropdown-bulk-close-all'
    DROPDOWN_BULK_CLOSE_PROFIT = 'dropdown-bulk-close-profit'
    DROPDOWN_BULK_CLOSE_LOSS = 'dropdown-bulk-close-loss'
    
    # BULK CLOSE SUBMIT / CANCEL FOR ALL
    BULK_CLOSE_MODAL_BUTTON_CANCEL_ALL = 'bulk-close-modal-button-cancel-all'
    BULK_CLOSE_MODAL_BUTTON_SUBMIT_ALL = 'bulk-close-modal-button-submit-all'
    
    # BULK CLOSE SUBMIT / CANCEL FOR PROFIT
    BULK_CLOSE_MODAL_BUTTON_SUBMIT_PROFIT = 'bulk-close-modal-button-submit-profit'
    BULK_CLOSE_MODAL_BUTTON_CANCEL_PROFIT = 'bulk-close-modal-button-submit-profit'
    
    # BULK CLOSE SUBMIT / CANCEL FOR LOSS
    BULK_CLOSE_MODAL_BUTTON_SUBMIT_LOSS = 'bulk-close-modal-button-submit-loss'
    BULK_CLOSE_MODAL_BUTTON_CANCEL_LOSS = 'bulk-close-modal-button-cancel-loss'
    
    # BULK DELETE SUBMIT / CANCEL FOR ALL
    BULK_DELETE_MODAL_BUTTON_CANCEL = 'bulk-delete-modal-button-cancel'
    BULK_DELETE_MODAL_BUTTON_SUBMIT = 'bulk-delete-modal-button-submit'
    
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    NOTIFICATION
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """

    NOTIFICATION_SELECTOR = 'notification-selector' # NOTIFICATION BELL
    NOTIFICATION_DROPDOWN_RESULT = 'notification-dropdown-result'
    NOTIFICATION_TYPE = 'notification-type' # ORDER / SYSTEM / INFORMATION
    TAB_NOTIFICATION_TYPE_ORDER = 'tab-notification-type-order'
    TAB_NOTIFICATION_TYPE_SYSTEM = 'tab-notification-type-system'
    TAB_NOTIFICATION_TYPE_INFORMATION = 'tab-notification-type-information'
    NOTIFICATION_LIST_RESULT_ITEM = 'notification-list-result-item'
    
    
    # SNACKBAR BANNER
    NOTIFICATION_BOX = 'notification-box' # SNACKBAR BOX
    NOTIFICATION_TITLE = 'notification-title'
    NOTIFICATION_DESCRIPTION = 'notification-description'
    NOTIFICATION_CLOSE_BUTTON = 'notification-close-button'
    
    # MOBILE / APP
    NOTIFICATION_BOX_TITLE = 'notification-box-title'
    NOTIFICATION_BOX_DESCRIPTION = 'notification-box-description'
    NOTIFICATION_BOX_CLOSE = 'notification-box-close'

    
    # NOTIFICATION ORDER DETAILS MODAL
    NOTIFICATION_ORDER_DETAILS_LABEL = 'notification-order-details-label'
    NOTIFICATION_ORDER_DETAILS_VALUE = 'notification-order-details-value'
    NOTIFICATION_ORDER_DETAILS_MODAL = 'notification-order-details-modal'
    NOTIFICATION_ORDER_DETAILS_MODAL_ORDDER_TYPE = 'notification-order-details-modal-order-type'
    NOTIFICATION_ORDER_DETAILS_MODAL_CLOSE = 'notification-order-details-modal-close'
    

    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    SETTING
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """

    SWITCH_THEME_BUTTON = 'switch-theme-button'
    SETTING_BUTTON = 'setting-button'
    # APP_SETTING_BUTTON = ".//android.widget.TextView[matches(@text, '^\d+$')]/following-sibling::android.widget.TextView[2]"
    APP_SETTING_BUTTON = ".//android.widget.TextView[matches(@text, '^\\d+$')]/following-sibling::android.widget.TextView[2]"
    SETTING_OPTION_SWITCH_TO_DEMO = 'setting-option-switch-to-demo'
    SETTING_OPTION_SWITCH_TO_LIVE = 'setting-option-switch-to-live'
    SETTING_OPTION_OPEN_DEMO_ACCOUNT = 'setting-option-open-demo-account'
    SETTING_OPTION_PAYMENT_METHOD = 'setting-option-payment-method'
    SETTING_OPTION_OCT = 'setting-option-oct'
    SETTING_OPTION_NOTIFICATION_SETTING = 'setting-option-notification-setting'
    SETTING_OPTION_LANGUGAGE = 'setting-option-language'
    SETTING_OPTION_APPEARANCE = 'setting-option-appearance'
    
    # Change Password
    SETTING_OPTION_CHANGE_PASSWORD = 'setting-option-change-password'
    APP_SETTING_OPTION_CHANGE_PASSWORD = '//android.widget.TextView[@text="Change Password"]'
    CHANGE_PASSWORD_MODAL_OLD_PASSWORD = 'change-password-modal-old-password'
    CHANGE_PASSWORD_MODAL_NEW_PASSWORD = 'change-password-modal-new-password'
    CHANGE_PASSWORD_MODAL_CONFIRM_NEW_PASSWORD = 'change-password-modal-confirm-new-password'
    CHANGE_PASSWORD_MODAL_CONFIRM = 'change-password-modal-confirm'
    CHANGE_PASSWORD_MODAL_CLOSE = 'change-password-modal-close'
    
    # APP
    APP_CHANGE_PASSWORD_MODAL_OLD_PASSWORD = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.EditText'
    APP_CHANGE_PASSWORD_MODAL_NEW_PASSWORD = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.EditText'
    APP_CHANGE_PASSWORD_MODAL_CONFIRM_NEW_PASSWORD = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.widget.EditText'
    APP_CHANGE_PASSWORD_MODAL_CONFIRM = '//android.view.ViewGroup[@content-desc="Submit"]'
    
    
    # END OF CHANGE PASSWORD
    
    SETTING_OPTION_LINKED_DEVICE = 'setting-option-linked-device'
    SETTING_OPTION_BIOMETRICS_SETTING = 'setting-option-biometrics-settings'
    SETTING_OPTION_REQUEST_CANCEL_ACCOUNT = 'setting-option-request-cancel-account'
    SETTING_OPTION_CONTACT_INFORMATION = 'setting-option-contact-information'
    SETTING_OPTION_HELP_SUPPORT = 'setting-option-help-support'
    SETTING_OPTION_ABOUT = 'setting-option-about'
    SETTING_OPTION_LOGOUT = 'setting-option-logout'
    APP_SETTING_OPTION_LOGOUT = '//android.view.ViewGroup[@content-desc="Logout"]'
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    OPEN A DEMO ACCOUNT
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """

    INPUT_FIELD_VALIDATION = 'input-field-validation'
    DEMO_ACCOUNT_CREATION_MODAL_NAME = 'demo-account-creation-modal-name'
    DEMO_ACCOUNT_CREATION_MODAL_EMAIL = 'demo-account-creation-modal-email'
    COUNTRY_DIAL_CODE = 'country-dial-code'
    COUNTRY_DIAL_CODE_DROPDOWN = 'country-dial-code-dropdown'
    COUNTRY_DIAL_CODE_SEARCH = 'country-dial-code-search'
    COUNTRY_DIAL_CODE_ITEM = 'country-dial-code-item'
    DEMO_ACCOUNT_CREATION_MODAL_PHONE = 'demo-account-creation-modal-phone'
    DEPOSIT_DROPDOWN_ITEM = 'deposit-dropdown-item'
    DEMO_ACCOUNT_CREATION_MODAL_CONFIRM = 'demo-account-creation-modal-confirm'
    DEMO_ACCOUNT_CREATION_MODAL_AGREEMENT_UNCHECKED = 'demo-account-creation-modal-agreement-unchecked'
    DEMO_ACCOUNT_COMPLETION_MODAL_TITLE = 'demo-account-completion-modal-title'
    DEMO_COMPLETION_LABEL = 'demo-completion-label'
    DEMO_COMPLETION_VALUE = 'demo-completion-value'
    
    
    # APP
    APP_DEMO_ACCOUNT_CREATION_MODAL_NAME = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.widget.EditText'
    APP_DEMO_ACCOUNT_CREATION_MODAL_EMAIL = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.EditText'
    APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE = '(//android.view.ViewGroup[3]//android.view.ViewGroup)[1]'
    APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE_LABEL = '//android.widget.TextView[@text="Dial Code"]'
    APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE_SEARCH = '//android.widget.EditText[@text="Search"]'
    APP_DEMO_ACCOUNT_CREATION_MODAL_COUNTRY_DIAL_CODE_ITEM = '//android.widget.ScrollView//android.view.ViewGroup/android.view.ViewGroup'
    APP_DEMO_ACCOUNT_CREATION_PHONE_NUMBER = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[4]/android.view.ViewGroup/android.widget.EditText'
    APP_DEMO_ACCOUNT_CREATION_DEPOSIT_AMT = '(//android.view.ViewGroup[5]//android.view.ViewGroup)[1]'
    APP_DEMO_ACCOUNT_CREATION_DEPOSIT_AMT_OPTIONS = '//android.widget.ScrollView/android.view.ViewGroup/android.view.ViewGroup'
    APP_DEMO_ACCOUNT_CREATION_AGREE_CONTINUE = '//android.widget.TextView[@text="Agree and continue"]'
    APP_DEMO_ACCOUNT_ERROR_CHECK = '//android.widget.TextView[contains(@text, "required")]'
    
    # APP DEMO ACCOUNT CREATTION SCREEN
    APP_DEMO_ACCOUNT_COMPLETION_COPIED = '//android.widget.TextView[@text="Copy"]'
    APP_DEMO_ACCOUNT_COMPLETION_TITLE = '//android.widget.TextView[@text="Your demo account has been opened successfully."]'
    APP_DEMO_ACCOUNT_COMPLETION_LABEL = '//android.widget.TextView[matches(@text, "^(Login|Password|View Only Password|Name|Leverage|Deposit)$")]'
    APP_DEMO_ACCOUNT_COMPLETION_VALUE = '//android.widget.TextView[matches(@text, "^(Login|Password|View Only Password|Name|Leverage|Deposit)$")]/following-sibling::android.widget.TextView[1]'
    APP_DEMO_ACCOUNT_COMPLETION_SIGN_IN = '//android.widget.TextView[@text="Sign in"]'
    
    
    """
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                    ACCOUNT HEALTH
    ---------------------------------------------------------------------------------------------------------------------------------------------------- 
    """
    
    ACCOUNT_SELECTOR = 'account-selector'
    ACCOUNT_TYPE_TAG = 'account-type-tag'
    APP_ACCOUNT_TYPE_TAG = '//android.widget.TextView[@text="DEMO"]'
    ACCOUNT_NAME = 'account-name'
    # APP_ACCOUNT_NAME = '(//android.view.ViewGroup/android.widget.TextView)[3]'
    APP_ACCOUNT_NAME = '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView[1]'
    ACCOUNT_ID = 'account-id'
    APP_ACCOUNT_ID = '(//android.view.ViewGroup/android.widget.TextView)[4]'
    ACCOUNT_DETAIL = 'account-detail'
    APP_ACCOUNT_DETAIL = '(//android.view.ViewGroup/android.widget.TextView)[8]'
    ACCOUNT_OPTION_BALANCE = 'account-option-balance'
    ACCOUNT_TOTAL_BALANCE = 'account-total-balance'
    APP_ACCOUNT_BALANCE = '//android.widget.TextView[@text="Available Balance"]/following-sibling::android.widget.TextView[1]'
    
    # ACCOUNT HEALTH DROPDOWN
    ACCOUNT_OPTION_DETAIL = 'account-option-detail'
    ACCOUNT_OPTION_ITEM = 'account-option-item'
    ADD_ACCOUNT = 'add-account'

    
    # LINK AND SWITCH / DELETE
    LINK_ACCOUNT_MODAL_TITLE = 'link-account-modal-title'
    LINK_ACCOUNT_MODAL_ACCOUNT_ID = 'link-account-modal-account-id'
    LINK_ACCOUNT_MODAL_PASSWORD = 'link-account-modal-password'
    LINK_ACCOUNT_MODAL_CONFIRM = 'link-account-modal-confirm'
    LINK_ACCOUNT_MODAL_CLOSE = 'link-account-modal-close'
    LINK_SWITCH_CONFIRMATION_MODAL_TITLE = 'link-switch-confirmation-modal-title'
    LINK_SWITCH_CONFIRMATION_MODAL_DESCRIPTION = 'link-switch-confirmation-modal-description'
    LINK_SWITCH_CONFIRMATION_MODAL_CONFIRM = 'link-switch-confirmation-modal-confirm'
