import pandas as pd

from tabulate import tabulate

from constants.helper.error_handler import handle_exception
from constants.helper.screenshot import attach_text
from constants.helper.element import find_list_of_elements_by_xpath, visibility_of_element_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TABLE BODY FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_body(driver):
    """
    Extracts and returns the table body (<tbody>) element.

    This function finds the <tbody> element that contains a specific
    `data-testid` attribute value ('list'). It ensures the table body is visible
    before returning the element.

    Returns:
    - WebElement: The Selenium WebElement representing the <tbody> element.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Locate and return the <tbody> element with the data-testid 'list' that is visible on the page
        return visibility_of_element_by_xpath(driver, ".//tbody[contains(@data-testid, 'list')]")
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - TABLE HEADER NAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_table_headers(driver):
    """
    Extracts and returns a list of column headers from a table.

    This function finds all table header cells (<th>) within a <thead> element,
    retrieves their text, and returns them as a list of strings. Specific headers
    like "price" and "entry price" are standardized to "Entry Price".

    Returns:
    - List of strings: A list of cleaned table headers (column names).

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Wait till the spinner icon no longer display
        # spinner_element(driver)

        # Find all <th> elements inside the <thead> with a specific data-testid for headers
        thead_rows = find_list_of_elements_by_xpath(driver, "//thead[contains(@data-testid, 'table-header')]//th")
        
        # Extract the text from each header element, ensuring we ignore empty strings
        thead_data = [header.text for header in thead_rows if header.text.strip() != '']
        
        # Standardize specific headers like "price" or "entry price"
        for i, header in enumerate(thead_data):
            # Check if the header matches any of the specified ones (case-insensitive)
            if header.lower() in ("price", "entry price"):
                thead_data[i] = "Entry Price" # Standardize the header to "Entry Price"
                break # Exit after the first match (to prevent unnecessary iterations)
        
        # Return the structured data
        return thead_data

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - RETRIEVE EACH INDIVDIUAL ORDER ROW - ORDERID
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_individual_orders(driver, orderPanel_data, table_order_ids):
    """
    Processes each individual order from the provided order data and generates a formatted table.
    
    For each order ID in the `table_order_ids`, this function:
    1. Filters the `orderPanel_data` to get the details for the specific order.
    2. Transposes the order data and fills any missing values with '-'.
    3. Formats the data into a grid-style table.
    4. Attaches the formatted table for that order with the order ID.

    Parameters:
    - orderPanel_data: A Pandas DataFrame containing order data with columns including 'Order No.' and 'Section'.
    - table_order_ids: A list of order IDs for which the table data should be extracted and formatted.

    Returns:
    - None: The function performs actions like attaching tables but does not return any value.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        # Iterate over each order ID in the provided list
        for order_id in table_order_ids:
            # Filter the DataFrame for the specific order using the 'Order No.' column
            individual_order_data = orderPanel_data[orderPanel_data['Order No.'] == order_id]
            
            # Check if any data was found for the given order_id
            if not individual_order_data.empty:
                # Transpose the DataFrame for better readability, setting 'Section' as the index
                # Fill missing values with a hyphen ('-') for any missing data
                # Format the transposed data into a grid using the tabulate library
                overall = tabulate(individual_order_data.set_index('Section').T.fillna('-'), headers='keys', tablefmt='grid', stralign='center')
                
                # Attach the formatted table to the report with the order ID
                attach_text(overall, name=f"Table for Order No.: {order_id}")

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER PANEL - CREATE DATAFRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_order_data_details(driver, table_row_contents, thead_data, section_name):
    """
    Extracts and structures order data details from table row contents and converts it into a Pandas DataFrame.
    
    This function takes the row data from a table, applies column headers, and adds a section label to the data.
    
    Arguments:
    - table_row_contents: A list of lists (or tuples) representing the rows of the table.
    - thead_data: A list of column headers for the table.
    - section_name: A string representing the section name to be added as a new column to the DataFrame.

    Returns:
    - orderPanel_data: A Pandas DataFrame containing the structured order data, including the section name.

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Ensure the table_row_contents and thead_data have matching dimensions
        if len(table_row_contents) == 0:
            raise ValueError("No table rows found in the provided table_row_contents.")
        if len(thead_data) == 0:
            raise ValueError("No column headers provided in thethead_data.")
        
        # Create the DataFrame from the table rows and headers
        orderPanel_data = pd.DataFrame(table_row_contents, columns=thead_data)
        
        # Add a new column for the section name
        orderPanel_data['Section'] = section_name

        # Return the structured data
        return orderPanel_data
    
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""