import re
import traceback
import pandas as pd

from tabulate import tabulate

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - COMPARE THE DATA TO ENSURE IT MATCH
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# def normalize_value(value):
#     """
#     Normalize numeric values by stripping commas and trailing zeros.
#     """
#     if isinstance(value, str):
#         # Remove commas and trailing zeros after the decimal point
#         return value.replace(',', '').rstrip('0').rstrip('.') if '.' in value else value
#     return str(value)  # Return the value as a string if it's not a string already


def normalize_value(x):
    """Normalize numeric values by removing commas and trailing zeros."""
    """Normalize numeric values by removing commas, trailing zeros, and leading plus signs."""
    # Convert to string and remove commas
    # s = str(x).replace(',', '')
    s = str(x).replace(',', '').lstrip('+')
    # Check if the string represents a number (integer or decimal)
    if re.match(r'^-?\d*\.?\d+$', s):
        if '.' in s:
            integer_part, fractional_part = s.split('.', 1)
            fractional_part = fractional_part.rstrip('0')
            if not fractional_part:
                return integer_part
            else:
                return f"{integer_part}.{fractional_part}"
        else:
            return s
    else:
        return s
    

def compare_dataframes(driver, df1, df2, name1, name2, compare_volume: bool = True, compare_units: bool = True, compare_profit_loss: bool = False):
    """
    Compare two dataframes and automatically detect columns for comparison, ignoring trailing zeros and commas.

    Arguments:
    - driver: WebDriver instance for handling exceptions (unused in this function but required for interface)
    - df1 (DataFrame): First dataframe
    - df2 (DataFrame): Second dataframe
    - name1 (str): Name of the first dataframe for reporting
    - name2 (str): Name of the second dataframe for reporting
    - compare_profit_loss (bool): Flag to indicate whether to compare the "Profit/Loss" value

    Raises:
    - AssertionError: If mismatched values are found
    """
    try:
        # Check if inputs are valid DataFrames
        if not isinstance(df1, pd.DataFrame):
            raise TypeError(f"df1 is not a DataFrame, it is a {type(df1)}")
        if not isinstance(df2, pd.DataFrame):
            raise TypeError(f"df2 is not a DataFrame, it is a {type(df2)}")

# Check if either of the dataframes is empty
        if df1.empty or df2.empty:
            raise ValueError("One or both of the dataframes are empty.")
        
        # Find common columns for comparison
        common_columns = list(set(df1.columns) & set(df2.columns))

        # # If 'Volume, Profit/Loss' should not be compared, exclude it from the common columns
        # for column, condition in [("Volume", compare_volume), ("Profit/Loss", compare_profit_loss), ("Units", compare_units)]:
        #     if not condition and column in common_columns:
        #         common_columns.remove(column)
        
        # Handle "Volume" or "Size" dynamically
        size_columns = ["Volume", "Size"]
        for column in size_columns:
            if column in common_columns:
                if not compare_volume:  # If the flag is False, exclude the column from comparison
                    common_columns.remove(column)

        # If Profit/Loss should not be compared, exclude it from the common columns
        for column, condition in [("Profit/Loss", compare_profit_loss), ("Units", compare_units)]:
            if not condition and column in common_columns:
                common_columns.remove(column)

        if not common_columns:
            raise ValueError("No common columns found between the two dataframes")
        
        # Concatenate the dataframes with only common columns
        master_df = pd.concat([df1[common_columns], df2[common_columns]])

        # Group by 'Order No.' if it exists, otherwise treat as a single group
        if 'Order No.' in common_columns:
            grouped = master_df.groupby('Order No.')
        else:
            grouped = [("All", master_df)]

        for orderID, group in grouped:
            # Transpose the group dataframe and fill missing values with '-'
            group_transposed = group.set_index('Section').T.fillna('-')

            # Convert to formatted table using tabulate
            formatted_table = tabulate(group_transposed, tablefmt='grid', stralign='center', headers='keys')
            attach_text(formatted_table, name=f"Table Comparison for {name1} and {name2} - {orderID}")

            # Extract index values from transposed DataFrame
            desired_index = group_transposed.index.tolist()
            
            # Get values of 'df1' and 'df2' columns for detected common fields
            df1_values = group_transposed.loc[desired_index, name1]
            df2_values = group_transposed.loc[desired_index, name2]

            # Normalize values by removing commas and trailing zeros
            df1_values_stripped = df1_values.apply(normalize_value)
            df2_values_stripped = df2_values.apply(normalize_value)

            # Find mismatched values
            mismatched = (df1_values_stripped != df2_values_stripped)
            
            if mismatched.any():
                # Display mismatched values
                error_message = f"Values do not match for {orderID} in the following fields:\n"
                mismatched_details = pd.DataFrame({
                    'Field': df1_values_stripped[mismatched].index,
                    f'{name1} Value': df1_values_stripped[mismatched],
                    f'{name2} Value': df2_values_stripped[mismatched]
                })
                error_message += mismatched_details.to_string(index=False)
                attach_text(error_message, name="Mismatch Details")
                assert False, error_message
            else:
                attach_text(f"All values match for {orderID}", name=f"Comparison on {name1} and {name2} Result")

    except Exception as e:
        print(f"An error occurred during dataframe comparison between {name1} and {name2}. Error: {str(e)}")
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PRINT DATA
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def process_and_print_data(*dfs, group_by_order_no: bool = False):
    try:

        # Concatenate the dataframes
        master_df = pd.concat(dfs)
        
        if group_by_order_no:
            # Group by 'Order No.'
            grouped = master_df.groupby('Order No.')
            
            for order_no, group in grouped:
                # Transpose the group dataframe and fill missing values with '-'
                group_transposed = group.set_index('Section').T.fillna('-')
                
                # Print the tabulated data with the 'Result' column for each group
                overall = tabulate(group_transposed, headers='keys', tablefmt='grid', stralign='center')
                attach_text(overall, name=f"Table for Order No.: {order_no}")
        else:
            # Transpose the concatenated dataframe and fill missing values with '-'
            master_df_transposed = master_df.set_index('Section').T.fillna('-')
            
            # Print the tabulated data with the 'Result' column for the overall dataframe
            overall = tabulate(master_df_transposed, headers='keys', tablefmt='grid', stralign='center')
            attach_text(overall, name="Overall Table Comparison")

    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        assert False, f"{str(e)}\n{traceback.format_exc()}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""