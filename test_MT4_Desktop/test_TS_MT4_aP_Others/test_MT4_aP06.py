import allure
import pytest

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, button_tradeModule, dropdown_orderType, button_buy_sell_type, verify_volume_minMax_buttons, btn_minMax_price, btn_min_max_stop_loss, btn_minMax_takeProfit

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop ts_ap - Others")

# Member Portal
class TC_MT4_aP06():
  
    @allure.title("TC_MT4_aP06")

    @allure.description(
        """
        (Place) - Pending Order - Limit
        
        Increase/Decrease by button
        """
        )
      
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc06(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", symbol_type="Symbols_Price")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Specification OCT"):
                _, _, vol_step = button_tradeModule(driver=main_driver, module_Type="specification")

            with allure.step("Click on Trade tab"):
                button_tradeModule(driver=main_driver, module_Type="trade")
                
            with allure.step("Select the orderType option: Limit"):
                dropdown_orderType(driver=main_driver, partial_text="limit")
                
            with allure.step("Click on Buy button"):
                button_buy_sell_type(driver=main_driver, indicator_type="buy")
                
            with allure.step("Increase / Decrease Size"):
                verify_volume_minMax_buttons(driver=main_driver, trade_type="trade", actions=[("increase", 5), ("decrease", 3)], size_volume_step=vol_step)
                
            with allure.step("Increase / Decrease Entry Price"):
                btn_minMax_price(driver=main_driver, trade_type="trade", minMax="decrease", number_of_clicks=5)
                btn_minMax_price(driver=main_driver, trade_type="trade", minMax="increase", number_of_clicks=3)

            with allure.step("Increase / Decrease Stop Loss"):
                btn_min_max_stop_loss(driver=main_driver, trade_type="trade", type="price", min_max="decrease", number_of_clicks=5)
                btn_min_max_stop_loss(driver=main_driver, trade_type="trade", type="points", min_max="increase", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="points", minMax="decrease", number_of_clicks=3)

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