import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_subMenu.utils import menu_button
# from common.mobileweb.trade.utils import asset_symbolName


@allure.epic("MT4 Mobile TS_aP")

# Member Portal
class TC_MT4_aP06():
  
    @allure.title("TC_MT4_aP06")

    @allure.description(
        """
        Member redirect to the symbol page upon clicking on symbol name
        """
        )
      
    def test_TC06(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu_option="assets")
                
            # with allure.step("Click on the symbol name to redirect to Trade page"):
                # asset_symbolName(driver=main_driver, row_number=1)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)