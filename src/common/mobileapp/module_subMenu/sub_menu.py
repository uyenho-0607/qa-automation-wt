from constants.helper.error_handler import handle_exception
from constants.helper.element import click_element_with_wait, visibility_of_element_by_testid


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
        # Locate the menu element using the provided menu name and data-testid attribute
        menu_selection = visibility_of_element_by_testid(driver, data_testid=f"side-bar-option-{menu}")
        # Click on the found menu element with an optional wait to ensure the action is completed
        click_element_with_wait(driver, element=menu_selection)
        
        if "selected" in menu_selection.get_attribute("class"):
            return menu_selection.text.strip().lower()

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""