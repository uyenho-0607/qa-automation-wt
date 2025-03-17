from constants.element_ids import DataTestID
from constants.helper.error_handler import handle_exception
from constants.helper.element_android_app import click_element, wait_for_element_clickable_xpath



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MENU SELECTION (TRADE / MARKET / ASSET / SIGNAL / CALENDAR / NEWS)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# menu button (Trade / Market / Asset / Signal / Calendar / News)
def menu_button(driver, menu: str):
    """
    Navigates to a specified menu in the sidebar by clicking on it.

    Arguments:
    - menu: The name of the menu to navigate to (e.g., 'trade', 'markets', 'assets', 'signal', 'news', 'copy-trade').

    Raises:
    - AssertionError: If any exception occurs, an assertion is raised with the error message and stack trace.
    """
    try:
        
        # Determine the data-testid based on the button type
        button_testids = {
            "home": DataTestID.APP_SIDE_BAR_OPTION_HOME.value,
            "market": DataTestID.APP_SIDE_BAR_OPTION_MARKET.value,
            "trade": DataTestID.APP_SIDE_BAR_OPTION_TRADE.value,
            "info": DataTestID.APP_SIDE_BAR_OPTION_INFO.value,
            "assets": DataTestID.APP_SIDE_BAR_OPTION_ASSETS.value
        }
        
        button_testid = button_testids.get(menu)
        if not button_testid:
            raise ValueError(f"Invalid button type: {menu}")
        
        # Locate the menu element using the provided menu name and data-testid attribute
        menu_selection = wait_for_element_clickable_xpath(driver, button_testid)
        
        # menu_selection = visibility_of_element_by_testid(driver, data_testid=f"side-bar-option-{menu}")
        # Click on the found menu element with an optional wait to ensure the action is completed
        click_element(element=menu_selection)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""