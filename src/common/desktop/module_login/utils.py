from common.desktop.module_login.cpuat import launch_cpuat, cpuat_user_login, btn_webTrader, login_cpuat
from common.desktop.module_login.webtrader_login import launch_wt, handle_alert_error, handle_login_result, wt_user_login, login_wt, select_account_type, select_and_verify_language
from common.desktop.module_login.forgot_password import handle_help_is_on_the_way, handle_reset_password_flow, forgot_password
from common.desktop.module_login.language import select_and_verify_language, select_english_language


__all__ = [
    
    # CPUAT
    'launch_cpuat',
    'cpuat_user_login',
    'btn_webTrader',
    'login_cpuat',
    
    
    # WT
    'launch_wt',
    'handle_alert_error',
    'handle_login_result',
    'wt_user_login',
    'login_wt',
    'select_account_type',
    
    # Language
    'select_and_verify_language',
    'select_english_language',
    
    # Forgot Password
    'handle_help_is_on_the_way',
    'handle_reset_password_flow',
    'forgot_password'
]