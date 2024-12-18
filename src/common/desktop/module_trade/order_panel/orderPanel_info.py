from tabulate import tabulate

from selenium.webdriver.common.by import By

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import wait_for_element_visibility, spinner_element, javascript_click, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_element_by_xpath_with_wait, visibility_of_element_by_xpath, visibility_of_element_by_testid, get_label_of_element
from common.desktop.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers
from common.desktop.module_chart.chart import get_chart_symbol_name


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
        handle_exception(driver, e)
        
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
def type_orderPanel(driver, tab_order_type, sub_tab=None, position: bool = False):
    try:
        delay(1)
        
        orderPanel_type = visibility_of_element_by_testid(driver, data_testid=f"tab-asset-order-type-{tab_order_type}")

        javascript_click(driver, element=orderPanel_type)
        
        if position:
            # orderHistory_position = visibility_of_element_by_testid(driver, data_testid="tab-asset-order-type-history-orders-and-deals")
            orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
            click_element(orderHistory_position)
            
    except Exception as e:
        handle_exception(driver, e)

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
            
        for row in row_number:
            # Find all elements matching the attribute selector
            action_button = find_element_by_xpath(driver, f"(//div[contains(@data-testid, 'button-{order_action}')])[{row}]")
            click_element(action_button)

        # For Pending Order tab (OCT disable)
        if delete_button:
            # local_delete_button = find_element_by_testid(driver, data_testid="close-order-button-submit")
            local_delete_button = find_element_by_xpath(driver, "//button[contains(normalize-space(text()), 'Delete Order')]")
            click_element(local_delete_button)
        
        if order_action == "edit":
            visibility_of_element_by_testid(driver, data_testid="edit-confirmation-modal")

        if order_action == "close":
            try:
                visibility_of_element_by_xpath(driver, "//div[@class='sc-ur24yu-1 eqxJBS']")
            except Exception as e:
                pass
                
    except Exception as e:
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE ORDERIDs
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_orderID(driver, row_number):

    order_ids = []
    try:
        # Locate the table body
        table_body = get_table_body(driver)
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Iterate through specified row numbers
        for row in row_number:
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")
            
            # Iterate through specified row numbers
            order_id_element = table_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_ids.append(order_id_element.text)

        attach_text(order_id_element.text, name="orderID")
        
        return order_ids

    except Exception as e:
        handle_exception(driver, e)

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
def extract_order_info(driver, tab_order_type, section_name, row_number, sub_tab=None, position: bool = False):
    
    # Initialize an empty list to hold the data
    order_ids = []
    table_row_contents = []

    try:

        type_orderPanel(driver, tab_order_type, sub_tab, position)
        
        # if response.status_code == 200:
        spinner_element(driver)

        # Locate the table body
        table_body = get_table_body(driver)
        
        # Locate the table header
        thead_data = get_table_headers(driver)

        # Check if the Symbol element exists and retrieve its data
        chart_symbol_name = get_chart_symbol_name(driver)
        if chart_symbol_name:
            thead_data.append("Symbol")

        spinner_element(driver)
        
        # Extract data from each specified row for order IDs
        for row in row_number:
            table_row = table_body.find_element(By.XPATH, f".//tr[{row}]")

            # Locate and extract the order ID from the current row
            order_id_element = visibility_of_element_by_xpath(driver, ".//td[contains(@data-testid, 'order-id')]")
            # order_id_element = table_row.find_element(By.XPATH, ".//td[contains(@data-testid, 'order-id')]")
            order_ids.append(order_id_element.text)

            # Extract data from the row for the table content
            cells = table_row.find_elements(By.XPATH, ".//th[1] | .//td")
            # row_data = [cell.text for cell in cells]
            
            row_data = []
            for cell in cells:            
                wait_for_element_visibility(driver, cell)
                row_data.append(cell.text)
                
            if chart_symbol_name:
                row_data.append(chart_symbol_name)
                
            table_row_contents.append(row_data)

        # Attach order IDs text
        attach_text(order_id_element.text, name="orderID")

        # else:
        #     assert False, f"Failed to fetch data. Status code: {response.status_code}"
        
        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        
        master_df_transposed = orderPanel_data.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=section_name)

        return order_ids, orderPanel_data

    except Exception as e:
        handle_exception(driver, e)

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
        handle_exception(driver, e)

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
        
        spinner_element(driver)

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
        handle_exception(driver, e)
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""