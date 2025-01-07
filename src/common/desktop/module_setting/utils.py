from common.desktop.module_setting.setting_general import button_setting, button_theme
from common.desktop.module_setting.setting_switchAccount import switch_account_type, link_account, switch_or_delete_account
from common.desktop.module_setting.setting_changePwd import change_password
from common.desktop.module_setting.setting_demoAccount import generate_random_name_and_email, generate_singapore_phone_number, open_demo_account, demo_account_ready_screen, handle_sign_in, validate_account_details


__all__ = [
    
    # Setting General
    'button_setting',
    'button_theme',
    
    # Switch Account
    'switch_account_type',
    'link_account',
    'switch_or_delete_account',
    
    # Change Password
    'change_password',
    
    # Demo Account
    'generate_random_name_and_email',
    'generate_singapore_phone_number',
    'open_demo_account',
    'demo_account_ready_screen',
    'handle_sign_in',
    'validate_account_details'

]