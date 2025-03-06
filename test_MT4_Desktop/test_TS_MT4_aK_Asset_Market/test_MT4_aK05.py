import allure
import pandas as pd

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_symbol.search_symbol import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_market_order, close_delete_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Desktop - Asset - Modify / Close Market Order")

@allure.epic("MT4 Desktop ts_am - Asset - Modify / Close Market Order")

# Member Portal
class TC_mt4_ak05():

    @allure.title("tc_mt4_ak05")

    @allure.description(
        """
        Buy Order
                
        Member able to place a Market Order
        - Size
        - Stop Loss By Price
        - Take Profit By Points
        
        Member able to partial close an order
        """
        )
    
    def test_tc05(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")

            """Place Order """
            
            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="buy", sl_type="price", tp_type="points")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_tradeConfirmation_df = trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Trade Open Position", row_number=[1])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_tradeConfirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Order """
            
            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                                
            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, asset_order_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Asset Open Position", row_number=[1])
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"
                    
            """Start of Partial Close Order """

            with allure.step("Order Panel: Open Position - Click on Close to Partial close an order"):
                close_delete_order(driver=main_driver, row_number=[1], order_action="close", set_marketSize=True, clearField=True)
                
            with allure.step("Retrieve the snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the New Open Position data"):
                orderIDs_new_openPosition, new_open_position_df = extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="New Open Position", row_number=[1])

            with allure.step("Retrieve and compare New Open Position and Notification Order Message"):
                # Call the method to get the lists of dataframes
                OP_noti_message, OP_noti_order_details = process_order_notifications(driver=main_driver, orderIDs=orderIDs_new_openPosition)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if OP_noti_message:  # Check if noti_message is not empty
                    OP_noti_msg_df = pd.concat(OP_noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=new_open_position_df, name1="New Open Position", df2=OP_noti_msg_df, name2="Notification Order Message")

            with allure.step("Retrieve and compare New Open Position and Notification Order Details"):
                if OP_noti_order_details:  # Check if noti_order_details is not empty
                    OP_noti_order_df = pd.concat(OP_noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=new_open_position_df, name1="New Open Position",
                                   df2=OP_noti_order_df, name2="Notification Order Details")

            with allure.step("Print Final Result for Newly Created Order"):
                process_and_print_data(new_open_position_df, OP_noti_msg_df, OP_noti_order_df)
                
            """Comparison on Order History and newly closed order"""

            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type="history", section_name="Order History", row_number=[1])
            
                compare_dataframes(driver=main_driver, df1=asset_order_df, name1="Asset Open Position", df2=order_history_df, name2="Order History", compare_volume=False, compare_units=False)
                    
            with allure.step("Retrieve and compare Order History and Notification Order Message"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=asset_orderID)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_msg_df, name2="Notification Order Message", compare_profit_loss=True)

                # Concatenate all dataframes in the order_details_list into a single dataframe
                noti_order_df = pd.concat(noti_order_details, ignore_index=True)

            with allure.step("Retrieve and compare Order History and Notification Order Details"):
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_order_df, name2="Notification Order Details", compare_profit_loss=True)

            with allure.step("Print Final Result for Closed Order"):
                process_and_print_data(order_history_df, snackbar_banner_df, noti_msg_df, noti_order_df)
                    
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
