import allure
import pytest

from enums.main import Server, TradeConstants, ButtonModuleType, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radio_button, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_signal.utils import button_copyTrade, handle_order_type
from data_config.utils import compare_dataframes, process_and_print_data


@allure.parent_suite("MT5 Membersite - Desktop - Signal")

@allure.epic("MT5 Desktop ts_au - Signal")

# Member Portal
class TC_aU04():

    @allure.title("TC_aU04")

    @allure.description(
        """
        Signal - Copy To Trade Order
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc04(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)
                
            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="unchecked")
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df, label_OrderStatus = button_copyTrade(driver=main_driver)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)

            with allure.step("Compare against the Copy Trade Details and Trade Confirmation Details"):
                compare_dataframes(driver=main_driver, df1=copyTrade_df, name1=SectionName.COPY_TRADE_DETAIL, df2=trade_confirmation_df, name2=SectionName.TRADE_CONFIRMATION_DETAILS)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Redirect to Asset Page"):
                order_panel_type, orderPanel_name = handle_order_type(driver=main_driver, order_type=label_OrderStatus)

            with allure.step("Retrieve the Newly Created Order"):
                _, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=order_panel_type, section_name=orderPanel_name)
            
            with allure.step("Compare against the Snackbar message and Order Panel details"):
                compare_dataframes(driver=main_driver, df1=trade_snackbar_banner_df, name1=SectionName.SNACKBAR_BANNER_MESSAGE, df2=trade_order_df, name2=orderPanel_name, compare_options=TradeConstants.COMPARE_VOLUME)
            
            with allure.step("Print the Order Table Result"):
                process_and_print_data(copyTrade_df, trade_confirmation_df, trade_snackbar_banner_df, trade_order_df)
                
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