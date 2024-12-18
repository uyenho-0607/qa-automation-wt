import allure
import pandas as pd

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_chart.utils import chart_minMax, chart_trade_modal_close
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data


@allure.epic("MT4 Desktop TS_aI - Chart - Order Placing Window")

# Member Portal
class TC_MT4_aI02():

    @allure.title("TC_MT4_aI02")
              
    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order via Chart
        - Size
        - Stop Loss by Price
        - Take Profit by Points
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
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")

            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="sell", set_Chart=True, chart_fullscreen="chart-toggle-fullscreen", sl_type="price", tp_type="points")
                
            with allure.step("Click on the Trade Confirmation button to update the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")

            with allure.step("Retrieve the updated order snackbar message "):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(df1=trade_tradeConfirmation_df, name1="Trade Confirmation Details",
                                   df2=snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])
            
            with allure.step("Close the Trade Modal"):
                chart_trade_modal_close(driver=main_driver)
            
            with allure.step("Exit Fullscreen Chart"):
                chart_minMax(driver=main_driver, chart_fullscreen="chart-exit-fullscreen")

            with allure.step("Retrieve the Open Position data"):
                orderIDs_openPosition, open_position_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Open Position", row_number=[1])

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(df1=open_position_df, name1="Open Position",
                                   df2=snackbar_banner_df, name2="Snackbar Banner Message",
                                   required_columns=["Symbol", "Type", "Size", "Units", "Stop Loss", "Take Profit"])

            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=orderIDs_openPosition)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe

                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(df1=open_position_df, name1="Open Position",
                                   df2=noti_msg_df, name2="Notification Order Message",
                                   required_columns=["Symbol", "Order No.", "Size"])

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(df1=open_position_df, name1="Open Position",
                                   df2=noti_order_df, name2="Notification Order Details",
                                   required_columns=["Open Date", "Symbol", "Order No.", "Type", "Size", "Units", "Take Profit", "Stop Loss", "Swap", "Commission"])

            with allure.step("Print Final Result"):
                process_and_print_data(open_position_df, trade_tradeConfirmation_df, snackbar_banner_df, noti_msg_df, noti_order_df)
                                

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
