import allure
import pytest

from enums.main import Server, ButtonModuleType, OrderExecutionType, TradeConstants, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_pending_order, close_delete_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Android - Trade - Limit Order")

@allure.epic("MT5 Andorid ts_ad - Limit")

# Member Portal
class TC_aD17():

        
    @allure.title("TC_aD17")

    @allure.description(
        """
        Buy Order
        
        Member able to place a Limit order with
        - Volume
        - Price
        - Stop Loss by Points
        - Expiry: Good Till Day
        
        Member able to delete a Limit order
        """
    )


    def test_tc17(self, android_driver):
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

            with allure.step("Place Limit Order"):
                trade_pending_order(driver=main_driver, order_type=OrderExecutionType.LIMIT, option=TradeDirectionOption.BUY, expiry_type=ExpiryType.GOOD_TILL_DAY, sl_type=SLTPOption.POINTS)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                _, pending_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.TRADE_PENDING_ORDER)

            """ End of Place Order """
                
            with allure.step("Order Panel: Pending Order - Click on Delete button"):
                close_delete_order(driver=main_driver, close_options=TradeConstants.DELETE_BUTTON)

            with allure.step("Retrieve the snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.ORDER_AND_DEALS, section_name=SectionName.ORDER_HISTORY)

                compare_dataframes(driver=main_driver, df1=pending_order_df, name1=SectionName.TRADE_PENDING_ORDER, df2=order_history_df, name2=SectionName.ORDER_HISTORY)

            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, snackbar_banner_df, order_history_df)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)