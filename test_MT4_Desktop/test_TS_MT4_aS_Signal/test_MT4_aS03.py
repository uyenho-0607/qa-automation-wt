import allure
import pytest

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting
from common.desktop.module_trade.utils import toggle_radioButton, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_signal.utils import button_copyTrade, handle_order_type
from data_config.utils import compare_dataframes, process_and_print_data


@allure.parent_suite("MT4 Membersite - Desktop - Signal")

@allure.epic("MT4 Desktop ts_as - Signal")


# Member Portal
class TC_MT4_aS03():

    @allure.title("TC_MT4_aS03")

    @allure.description(
        """
        Signal - Copy To Trade Order
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc03(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df, label_OrderStatus = button_copyTrade(driver=main_driver)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Compare against the Copy Trade Details and Trade Confirmation Details"):
                compare_dataframes(driver=main_driver, df1=copyTrade_df, name1="Copy Trade Details", df2=trade_tradeConfirmation_df, name2="Trade Confirmation Details")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details", df2=trade_snackbar_banner_df, name2="Snackbar Banner Message")

            with allure.step("Redirect to Asset Page"):
                orderPanel_type, orderPanel_name = handle_order_type(driver=main_driver, order_type=label_OrderStatus)

            with allure.step("Retrieve the Newly Created Order"):
                _, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=orderPanel_type, section_name=orderPanel_name, row_number=[1])
            
            with allure.step("Compare against the Snackbar message and Order Panel details"):
                compare_dataframes(driver=main_driver, df1=trade_snackbar_banner_df, name1="Snackbar Banner Message", df2=trade_order_df, name2=orderPanel_name)
            
            with allure.step("Print the Order Table Result"):
                process_and_print_data(copyTrade_df, trade_tradeConfirmation_df, trade_snackbar_banner_df, trade_order_df)
                
        except Exception as e:
            test_failed = True  # Mark test as failed
            if test_failed:
                attach_text(get_text=str(e), name="Failure Info")
                button_setting(driver=main_driver, setting_option="logout")
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