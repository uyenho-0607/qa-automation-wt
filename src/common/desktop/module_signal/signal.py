import random
import pandas as pd

from tabulate import tabulate

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, visibility_of_element_by_xpath, get_label_of_element
from constants.helper.screenshot import attach_text

from common.desktop.module_trade.order_placing_window.utils import input_size_volume, button_trade_action
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_chart.utils import get_chart_symbol_name


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                COPY TO TRADE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def button_copyTrade(driver):
    try:
        
        # Navigate to the 'Signal' menu using a helper function
        menu_button(driver, menu="signal")

        # Lists to store extracted labels and corresponding headers
        copyTrade_elements = []
        copyTrade_headers = []
        
        # Define two possible options for selecting trade details
        options = [
            {
                "button_xpath": "(//button[contains(normalize-space(text()), 'Copy to order')])[1]",
                "take_profit_xpath": "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[1]"
            },
            {
                "button_xpath": "(//button[contains(normalize-space(text()), 'Copy to order')])[2]",
                "take_profit_xpath": "(//div[normalize-space(@class)='sc-hm0akf-9 lnouFc'])[2]"
            }
        ]
        
        # Randomly select one of the defined options
        selected_option = random.choice(options)
        
        # Find and click the 'Copy to order' button using the selected option
        btn_copyTrade = visibility_of_element_by_xpath(driver, selected_option["button_xpath"])
        click_element(btn_copyTrade)

        chart_symbol_name = get_chart_symbol_name(driver)
        copyTrade_elements.append(chart_symbol_name)
        copyTrade_headers.append("Symbol")
        
        OrderStatus = visibility_of_element_by_xpath(driver, "//span[@class='sc-7yzo5u-0 lkwwuc']")
        label_OrderStatus = get_label_of_element(OrderStatus).upper()
        copyTrade_elements.append(label_OrderStatus)
        copyTrade_headers.append("Type")

        # Extract the 'Entry Price' label
        entryPrice = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[2]")
        label_entryPrice = get_label_of_element(entryPrice)
        copyTrade_elements.append(label_entryPrice)
        copyTrade_headers.append("Entry Price")

        # Extract the 'Stop Loss' label
        stopLoss = visibility_of_element_by_xpath(driver, "(//div[@class='sc-hm0akf-4 liWewR'])[3]")
        label_stopLoss = get_label_of_element(stopLoss)
        copyTrade_elements.append(label_stopLoss)
        copyTrade_headers.append("Stop Loss")

        # Extract the 'Take Profit' label using the take_profit_xpath of the selected option
        takeProfit = visibility_of_element_by_xpath(driver, selected_option["take_profit_xpath"])
        label_takeProfit = get_label_of_element(takeProfit)
        copyTrade_elements.append(label_takeProfit)
        copyTrade_headers.append("Take Profit")

        # Create a DataFrame with the extracted copy trade details
        copyTrade_details = pd.DataFrame([copyTrade_elements], columns=copyTrade_headers)
        copyTrade_details['Section'] = "Copy Trade Details"
        print(copyTrade_details)

        # Transpose the DataFrame for better readability and format it using tabulate
        master_df_transposed = copyTrade_details.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center', numalign='center')
        
        # Attach the formatted table to the report for documentation purposes
        attach_text(overall, name="Copy Trade Details")
        
        # Input the trade volume
        input_size_volume(driver)
        
        # Perform the trade action (e.g., 'trade')
        button_trade_action(driver, trade_type="trade")
        
        # Return the transposed DataFrame containing trade details
        return copyTrade_details
    
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""