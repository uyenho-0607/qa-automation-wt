from common.desktop.module_setting.setting_general import button_setting, button_theme
from common.desktop.module_setting.setting_account_details import sum_by_currency
from common.desktop.module_setting.setting_notifications import notification_settings_modal
from common.desktop.module_setting.setting_link_switch_account import switch_account_type, link_account, switch_or_delete_account, handle_password_prompt_on_account_switch
from common.desktop.module_setting.setting_change_pwd import populate_password_fields, submit_and_handle_alert, capture_alert, handle_success, perform_login, handle_error, change_password
from common.desktop.module_setting.setting_demo_account import generate_random_name_and_email, generate_singapore_phone_number, open_demo_account_error_msg, open_demo_account_screen, demo_account_ready_screen, handle_sign_in, validate_account_details

__all__ = [
    
    # Setting General
    'button_setting',
    'button_theme',
    'notification_settings_modal',
    
    # Account Details
    'sum_by_currency',
    
    # Switch Account
    'switch_account_type',
    'link_account',
    'switch_or_delete_account',
    'handle_password_prompt_on_account_switch',
    
    # Change Password
    'populate_password_fields',
    'submit_and_handle_alert',
    'capture_alert',
    'handle_success',
    'perform_login',
    'handle_error',
    'change_password',

    # Demo Account
    'generate_random_name_and_email',
    'generate_singapore_phone_number',
    'open_demo_account_error_msg',
    'open_demo_account_screen',
    'demo_account_ready_screen',
    'handle_sign_in',
    'validate_account_details',

]