import allure
import pandas as pd

from enums.main import Server, Menu, TradeConstants, TradeDirectionOption, SLTPOption, ButtonModuleType, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_sub_menu.utils import menu_button
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_market_order, close_delete_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from common.mobileapp.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data


@allure.parent_suite("MT5 Membersite - Android - Trade - Market Order")

@allure.epic("MT5 Android ts_ab - Market")

# Member Portal
class TC_aB18():

    @allure.title("TC_aB18")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Size
        - Stop Loss by Price
        - Take Profit by Points
        
        Member able to full close a Market order
        """
    )

    
    def test_tc18(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)

        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT5)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver)

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, option=TradeDirectionOption.SELL, trade_constants=TradeConstants.SET_FILL_POLICY, sl_type=SLTPOption.PRICE, tp_type=SLTPOption.POINTS)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_orders_confirmation_details(driver=main_driver, trade_type=ButtonModuleType.TRADE)

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.TRADE_OPEN_POSITION)

            """ End of Place Order """
            
            with allure.step("Order Panel: Open Position - Click on Close button"):
                close_delete_order(driver=main_driver, trade_type=ButtonModuleType.CLOSE, close_options=TradeConstants.SET_CLOSE_MARKET_SIZE | TradeConstants.SET_FILL_POLICY)

            with allure.step("Retrieve the closed order snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.HISTORY, section_name=SectionName.ORDER_HISTORY)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=order_history_df, name2=SectionName.ORDER_HISTORY)
            
            with allure.step("Redirect to home page"):
                menu_button(driver=main_driver, menu=Menu.HOME)
                
            with allure.step("Retrieve and compare Order History and Notification Order Message"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, order_ids=original_order_id)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1=SectionName.ORDER_HISTORY, df2=noti_msg_df, name2=SectionName.NOTIFICATION_ORDER_MESSAGE, compare_options=TradeConstants.COMPARE_PROFIT_LOSS)
    
            with allure.step("Retrieve and compare Order History and Notification Order Details"):
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1=SectionName.ORDER_HISTORY, df2=noti_order_df, name2=SectionName.NOTIFICATION_ORDER_DETAIL, compare_options=TradeConstants.COMPARE_PROFIT_LOSS)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, snackbar_banner_df, noti_msg_df, noti_order_df, order_history_df)
                        
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)