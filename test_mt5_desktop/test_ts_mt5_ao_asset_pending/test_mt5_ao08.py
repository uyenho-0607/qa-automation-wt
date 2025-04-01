import allure
import pytest

from enums.main import Server, Menu, OrderPanel
from dateutil.parser import parse
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_sub_menu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_limit_order, close_delete_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Asset - Modify / Delete Pending Order")

@allure.epic("MT5 Desktop ts_ao - Asset - Modify / Delete Pending Order")

# Member Portal
class TC_MT5_aO08():

    @allure.title("TC_MT5_aO08")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Limit Order
        - Volume
        - Take Profit By Price
        - Expiry: Good Till Cancelled
        - Expiry: Specified Date and Time

        Member able to delete a Limit order
        """
    )

    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc08(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT5)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="unchecked")

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, tp_type="price", expiryType="specified-date-and-time", expiryDate="19", targetMonth=parse("April 2025"), hour_option="11", min_option="35", specifiedDate=True)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name="Trade Pending Order", row_number=[1])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_tradeConfirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Order """

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu=Menu.ASSETS)

            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, pending_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name="Asset Pending Order", row_number=[1])
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"

            """ Delete Pending Order """

            with allure.step("Order Panel: Pending Order - Click on Delete button"):
                close_delete_order(driver=main_driver, row_number=[1], order_action="close")

            with allure.step("Retrieve the snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.ORDER_AND_DEALS, section_name="Order History", row_number=[1])

                compare_dataframes(driver=main_driver, df1=pending_order_df, name1="Asset Pending Order", df2=order_history_df, name2="Order History")
            
            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, snackbar_banner_df, order_history_df)

        except Exception as e:
            test_failed = True  # Mark test as failed
            if test_failed:
                attach_text(get_text=str(e), name="Failure Info")
                shutdown(main_driver)
                raise  # Trigger retry if enabled

        finally:
            attach_session_video_to_allure(session_id)

            # Determine if this is the last attempt
            rerun_marker = request.node.get_closest_marker("flaky")
            if rerun_marker:
                reruns = rerun_marker.kwargs.get("reruns", 0)  # Max retries
                current_attempt = getattr(request.node, "execution_count", 1)  # Start at 1
                last_attempt = current_attempt >= (reruns + 1)  # Last attempt happens on final retry
            else:
                last_attempt = True  # No retries configured

            # Shutdown the driver if the test passed immediately OR if it's the last retry attempt
            if last_attempt or not test_failed:
                shutdown(main_driver)