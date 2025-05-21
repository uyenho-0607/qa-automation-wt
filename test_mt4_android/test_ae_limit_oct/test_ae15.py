import allure
import pytest

from enums.main import Server, ModuleOCT, OrderExecutionType, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_pending_order, modify_pending_order, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Android - Trade - Limit Order")

@allure.epic("MT4 Andorid ts_ae - Limit OCT")

# Member Portal
class TC_MT4_aE15():

    @allure.title("TC_MT4_aE15")
    
    @allure.description(
        """
        Sell Order
        
        Member able to place a Limit order with
        - Size
        - Price
        - Stop Loss by Price
        - Take Profit by Points
        - Expiry: Good Till Day

        Member able to modify a Limit order with
        - Price
        - Stop Loss by Points
        - Take Profit by Price
        - Expiry: Good Till Cancelled
        """
    )

    def test_tc15(self, android_driver):
        self.driver = android_driver
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

            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, desired_state=ModuleOCT.CHECKED)

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_pending_order(driver=main_driver, order_type=OrderExecutionType.LIMIT, option=TradeDirectionOption.SELL, sl_type=SLTPOption.PRICE, tp_type=SLTPOption.POINTS, expiry_type=ExpiryType.GOOD_TILL_DAY)

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.TRADE_PENDING_ORDER)

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_PENDING_ORDER, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ End of Place Order """
            
            """ Start of Modify Order """

            with allure.step("Modify on Limit Order"):
                modify_pending_order(driver=main_driver, order_type=OrderExecutionType.LIMIT, sl_type=SLTPOption.POINTS, tp_type=SLTPOption.PRICE, expiry_type=ExpiryType.GOOD_TILL_CANCELLED)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.UPDATED_PENDING_ORDER)

            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_PENDING_ORDER, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                    
            with allure.step("Verify if it is the same order_ids"):
                if original_order_id == updated_order_id:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_order_id} and Modified orderID - {updated_order_id} not matched"

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)