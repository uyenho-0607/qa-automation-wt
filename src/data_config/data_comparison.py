import re
import traceback
import pandas as pd

from tabulate import tabulate

from constants.helper.screenshot import attach_text
from constants.helper.error_handler import handle_exception
from enums.main import TradeConstants

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                TRADE / EDIT - COMPARE THE DATA TO ENSURE IT MATCH
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

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
    
def compare_dataframes(driver, df1, df2, name1, name2, compare_options: TradeConstants = TradeConstants.NONE):
    """
    Compare two dataframes and automatically detect columns for comparison, ignoring trailing zeros and commas.
    """
    try:
        if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
            raise TypeError("Both df1 and df2 must be pandas DataFrames")

        if df1.empty or df2.empty:
            raise ValueError("One or both of the dataframes are empty.")
        
        common_columns = list(set(df1.columns) & set(df2.columns))

        # Handle columns dynamically based on enum flags
        exclusions = {
            "Volume": TradeConstants.COMPARE_VOLUME,
            "Size": TradeConstants.COMPARE_VOLUME,
            "Units": TradeConstants.COMPARE_UNITS,
            "Profit/Loss": TradeConstants.COMPARE_PROFIT_LOSS
        }
        
        # By default, always exclude 'Profit/Loss'
        if compare_options & TradeConstants.COMPARE_PROFIT_LOSS == TradeConstants.NONE:
            if "Profit/Loss" in common_columns:
                print("Excluding 'Profit/Loss' column by default.")
                common_columns.remove("Profit/Loss")
                
        # Exclude columns based on the flags in compare_options
        for column, flag in exclusions.items():
            if column in common_columns and (compare_options & flag):  # Exclude if the flag is set
                print(f"Excluding column: {column} because compare_options includes {flag}")
                common_columns.remove(column)

        if not common_columns:
            raise ValueError("No common columns found between the two dataframes")
        
        # Merge DataFrames based on common columns
        master_df = pd.concat([df1[common_columns], df2[common_columns]])

        # Group by 'Order No.' if available
        grouped = master_df.groupby('Order No.') if 'Order No.' in common_columns else [("All", master_df)]

        for orderID, group in grouped:
            group_transposed = group.set_index('Section').T.fillna('-')
            formatted_table = tabulate(group_transposed, tablefmt='grid', stralign='center', headers='keys')
            attach_text(formatted_table, name=f"Table Comparison for {name1} and {name2} - {orderID}")

            desired_index = group_transposed.index.tolist()
            df1_values = group_transposed.loc[desired_index, name1]
            df2_values = group_transposed.loc[desired_index, name2]

            df1_values_stripped = df1_values.apply(normalize_value)
            df2_values_stripped = df2_values.apply(normalize_value)

            mismatched = (df1_values_stripped != df2_values_stripped)
            
            if mismatched.any():
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