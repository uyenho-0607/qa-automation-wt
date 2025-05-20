import re
from tabulate import tabulate

from selenium.webdriver.common.by import By

from enums.main import ButtonModuleType, OrderPanel, TradeConstants
from constants.element_ids import DataTestID

from constants.helper.driver import delay
from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element_android_app import spinner_element, get_label_of_element, click_element, click_element_with_wait, find_element_by_testid, find_element_by_xpath, find_element_by_testid_with_wait, find_element_by_xpath_with_wait, find_list_of_elements_by_xpath, find_visible_element_by_testid, find_visible_element_by_testid, wait_for_text_to_be_present_in_element_by_xpath


from common.mobileapp.module_trade.order_panel.op_general import extract_order_data_details, process_individual_orders, get_table_body, get_table_headers

# from common.mobileapp.module_chart.chart import get_chart_symbol_name



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL TYPE (OPEN POSITION / PENDING ORDER / ORDER HISTORY)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Choose order type (Open Position / Pending Order / Order History / Position (MT5) / Order & Deals (MT5))
def type_orderPanel(driver, tab_order_type: OrderPanel):
    try:
        delay(0.8)
        
        # Define both possible 'data-testid' values for the radio button states
        trade_action_button = {
            OrderPanel.OPEN_POSITIONS: DataTestID.TAB_ASSET_ORDER_TYPE_OPEN_POSITIONS,
            OrderPanel.PENDING_ORDERS: DataTestID.TAB_ASSET_ORDER_TYPE_PENDING_ORDERS,
            OrderPanel.HISTORY: DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY,
            OrderPanel.POSITION_HISTORY: DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY_POSITIONS_HISTORY,
            OrderPanel.ORDER_AND_DEALS: DataTestID.TAB_ASSET_ORDER_TYPE_HISTORY_ORDERS_AND_DEALS,   
        }
        
        button_testid = trade_action_button.get(tab_order_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {tab_order_type}")

        # Locate the trade action button using the provided trade_type
        order_panel_type = find_element_by_testid_with_wait(driver, data_testid=button_testid)
        # Click the button and wait for the action to complete
        click_element(order_panel_type)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - VIEW ALL TRANSACTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Choose order type (View all Transaction)
def button_viewAllTransaction(driver):
    try:
        viewAllTransaction_button = find_visible_element_by_testid(driver, data_testid=DataTestID.ASSET_HEADER_VIEW_ALL)
        click_element(viewAllTransaction_button)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL BUTTON (TRACK / EDIT / CLOSE (DELETE))
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# order panel - Track / Edit / Close (Delete) button
def handle_track_close_edit(driver, trade_type: ButtonModuleType, close_options: TradeConstants = TradeConstants.NONE):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        action_button = {
            ButtonModuleType.TRACK: DataTestID.ASSET_LIST_BUTTON_TRACK,
            ButtonModuleType.CLOSE: DataTestID.ASSET_LIST_BUTTON_CLOSE,
            ButtonModuleType.EDIT: DataTestID.ASSET_LIST_BUTTON_EDIT,
        }
        
        button_testid = action_button.get(trade_type)
        if not button_testid:
            raise ValueError(f"Invalid button type: {trade_type}")
            
        # Find all elements matching the attribute selector
        btn_module = find_element_by_xpath_with_wait(driver, button_testid)
        click_element_with_wait(driver, element=btn_module)
        
        # For Pending Order tab
        # if delete_button:
        if TradeConstants.DELETE_BUTTON in close_options:
            wait_for_text_to_be_present_in_element_by_xpath(driver, '//android.widget.TextView[@text="Confirm Delete Order?"]', text="Confirm Delete Order?")
            delete_button = find_element_by_testid(driver, data_testid=DataTestID.CLOSE_ORDER_BUTTON_SUBMIT)
            click_element(element=delete_button)

        if trade_type == ButtonModuleType.CLOSE:
            try:
                wait_for_text_to_be_present_in_element_by_xpath(driver, '//android.widget.TextView[@text="Confirm Close Order?"]', text="Confirm Close Order?")
            except Exception as e:
                pass

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# order panel table details 
def order_expand_details(driver, tab_order_type: OrderPanel):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        # Locate the Open Position / Pending Order / Order History tab
        type_orderPanel(driver, tab_order_type)

        action_button = find_element_by_xpath_with_wait(driver, DataTestID.ASSET_LIST_ITEM_EXPAND)
        click_element(action_button)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE order_ids
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_order_id(driver):
    try:
        
        # Wait till the spinner icon no longer display
        spinner_element(driver)
        
        order_id = find_element_by_xpath_with_wait(driver, DataTestID.ASSET_LIST_ITEM_ORDER_NO)
        label_order_id = get_label_of_element(order_id)
        
        # Regular expression to extract the order number
        order_number = re.search(r'\d+', label_order_id).group()

        attach_text(order_number, name="orderID")
        
        return order_number

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT TABLE ORDERs INFO (WITH order_ids PRINT SEPERATELY TABLE)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Extract the order table
def extract_order_info(driver, tab_order_type, section_name):
    # Initialize an empty list to hold the data
    order_ids = []
    table_row_contents = []

    try:
                
        # Expand the details of the specified row
        order_expand_details(driver, tab_order_type)

        # Locate the table header
        thead_data = get_table_headers(driver)

        # Locate all the row elements for the order data
        elements = find_list_of_elements_by_xpath(driver, DataTestID.ASSET_DETAILED_VALUE)
        delay(0.1)

        # Extract data from each specified row for order IDs
        for element in elements:

            # Extract the order ID only once
            order_id_element = find_element_by_xpath(driver, DataTestID.ASSET_DETAILED_ORDERID_VALUE)
            
            # Extract the text from the element
            table_row_contents.append(get_label_of_element(element=element))
        
        order_ids.append(get_label_of_element(element=order_id_element))
        
        # Append the symbol name only once after the loop
        asset_symbolName = find_visible_element_by_testid(driver, data_testid=DataTestID.ASSET_DETAILED_HEADER_SYMBOL)
        table_row_contents.append(get_label_of_element(element=asset_symbolName))
        thead_data.append("Symbol")

        asset_orderType = find_visible_element_by_testid(driver, data_testid=DataTestID.ASSET_ORDER_TYPE)
        table_row_contents.append(get_label_of_element(element=asset_orderType))
        thead_data.append("Type")

        # Attach order IDs text
        attach_text(order_id_element.text, name="orderID")

        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        
        master_df_transposed = orderPanel_data.set_index('Section').T.fillna('-')
        overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
        attach_text(overall, name=section_name)

        cancel_button = find_element_by_testid(driver, data_testid=DataTestID.ACTION_SHEET_CANCEL_BUTTON)
        click_element(cancel_button)
        
        return order_ids, orderPanel_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
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
                                                REVIEW order_ids FROM CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Ensure the pending order - order_ids not in the table 
def review_pending_order_ids(driver, order_ids, order_panel):
    try:
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        
        click_element_with_wait(driver, element=type_orderPanel)

        # Locate the table body
        table_body = get_table_body(driver)

        spinner_element(driver)

        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")]

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
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CHECK order_ids IN TABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def check_order_ids_in_table(driver, order_ids, order_panel, section_name, sub_tab = None, position : bool = False):
    try:
        type_orderPanel = find_element_by_testid(driver, data_testid=order_panel)
        click_element_with_wait(driver, element=type_orderPanel)

        if position:
            orderHistory_position = find_element_by_testid(driver, data_testid=f"tab-asset-order-type-history-{sub_tab}")
            click_element_with_wait(driver, element=orderHistory_position)
            
        # Locate the table body
        table_body = get_table_body(driver)

        table_rows = table_body.find_elements(By.XPATH, ".//tr")

        table_order_ids = [element.text for element in table_body.find_elements(By.XPATH, ".//*[contains(@data-testid, 'order-id')]")]
            
        thead_data = get_table_headers(driver)

        # Check if the Symbol element exists and retrieve its data
        # chart_symbol_name = get_chart_symbol_name(driver)
        # if chart_symbol_name:
        #     thead_data.append("Symbol")

        table_row_contents = []

        for order_id in order_ids:
            if order_id in table_order_ids:
                # Find the index of the order_id in table_order_ids
                index = table_order_ids.index(order_id)
                row = table_rows[index]
                cells = row.find_elements(By.XPATH, "./th[1] | ./td")
                row_data = [cell.text for cell in cells]

                # if chart_symbol_name:
                #     row_data.append(chart_symbol_name)
                
                table_row_contents.append(row_data)
        
        # Create a DataFrame using the data
        orderPanel_data = extract_order_data_details(driver, table_row_contents, thead_data, section_name)
        process_individual_orders(driver, orderPanel_data, order_ids)

        return orderPanel_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)