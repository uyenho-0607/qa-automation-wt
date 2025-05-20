import allure
import pytest

from enums.main import Server, SymbolsList, TradeDirectionOption, ExpiryType, SectionName, OrderPanel

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_stop_limit_order, btn_min_max_price, btn_min_max_stop_limit_price, btn_min_max_stop_loss, btn_min_max_take_profit, handle_track_close_edit, get_trade_snackbar_banner, extract_order_info

@allure.parent_suite("MT5 Membersite - Desktop - Others")

@allure.epic("MT5 Desktop ts_ar - Others")

# Member Portal
class TC_aR07():

    @allure.title("TC_aR07")
    
    @allure.description(
        """
        (Modify) - Pending Order (Stop Limit)
        
        Increase/Decrease by button
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc07(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT5, symbol_type=SymbolsList.SYMBOLS_PRICE)
             
            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="checked")

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_stop_limit_order(driver=main_driver, option=TradeDirectionOption.SELL, expiry_type=ExpiryType.GOOD_TILL_CANCELLED)

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.UPDATED_PENDING_ORDER)

            """ End of Place Limit Order """

            """ Start of modifying Pending Order """
                
            with allure.step("Modify order"):
                handle_track_close_edit(driver=main_driver, trade_type="edit")
                
            with allure.step("Increase / Decrease Entry Price"):
                btn_min_max_price(driver=main_driver, trade_type="edit", min_max="increase", number_of_clicks=5)
                btn_min_max_price(driver=main_driver, trade_type="edit", min_max="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Stop Limit Price"):
                btn_min_max_stop_limit_price(driver=main_driver, trade_type="edit", min_max="increase", number_of_clicks=5)
                btn_min_max_stop_limit_price(driver=main_driver, trade_type="edit", min_max="decrease", number_of_clicks=3)
                
            with allure.step("Increase / Decrease Stop Loss"):
                btn_min_max_stop_loss(driver=main_driver, trade_type="edit", type="price", min_max="increase", number_of_clicks=5)
                btn_min_max_stop_loss(driver=main_driver, trade_type="edit", type="points", min_max="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_min_max_take_profit(driver=main_driver, trade_type="edit", type="price", min_max="decrease", number_of_clicks=5)
                btn_min_max_take_profit(driver=main_driver, trade_type="edit", type="points", min_max="increase", number_of_clicks=3)

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