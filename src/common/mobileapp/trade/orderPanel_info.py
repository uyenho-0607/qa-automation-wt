import traceback

from tabulate import tabulate

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.screenshot import take_screenshot, attach_text
from constants.helper.element_android_app import spinner_element, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_list_of_elements_by_xpath, find_element_by_xpath_with_wait, visibility_of_element_by_xpath, visibility_of_element_by_testid, get_label_of_element
from common.mobileweb.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.mobileweb.module_chart.chart import get_chart_symbol_name


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ASSET - SYMBOL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def asset_symbolName(driver, row_number):
    try:
                
        # Locate the table body
        get_table_body(driver)
        
        # Locate the table header
        get_table_headers(driver)

        # Wait till the spinner icon no longer display
        spinner_element(driver)

        symbol_name = find_element_by_xpath_with_wait(driver, f"(//td[@data-testid='asset-open-column-symbol'])[{row_number}]")

        # symbol_name = find_element_by_xpath_with_wait(driver, f"(//span[@class='sc-wfkeqv-0 dLLeem'])[{row_number}]")
        asset_symbolName = get_label_of_element(symbol_name)
        print("asset symbol name", asset_symbolName)
        click_element_with_wait(driver, element=symbol_name)
        
        delay(1)

        chart_symbolName = get_chart_symbol_name(driver)

        # Check if chart symbol name matches desired symbol name
        if asset_symbolName == chart_symbolName:
            attach_text(asset_symbolName, name="Symbol Name")
            assert True
        else:
            assert False, f"Invalid Symbol Name: {chart_symbolName}"


    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "asset_symbolName - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}" 

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL TYPE (OPEN POSITION / PENDING ORDER / ORDER HISTORY)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Choose order type (Open Position / Pending Order / Order History)
def type_orderPanel(driver, tab_order_type):
    try:

        orderPanel_type = visibility_of_element_by_xpath(driver, f"//div[@data-testid='tab-asset-order-type-{tab_order_type}']")

        click_element_with_wait(driver, element=orderPanel_type)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "type_orderPanel - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL BUTTON (TRACK / CLOSE (DELETE) / EDIT)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# order panel - Track / Close (Delete) / Edit button
def button_orderPanel_action(driver, order_action, row_number, delete_button: bool = False):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
            
        # Find all elements matching the attribute selector
        action_button = find_element_by_xpath_with_wait(driver, f"(//div[contains(@data-testid, 'button-{order_action}')])[{row_number}]")
        
        click_element_with_wait(driver, element=action_button)
        
        # For Pending Order tab
        if delete_button:
            delete_button = find_element_by_xpath_with_wait(driver, "//button[text()='Delete Order']")
            click_element_with_wait(driver, element=delete_button)

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_orderPanel_action - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL BUTTON (TRACK / CLOSE (DELETE) / EDIT)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# order panel
def order_expand_details(driver, row_number):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)

        action_button = find_element_by_xpath(driver, f"(//div[contains(@data-testid, 'list-item-expand')])[{row_number}]")
        
        click_element_with_wait(driver, element=action_button)
            

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "button_orderPanel_action - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE ORDERIDs
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_orderID(driver, row_numbers):

    order_ids = []
    try:
        # Locate the table body
        table_body = get_table_body(driver)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Iterate through specified row numbers
        for row in row_numbers:
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")
            
            # Iterate through specified row numbers
            order_id_element = table_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_ids.append(order_id_element.text)

        attach_text(order_id_element.text, name="orderID")
        
        return order_ids

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "get_orderID - Exception Screenshot")
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT TABLE ORDERs INFO (WITH ORDERIDs PRINT SEPERATELY TABLE)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Extract the order table
def extract_order_info(driver, tab_order_type, section_name, row_number):
    # Initialize an empty list to hold the data
    order_ids = []
    table_row_contents = []

    try:
        
        # Locate the Open Position / Pending Order / Order History tab
        type_orderPanel(driver, tab_order_type)
        
        # Expand the details of the specified row
        order_expand_details(driver, row_number)

        # Locate the table header
        thead_data = get_table_headers(driver)

        # Locate all the row elements for the order data
        elements = find_list_of_elements_by_xpath(driver, "//div[contains(@data-testid, 'value')]")
        delay(0.1)

        # Extract data from each specified row for order IDs
        for element in elements:
            print(element.text)
            
            # Extract the order ID only once
            order_id_element = find_element_by_xpath(driver, "//div[contains(@data-testid, 'order-id-value')]")
            
            # Extract the text from the element
            table_row_contents.append(element.text)
        
        order_ids.append(order_id_element.text)
        
        # Append the symbol name only once after the loop
        chart_symbol_name = visibility_of_element_by_testid(driver, data_testid="asset-detailed-header-symbol")
        thead_data.append("Symbol")
        table_row_contents.append(chart_symbol_name.text)

        # Attach order IDs text
        attach_text(order_id_element.text, name="orderID")
        
        print("order data value", table_row_contents)

        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        print("ddd", orderPanel_data)
        
        master_df_transposed = orderPanel_data.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=section_name)

        cancel_button = find_element_by_testid(driver, data_testid="action-sheet-cancel-button")
        click_element(cancel_button)
        
        return order_ids, orderPanel_data

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "extract_order_info - Exception Screenshot")
        # Log the full exception message and stacktrace
        assert False, f"{str(e)}\n{traceback.format_exc()}"
        


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANNEL NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Helper function to map order panel data_testid to a descriptive name
def get_order_panel_name(order_panel):
    order_panel_names = {
        "tab-asset-order-type-history": "Order History / Position",
        "tab-asset-order-type-history-orders-and-deals": "Order History (Order & Deals)",
        "tab-asset-order-type-pending-orders": "Pending Orders",
        "tab-asset-order-type-open-positions": "Open Positions",
        # Add more mappings as needed
    }
    return order_panel_names.get(order_panel, "Order Panel")

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                REVIEW ORDERIDs FROM CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Ensure the pending order - orderIDs not in the table 
def review_pending_orderIDs(driver, order_ids, order_panel):
    try:
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        
        click_element_with_wait(driver, element=type_orderPanel)

        # Locate the table body
        table_body = get_table_body(driver)

        spinner_element(driver)

        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")]

        failed_order_ids = []
        
        result_message = f"Switching to order panel: {get_order_panel_name(order_panel)}\n"
                
        for order_id in order_ids:
            if order_id in table_order_ids:
                result_message += f"Data match for {order_id}\n"
            else:
                result_message += f"No Data match for {order_id}\n"
                failed_order_ids.append(order_id)
                
        attach_text(result_message.strip(), name="Order Result")

        return failed_order_ids

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "review_pending_orderIDs - Exception Screenshot")
        # Handle potential errors during element interaction
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHECK ORDERIDs IN TABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def check_orderIDs_in_table(driver, order_ids, order_panel, section_name, sub_tab = None, position : bool = False):
    try:
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        click_element_with_wait(driver, element=type_orderPanel)

        if position:
            orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
            click_element_with_wait(driver, element=orderHistory_position)
            
        # Locate the table body
        table_body = get_table_body(driver)

        table_rows = table_body.find_elements(By.XPATH, ".//tr")

        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")]
            
        thead_data = get_table_headers(driver)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        table_row_contents = []

        for order_id in order_ids:
            if order_id in table_order_ids:
                # Find the index of the order_id in table_order_ids
                index = table_order_ids.index(order_id)
                row = table_rows[index]
                cells = row.find_elements(By.XPATH, "./th[1] | ./td")
                row_data = [cell.text for cell in cells]

                if chart_symbol_name:
                    row_data.append(chart_symbol_name)
                
                table_row_contents.append(row_data)
        
        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        process_individual_orders(driver, orderPanel_data, order_ids)

        return orderPanel_data

    except Exception as e:
        # Attach a screenshot in case of an exception
        take_screenshot(driver, "check_orderIDs_in_table - Exception Screenshot")
        # Handle potential errors during element interaction
        assert False, f"{str(e)}\n{traceback.format_exc()}"