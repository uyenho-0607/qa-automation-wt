import re
from decimal import Decimal
from collections import defaultdict

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import get_label_of_element, find_list_of_elements_by_xpath

from common.desktop.module_setting.setting_general import accountInformation



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                SETTING ACCOUNT INFORMATION TAB
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def sum_by_currency(driver):
    try:
        accountInformation(driver)
        
        currency_totals = defaultdict(lambda: Decimal('0'))
        
        amounts = find_list_of_elements_by_xpath(driver, "//div[@class='sc-3lrinj-1 AzVAk']")
        
        for amount in amounts:
            text = amount.text.strip()
            match = re.match(r"([\d,]+\.\d+)\s*([A-Z]+)", text)
            if match:
                value_str = match.group(1).replace(',', '')
                currency = match.group(2)
                value = Decimal(value_str)
                currency_totals[currency] += value
        
        total_balance_elements = find_list_of_elements_by_xpath(driver, "//div[@class='sc-h7om0g-0 hcOEZB']/span")
        
        for total_balance_element in total_balance_elements:
            label_total_balance = get_label_of_element(element=total_balance_element)

            # Extract numeric value and currency from the total balance label
            match = re.match(r"([\d,]+\.\d+)\s*([A-Z]+)", label_total_balance)
            if match:
                total_balance_value_str = match.group(1).replace(',', '')
                total_balance_currency = match.group(2)
                
                # Direct conversion assuming valid input
                total_balance_value = Decimal(total_balance_value_str)
                
                computed_total = currency_totals.get(total_balance_currency, Decimal('0'))
                if computed_total == total_balance_value:
                    attach_text(f"{total_balance_currency} Balance matches: {computed_total:,.2f}{total_balance_currency}", name=f"Expected total balance: {label_total_balance}")
                else:
                    assert False, (f"Balance mismatch! Computed: {currency_totals[total_balance_currency]:,.2f} vs Account Balance: {total_balance_value:,.2f} {total_balance_currency}")
            else:
                assert False, "Total balance label format is incorrect."
        
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""     
        
