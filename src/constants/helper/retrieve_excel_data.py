from __future__ import annotations

import os
import pandas as pd

from constants.helper.error_handler import handle_exception

from custom_types import ParamData



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                PARSE DATA FROM EXCEL FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def parse_data_from_param_sheet(param_file_path: str = "./parameters.xlsx", sheet_name: str | None = None):
    """
        Retrieve a DataFrame of the Excel sheet containing test case parameters
        If `sheet_name` is specified, a DataFrame of that sheet tab will be returned
        If `sheet_name` is None, a consolidated DataFrame of all sheets will be returned

        e.g.
        parse_data_from_param_sheet("./parameters.xlsx")
        >>>>> df = data from Sheet1 + Sheet2 + Sheet3
        parse_data_from_param_sheet("./parameters.xlsx", sheet_name="Sheet2")
        >>>>> df = data from Sheet2
    """
    try:
        # Use os.path.expanduser() to get the user's home directory and construct the file path
        file_path = os.path.expanduser(param_file_path)

        # Read the Excel file using the provided file path and sheet name "login"
        return pd.read_excel(file_path, sheet_name=sheet_name)

    except Exception as e:
        handle_exception(e)

    return None

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                RETRIEVE VALUE FROM DATAFRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def retrieve_value_from_dataframe(df: ParamData, filter_column: str, keyword: str | int, column: str):
    """
        Retrieve a single value of `column` field which matches the condition `filter_column` == `keyword`

        e.g.
            df =    index       name        status
                        0       tom         active
                        1       harry       inactive
                        2       jane        suspended
        retrieve_value_from_dataframe(df, name, "jane", status)
        >>>> suspended
        retrieve_value_from_dataframe(df, status, "inactive", name)
        >>>> harry
    """
    return df.loc[df[filter_column] == keyword, column].iloc[0]

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""