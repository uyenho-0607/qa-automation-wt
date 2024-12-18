import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_cpuat


@allure.epic("MT4 Desktop TS_aA - Login")

# example: function based implementation
class TC_MT4_aA01():
    # filepath = "./parameters.xlsx"
    # data = parse_data_from_param_sheet(filepath)
        
    @allure.title("TC_MT4_aA01")

    @allure.description(
        """
        Member able login to CPUAT and redirect to Web Trader
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)

        try:
            
            with allure.step("Launch CPUAT and redirect to WebTrader website"):
                login_cpuat(self, platform="CPUAT", testcaseID="TC01")

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(self.driver)

            attach_video_to_allure(screen_recording_file, class_name)
