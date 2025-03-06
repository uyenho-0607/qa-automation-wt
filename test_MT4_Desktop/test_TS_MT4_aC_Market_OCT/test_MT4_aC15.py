import allure
import pandas as pd

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_market_order, modify_market_order, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Desktop - Trade - Market Order")

@allure.epic("MT4 Desktop ts_ac - Market OCT")

# Member Portal
class TC_mt4_ac15():

    @allure.title("tc_mt4_ac15")
    
    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Size
        - Stop Loss by Price
        - Take Profit by Points
        
        Member able to modify a Market order with
        - Stop Loss by Points
        - Take Profit by Price
        """
    )
    
    def test_tc15(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="sell", sl_type="price", tp_type="points")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Trade Open Position", row_number=[1])

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position", df2=trade_snackbar_banner_df, name2="Snackbar Banner Message")

            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=original_orderID)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe

                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position", df2=noti_msg_df, name2="Notification Order Message")

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1="Trade Open Position", df2=noti_order_df, name2="Notification Order Details")
                
            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df, noti_msg_df, noti_order_df)

            """ End of Place Order """


            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, trade_type="edit", row_number=[1], sl_type="points", tp_type="price")

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Updated Open Position", row_number=[1])

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1="Updated Open Position", df2=edit_snackbar_banner_df, name2="Snackbar Banner Message")

            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                            
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID == updated_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
