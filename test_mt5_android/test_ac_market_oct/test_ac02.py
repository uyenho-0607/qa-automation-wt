import allure
import pytest
import pandas as pd

from enums.main import Server, Menu, ModuleOCT, TradeDirectionOption, SLTPOption, OrderPanel, SectionName
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_sub_menu.utils import menu_button
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_oct_market_order, modify_market_order, get_trade_snackbar_banner, extract_order_info
from common.mobileapp.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Android - Trade - Market Order")

@allure.epic("MT5 Android ts_ac - Market OCT")

# Member Portal
class TC_aC02():

    @allure.title("TC_aC02")
        
    @allure.description(
        """
        Buy Order
        
        Member able to place a Market order with
        - Size
        
        Member able to modify a Market order with
        - Take Profit by Price

        """
    )

    def test_tc02(self, android_driver):
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

            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, desired_state=ModuleOCT.CHECKED)

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, option=TradeDirectionOption.BUY)

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.TRADE_OPEN_POSITION)

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)

            """ End of Place Order """

            """ Start of Modify Order """

            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, tp_type=SLTPOption.PRICE)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Order Panel data"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.UPDATED_OPEN_POSITION)
            
            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Verify if it is the same order_ids"):
                if original_order_id != updated_order_id:
                    assert False, f"Place orderID - {original_order_id} and Modified orderID - {updated_order_id} not matched"
                    
            with allure.step("Redirect to home page"):
                menu_button(driver=main_driver, menu=Menu.HOME)
            
            with allure.step("Retrieve and compare Open Position and Notification Order Message"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, order_ids=original_order_id)

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
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)
