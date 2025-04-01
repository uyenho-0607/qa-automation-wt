import allure
import pytest

from enums.main import Server, OrderPanel
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_stopLimit_order, modify_stopLimit_order, get_neg_snackbar_banner, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info

@allure.parent_suite("MT5 Membersite - Desktop - Negative Scenarios")

@allure.epic("MT5 Desktop ts_as - Negative Scenarios")

# Member Portal
class TC_MT5_aS30():

    @allure.title("TC_MT5_aS30")

    @allure.description(
        """
        (Modify) - Pending Order (Stop Limit) Sell Order

        Negative Scenario: Pending Order - Invalid Price submitted
        Error message: Invalid Price Submitted
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc30(self, chromeDriver, request):
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
                
            with allure.step("Place Stop Limit Order"):
                trade_stopLimit_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, set_takeProfit=False, expiryType="good-till-day")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name="Pending Order", row_number=[1])

            """ Start of modifying Pending Order """
            
            with allure.step("Modify on Stop Limit Order"):
                modify_stopLimit_order(driver=main_driver, trade_type="edit", row_number=[1], entryPrice_flag=False, set_stopLoss=False, set_takeProfit=False, expiryType="good-till-cancelled")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="edit")
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)

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