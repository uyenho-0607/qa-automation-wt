import allure
import pytest

from enums.main import Server, ButtonModuleType, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_chart.utils import chart_min_max, chart_trade_modal_close
from common.desktop.module_trade.utils import toggle_radio_button, trade_limit_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Desktop - Trade - Chart - Place Order")

@allure.epic("MT4 Desktop ts_ai - Chart - Order Placing Window")

# Member Portal
class TC_MT4_aI03():

    @allure.title("TC_MT4_aI03")

    @allure.description(
        """
        Buy Order
        
        Member able to place a Limit order via Chart
        - Size
        - Price
        - Stop Loss by Points
        - Take Profit by Price
        - Expiry: Good Till Day
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc03(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT4)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="unchecked")
                
            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, option=TradeDirectionOption.BUY, sl_type=SLTPOption.POINTS, tp_type=SLTPOption.PRICE, expiry_type=ExpiryType.GOOD_TILL_DAY, chart_fullscreen="toggle")

            with allure.step("Click on the Trade Confirmation button to update the order"):
                trade_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)

            with allure.step("Retrieve the updated order snackbar message "):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
        
            with allure.step("Close the Trade Modal"):
                chart_trade_modal_close(driver=main_driver)
                
            with allure.step("Exit Fullscreen Chart"):
                chart_min_max(driver=main_driver, chart_fullscreen="exit")
                
            with allure.step("Retrieve the Pending Order data"):
                _, pending_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.TRADE_PENDING_ORDER)

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=pending_order_df, name1=SectionName.TRADE_PENDING_ORDER, df2=snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, trade_confirmation_df, snackbar_banner_df)

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