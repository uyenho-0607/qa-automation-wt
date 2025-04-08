import allure
import pytest
import pandas as pd

from enums.main import Server, Menu, TradeDirectionOption, SLTPOption, ButtonModuleType, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_sub_menu.utils import menu_button
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_market_order, modify_market_order, trade_orders_confirmation_details, get_trade_snackbar_banner, get_order_id, extract_order_info
from common.mobileapp.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data


@allure.parent_suite("MT4 Membersite - Android - Trade - Market Order")

@allure.epic("MT4 Android ts_ab - Market")

# Member Portal
class TC_aB02():

    @allure.title("TC_aB02")
        
    @allure.description(
        """
        Buy Order
        
        Member able to place a Market order with
        - Size
        
        Member able to modify a Market order with
        - Take Profit by Points

        """
    )
    
    def test_TC02(self, androidDriver):
        self.driver = androidDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)

        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT4)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver)

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, option=TradeDirectionOption.BUY)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df, _ = trade_orders_confirmation_details(driver=main_driver, trade_type=ButtonModuleType.TRADE)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.TRADE_OPEN_POSITION)

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
            
            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_confirmation_df, trade_snackbar_banner_df)

            """ End of Place Order """
            
            """ Start of Modify Order """

            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, tp_type=SLTPOption.POINTS)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                edit_tradeConfirmation_df, confirmation_orderID = trade_orders_confirmation_details(driver=main_driver, trade_type=ButtonModuleType.EDIT)
                
            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=edit_tradeConfirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Verify if it is the same orderIDs"):
                order_no = get_order_id(driver=main_driver)
                if confirmation_orderID != order_no:
                    assert False, f"Place orderID - {original_orderID} and retrieving orderID - {confirmation_orderID} not matched"
                     
            with allure.step("Retrieve the Order Panel data"):
                updated_orderID, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.UPDATED_OPEN_POSITION)

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Verify if it is the same orderIDs"):
                if original_orderID != updated_orderID:
                    assert False, f"Place orderID - {original_orderID} and Modified orderID - {updated_orderID} not matched"
                    
            with allure.step("Redirect to home page"):
                menu_button(driver=main_driver, menu=Menu.HOME)
            
            with allure.step("Retrieve and compare Open Position and Notification Order Message"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=original_orderID)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe

                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=noti_msg_df, name2=SectionName.NOTIFICATION_ORDER_MESSAGE)

            with allure.step("Retrieve and compare Open Position and Notification Order Details"):

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=noti_order_df, name2=SectionName.NOTIFICATION_ORDER_DETAIL)
                
            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(updated_order_df, edit_tradeConfirmation_df, edit_snackbar_banner_df, updated_order_df, noti_msg_df, noti_order_df)
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)