import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_trade.utils import asset_symbolName


@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR06():
  
    @allure.title("TC_MT5_aR06")

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
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                
            with allure.step("Click on the symbol name to redirect to Trade page"):
                asset_symbolName(driver=main_driver, row_number=1)

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
