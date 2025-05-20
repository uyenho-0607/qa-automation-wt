from enums.main import Menu
from constants.element_ids import DataTestID

from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element, find_visible_element_by_testid


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                MENU SELECTION (TRADE / MARKET / ASSET / SIGNAL / CALENDAR / NEWS)
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# menu button (Trade / Market / Asset / Signal / Calendar / News)
def menu_button(driver, menu: Menu):
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
            Menu.TRADE: DataTestID.SIDE_BAR_OPTION_TRADE,
            Menu.MARKET: DataTestID.SIDE_BAR_OPTION_MARKETS,
            Menu.SIGNAL: DataTestID.SIDE_BAR_OPTION_SIGNAL,
            Menu.NEWS: DataTestID.SIDE_BAR_OPTION_NEWS,
            Menu.ASSETS: DataTestID.SIDE_BAR_OPTION_ASSETS,
            Menu.DEALER: DataTestID.SIDE_BAR_OPTION_DEALER,
            Menu.EDUCATION: DataTestID.SIDE_BAR_OPTION_EDUCATION
        }
        
        button_testid = button_testids.get(menu)
        if not button_testid:
            raise ValueError(f"Invalid button type: {menu}")
        
        # Locate the menu element using the provided menu name and data-testid attribute
        menu_selection = find_visible_element_by_testid(driver, button_testid)
        
        # Click on the found menu element with an optional wait to ensure the action is completed
        click_element(element=menu_selection)
        
        if "selected" in menu_selection.get_attribute("class"):
            return menu_selection.text.strip().lower()

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""