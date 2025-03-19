import allure
import pytest

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radioButton, trade_oct_market_order, get_trade_snackbar_banner
from common.mobileapp.module_markets.utils import myTrade_order


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android ts_ar - Markets")

# Member Portal
class TC_MT4_aR05():

    @allure.title("TC_MT4_aR05")

    @allure.description(
        """
        "My Trade" displays the symbol of the most recently placed order.
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc05(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4, client_name="Lirunex")

            with allure.step("Search symbol"):
                symbolName = input_symbol(driver=main_driver, server=Server.MT4, client_name="Lirunex")

            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Market Order"):
                direction = trade_oct_market_order(driver=main_driver, indicator_type="buy")

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Verify My Trade Order"):
                myTrade_order(driver=main_driver, symbol_name=symbolName, order_type=direction)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)