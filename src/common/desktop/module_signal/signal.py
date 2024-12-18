import random
import pandas as pd

from tabulate import tabulate

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, visibility_of_element_by_xpath, get_label_of_element
from constants.helper.screenshot import attach_text

from common.desktop.module_trade.order_placing_window.utils import input_size_volume, button_trade_action
from common.desktop.module_subMenu.utils import menu_button


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                COPY TO TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_copyTrade(driver):
    try:
        menu_button(driver, menu="signal")

        # Data dictionary to store extracted labels
        copyTrade_elements = []
        copyTrade_headers = []

        # Define the two possible options
        options = [
            "(//button[contains(normalize-space(text()), 'Copy to order')])[1]",
            "(//button[contains(normalize-space(text()), 'Copy to order')])[2]"
        ]
        
        # Select a random option
        selected_option = random.choice(options)
        
        # Find and click the selected option
        btn_copyTrade = visibility_of_element_by_xpath(driver, selected_option)
        click_element(btn_copyTrade)
        
        entryPrice = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[2]")
        label_entryPrice = get_label_of_element(entryPrice)
        copyTrade_elements.append(label_entryPrice)
        copyTrade_headers.append("Entry Price")

        stopLoss = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[3]")
        label_stopLoss = get_label_of_element(stopLoss)
        copyTrade_elements.append(label_stopLoss)
        copyTrade_headers.append("Stop Loss")

        # Conditional logic for take profit
        if selected_option == options[0]:  # If first button is selected
            takeProfit1 = visibility_of_element_by_xpath(driver, "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[1]")
            print(takeProfit1.text)
            label_takeProfit = get_label_of_element(takeProfit1)
            print("xx", label_takeProfit)
        else:  # If second button is selected
            takeProfit2 = visibility_of_element_by_xpath(driver, "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[2]")
            label_takeProfit = get_label_of_element(takeProfit2)
        copyTrade_elements.append(label_takeProfit)
        copyTrade_headers.append("Take Profit")

        # Create a DataFrame with the snackbar message details
        copyTrade_details = pd.DataFrame([copyTrade_elements], columns=copyTrade_headers)
        copyTrade_details['Section'] = "Copy Trade Details"
        print(copyTrade_details)

        master_df_transposed = copyTrade_details.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center', numalign='center')
        attach_text(overall, name="Copy Trade Details")
        
        input_size_volume(driver)
        
        button_trade_action(driver, trade_type="trade")
        
        # Return the transposed DataFrame
        return copyTrade_details
    
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""