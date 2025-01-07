import re
import pandas as pd

from tabulate import tabulate

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.element import find_element_by_xpath, get_label_of_element

from common.desktop.module_subMenu.utils import menu_button
from constants.helper.screenshot import attach_text


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                OPEN A DEMO ACCOUNT
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def asset_account_balance_details(driver):
    """
    This function navigates to the 'Assets' page, retrieves the account name, Metatrader ID, 
    leverage, and available balance, then prints the extracted details.
        
    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Redirect to Asset page
        menu_button(driver, menu="assets")
        
        # Wait for the page to load
        delay(1)
        
        # Retrieve the Account Name
        account_name = find_element_by_xpath(driver, "//div[@class='sc-1noy9f2-2 kohjey']")
        label_accountName = get_label_of_element(account_name)

        # Extract the text after "LIVE" or "DEMO"
        # match = re.search(r"(?<=\b(LIVE|DEMO)\s)(.*)", label_accountName).group(2)

        # Extract account type (LIVE or DEMO) and the name after it
        match = re.search(r"(?<=\b(LIVE|DEMO)\s)(.*)", label_accountName)
        if match:
            account_type = match.group(1)  # LIVE or DEMO
            account_name = match.group(2)  # Account name without the type
            print(f"Account Type: {account_type}, Account Name: {account_name}")

        # Retrieve the MetatraderID and Leverage
        traderID = find_element_by_xpath(driver, "//div[@class='sc-1noy9f2-3 bZIhdg']")
        label_username = get_label_of_element(traderID)

        # Search for the pattern in the text
        match = re.search(r"UID:\s*(\d+)\s*\((\d+:\d+)\)", label_username)
        if match:
            uid = match.group(1)
            Leverage = match.group(2)
            print(f"MetatraderID: {uid}, Leverage: {Leverage}")
        
        # Account Balance (Available Balance)
        balance = find_element_by_xpath(driver, "(//div[@class='sc-2l74dl-0 iwdqqf'])[4]")
        label_balance = get_label_of_element(balance)
        print(f"Account Balance: {label_balance}")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
    
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                BALANCE DETAILS DROPDOWN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
     
def account_balance_details(driver):
    """
    Extracts account balance details from the platform and formats them into a readable table.
    """
    try:
        
        # Initialize lists to store account details and headers for the DataFrame
        accountDetails = []
        accountDetails_header = []
        
        # Retrieve the Account Balance
        account_balance = find_element_by_xpath(driver, "(//div[@class='sc-2l74dl-0 iwdqqf'])[1]")
        label_accountBalance = get_label_of_element(account_balance)
        accountDetails_header.append("Account Balance")
        accountDetails.append(label_accountBalance)
        
        # Retrieve the Account Name
        account_name = find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-5 fRgsvl']")
        label_accountName = get_label_of_element(account_name)
        accountDetails_header.append("Account Name")
        accountDetails.append(label_accountName)
        
        # Retrieve the MetaTrader ID
        traderID = find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-3 fdbvSk']")
        label_traderID = get_label_of_element(traderID)
        accountDetails_header.append("MetaTraderID")
        accountDetails.append(label_traderID)
        
        # Retrieve the Currency and Leverage information
        usd_leverage = find_element_by_xpath(driver, "//div[@class='sc-ck4lnb-4 iPvqUv']")
        label_usd_leverage = get_label_of_element(usd_leverage)
        
        # Parse the 'Currency | Leverage' pattern like "USD | 1:40"
        usd_or_leverage_match = re.search(r"(\w+)\s*\|\s*([\d:]+)", label_usd_leverage)
        if usd_or_leverage_match:
            currency = usd_or_leverage_match.group(1) # 'USD'
            accountDetails_header.append("Currency")
            accountDetails.append(currency)
            
            leverage = usd_or_leverage_match.group(2) # '1:40'
            accountDetails_header.append("Leverage")
            accountDetails.append(leverage)

        # Create a DataFrame with the snackbar message details
        account_summary = pd.DataFrame([accountDetails], columns=accountDetails_header)
        account_summary['Section'] = "Account Details"
        
        # Transpose the DataFrame for better readability and format it using tabulate
        overall = tabulate(account_summary.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
        
        # Attach the formatted table to the report for documentation purposes
        attach_text(overall, name="Account Details")
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
