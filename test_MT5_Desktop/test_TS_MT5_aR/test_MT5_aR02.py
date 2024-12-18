import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, button_buy_sell_type, dropdown_orderType, btn_minMax_size, btn_minMax_stopLoss, btn_minMax_takeProfit

@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR02():

    @allure.title("TC_MT5_aR02")

    @allure.description(
        """
        Market Order
        
        Increase/Decrease by button
        """
        )
    
    def test_TC02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live") 

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", symbol_type="Symbols_Price")
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Click on Buy button"):
                button_buy_sell_type(driver=main_driver, indicator_type="buy")

            with allure.step("Increase / Decrease Volume"):
                btn_minMax_size(driver=main_driver, minMax="increase", number_of_clicks=5)
                btn_minMax_size(driver=main_driver, minMax="decrease", number_of_clicks=3)

            with allure.step("Select the orderType option: Market"):
                dropdown_orderType(driver=main_driver, partial_text="market")
                
            with allure.step("Increase / Decrease Stop Loss"):
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="price", minMax="decrease", number_of_clicks=5)
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="points", minMax="increase", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="points", minMax="decrease", number_of_clicks=3)
            
        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
