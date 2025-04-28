import allure
import pytest

from enums.main import Server, TradeDirectionOption, SLTPOption, AlertType
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_market_order, get_neg_snackbar_banner

@allure.parent_suite("MT4 Membersite - Desktop - Negative Scenarios")

@allure.epic("MT4 Desktop ts_aq - Negative Scenarios")

# Member Portal
class TC_MT4_aQ02():

    @allure.title("TC_MT4_aQ02")

    @allure.description(
        """
        (Place) OCT - Market Sell Order

        Negative Scenario: Invalid Take Profit
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
        
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc02(self, chrome_driver, request):
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
                
            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Take Profit - Price"):
                trade_market_order(driver=main_driver, option=TradeDirectionOption.SELL, tp_type=SLTPOption.PRICE, take_profit_flag=AlertType.NEGATIVE)

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