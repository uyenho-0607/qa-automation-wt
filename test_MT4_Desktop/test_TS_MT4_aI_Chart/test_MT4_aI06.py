import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_chart.utils import chart_minMax, chart_trade_modal_close
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_stop_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Desktop TS_aI - Chart - Order Placing Window")

# Member Portal 
class TC_MT4_aI05():

    @allure.title("TC_MT4_aI05")
        
    @allure.description(
        """
        Sell Order
        
        Member able to place a Stop order via Chart
        - Size
        - Price
        - Stop Loss by Points
        - Take Profit by Price
        - Expiry: Good Till Day
        """
    )
    
    def test_TC05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, trade_type="trade", option="sell", sl_type="points", tp_type="price", expiryType="good-till-day", set_Chart=True, chart_fullscreen="toggle")

            with allure.step("Click on the Trade Confirmation button to update the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Retrieve the updated order snackbar message "):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Stop Loss", "Take Profit"])
            
            with allure.step("Close the Trade Modal"):
                chart_trade_modal_close(driver=main_driver)
                
            with allure.step("Exit Fullscreen Chart"):
                chart_minMax(driver=main_driver, chart_fullscreen="exit")
                
            with allure.step("Retrieve the Pending Order data"):
                _, pending_order_df = extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(df1=pending_order_df, name1="Pending Order",
                                   df2=snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Stop Loss", "Take Profit"])
                
            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, trade_tradeConfirmation_df, snackbar_banner_df)
                    


                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
