import yaml
import os

def test(web):
    # Read demo account credentials from YAML file
    credentials_path = os.path.join(os.path.dirname(__file__), "data", "test_accounts", "demo_account_credentials.yaml")
    
    with open(credentials_path, 'r') as f:
        accounts = yaml.safe_load(f)
    
    # Change password back to original for each account
    for account in accounts:
        user_id = account["user_id"]
        current_password = account["password"]  # Use the actual password from YAML
        
        # Login with current password
        web.login_page.login(userid=user_id, password=current_password)

        web.home_page.settings.change_password(current_password, "Autotest@12345")

        # Logout to prepare for next account
        web.home_page.settings.logout()

