import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_subMenu.utils import menu_button
from common.mobileweb.module_symbol.utils import input_symbol
from common.desktop.trade.utils import toggle_radioButton_OCT, trade_market_order, modify_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, compare_dataframes, process_and_print_data, extract_order_info, process_order_notifications



@allure.epic("MT4 Desktop TS_aB - Market")

# Member Portal
class TC_MT4_aB01():

    @allure.title("TC_MT4_aB01")

    @allure.description(
        """
        Member able to submit a Market Buy order with OCT disabled
        - Size 
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id


        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
            with allure.step("Launch WT"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")
                
            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")

            # with allure.step("Disable OCT"):
            #     toggle_radioButton_OCT(driver=main_driver)
                
        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)
