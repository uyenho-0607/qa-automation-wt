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

def compare_dataframes(driver, df1, df2, name1, name2, required_columns):
    """
    Compare two dataframes and assert if the required columns match between them.

    Arguments:
    - df1 (DataFrame): First dataframe
    - df2 (DataFrame): Second dataframe
    - name1 (str): Name of the first dataframe for reporting
    - name2 (str): Name of the second dataframe for reporting
    - required_columns (list): List of column names required for comparison

    Raises:
    - AssertionError: If the required columns do not match between the two dataframes
    """
    try:
            
        # Check if inputs are valid DataFrames
        if not isinstance(df1, pd.DataFrame):
            raise TypeError(f"df1 is not a DataFrame, it is a {type(df1)}")
        if not isinstance(df2, pd.DataFrame):
            raise TypeError(f"df2 is not a DataFrame, it is a {type(df2)}")
        
        # Concatenate the dataframes
        master_df = pd.concat([df1, df2])

        # Group by 'Order No.' if it exists, otherwise treat as a single group
        if 'Order No.' in df1.columns and 'Order No.' in df2.columns:
            grouped = master_df.groupby('Order No.')
        else:
            grouped = [('All', master_df)]

        for orderID, group in grouped:
            # Transpose the group dataframe and fill missing values with '-'
            group_transposed = group.set_index('Section').T.fillna('-')

            # Convert the transposed dataframe to a formatted table using tabulate
            formatted_table = tabulate(group_transposed, tablefmt='grid', stralign='center', headers='keys')

            # Attach the formatted table as an attachment in allure report or print for debugging
            attach_text(formatted_table, name=f"Table Comparison for {name1} and {name2} - {orderID}")

            # Extract the index values from the transposed DataFrame
            desired_index = group_transposed.index.tolist()

            # Check if the required columns exist in the index of the transposed dataframe
            if set(required_columns).issubset(desired_index):
                # Get values of 'df1' and 'df2' columns using the desired index
                df1_values = group_transposed.loc[desired_index, name1]
                df2_values = group_transposed.loc[desired_index, name2]

                # Find mismatched values
                mismatched = (df1_values != df2_values) & df1_values.index.isin(required_columns)

                if mismatched.any():
                    # Display mismatched values
                    error_message = f"Values do not match for {orderID} in the following fields:\n"
                    mismatched_details = pd.DataFrame({
                        'Field': df1_values[mismatched].index,
                        f'{name1} Value': df1_values[mismatched],
                        f'{name2} Value': df2_values[mismatched]
                    })
                    error_message += mismatched_details.to_string(index=False)

                    # Raise an assertion error with the error message
                    assert False, error_message

                else:
                    attach_text(f"All values match for {orderID}", name="Values Comparison Result")
            else:
                # Required columns not found in the index
                missing_columns = set(required_columns) - set(desired_index)
                attach_text(f"Missing columns for {orderID}: {missing_columns}", name="Missing Data")
                assert False, f"Required columns not found in the index for {orderID}"

    except Exception as e:
        # Log the full exception message and stacktrace
        # Raise an assertion error with the error message
        handle_exception(driver, e)
        # assert False, f"{str(e)}\n{traceback.format_exc()}"


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