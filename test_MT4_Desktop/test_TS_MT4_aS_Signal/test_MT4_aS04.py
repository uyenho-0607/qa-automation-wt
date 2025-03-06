import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radioButton, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_signal.utils import button_copyTrade, handle_order_type
from data_config.utils import compare_dataframes, process_and_print_data


@allure.parent_suite("MT4 Membersite - Desktop - Signal")

@allure.epic("MT4 Desktop ts_as - Signal")


# Member Portal
class TC_mt4_as04():

    @allure.title("tc_mt4_as04")

    @allure.description(
        """
        Signal - Copy To Trade Order (OCT)
        """
        )
    
    def test_tc04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")
            
            with allure.step("Copy To Trade Order"):
                copyTrade_df, label_OrderStatus = button_copyTrade(driver=main_driver)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Compare against the Copy Trade and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=copyTrade_df, name1="Copy Trade Details", df2=trade_snackbar_banner_df, name2="Snackbar Banner Message")

            with allure.step("Redirect to Asset Page"):
                orderPanel_type, orderPanel_name = handle_order_type(driver=main_driver, order_type=label_OrderStatus)

            with allure.step("Retrieve the Newly Created Order"):
                _, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=orderPanel_type, section_name=orderPanel_name, row_number=[1])
            
            with allure.step("Compare against the Snackbar message and Order Panel details"):
                compare_dataframes(driver=main_driver, df1=trade_snackbar_banner_df, name1="Snackbar Banner Message", df2=trade_order_df, name2=orderPanel_name)
            
            with allure.step("Print the Order Table Result"):
                process_and_print_data(copyTrade_df, trade_snackbar_banner_df, trade_order_df)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
