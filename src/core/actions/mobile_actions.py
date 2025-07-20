import builtins
import time

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from src.core.actions.base_actions import BaseActions
from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT
from src.utils.logging_utils import logger


class MobileActions(BaseActions):
    def __init__(self, driver=None):
        super().__init__(driver or builtins.android_driver)

    @handle_stale_element
    def send_keys(
            self,
            locator: tuple[str, str], value,
            timeout=EXPLICIT_WAIT,
            raise_exception=True,
            show_log=True,
            hide_keyboard=True
    ):
        """Send keys to an element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if element and value is not None:
            element.clear()
            element.send_keys(str(value))

            if hide_keyboard:
                self.hide_keyboard()

    def get_content_desc(self, locator: tuple[str, str], timeout=EXPLICIT_WAIT):
        return self.get_attribute(locator, "content-desc", timeout=timeout)

    def hide_keyboard(self):
        """Hide the keyboard if it's visible."""
        try:
            self._driver.hide_keyboard()
        except Exception:
            try:
                # Some devices might need a different approach
                self._driver.execute_script("mobile: hideKeyboard")
            except Exception:
                # If both methods fail, try pressing back button
                self.press_back()

    def press_back(self):
        """Press device back button."""
        self._driver.press_keycode(4)  # Android back button keycode

    def press_done(self):
        """Press the Done button on mobile keyboard."""
        try:
            # Send IME action for Done
            self._driver.execute_script('mobile: performEditorAction', {'action': 'done'})
        except Exception:
            # Fallback to hiding keyboard if Done action fails
            self.hide_keyboard()


    def scroll_down(self, start_x_percent=0.85, scroll_step=0.4):
        """
        Scroll down the viewport using W3C actions.
        """
        try:
            # Get screen dimensions
            screen_size = self._driver.get_window_size()
            screen_width = screen_size['width']
            screen_height = screen_size['height']
            
            # Always start near the bottom (e.g., 85% of the screen height)
            start_x = screen_width // 2
            start_y = int(screen_height * start_x_percent)

            # Calculate end_y based on scroll_step, but don't go above 10% of the screen height
            scroll_distance = int(screen_height * scroll_step)
            end_y = max(int(screen_height * 0.1), start_y - scroll_distance)
            end_x = start_x
            
            # Setup finger input for W3C actions
            finger = PointerInput("touch", "finger1")
            actions = ActionBuilder(self._driver, mouse=finger)
            
            # Perform the scroll gesture
            actions.pointer_action.move_to_location(start_x, start_y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.pause(0.1)
            actions.pointer_action.move_to_location(end_x, end_y)
            actions.pointer_action.pause(0.1)
            actions.pointer_action.release()
            
            # Execute the action
            actions.perform()
            
            logger.debug(f"Successfully scrolled down viewport from ({start_x}, {start_y}) to ({end_x}, {end_y}) with step {scroll_step}")
        except Exception as e:
            logger.error(f"Failed to scroll down viewport: {str(e)}")
            raise

    # def scroll_direction(self, direction: str = "left", amount: int = 2):
    #     """
    #     Scroll on the screen in the specified direction.
    #     :param direction: "down" for vertical, "left" for horizontal
    #     :param amount: Number of times to scroll (only applies to "down")
    #     """
    #     try:
    #         if direction == "left":
    #             ui_automator = 'new UiScrollable(new UiSelector().scrollable(true).className("android.widget.HorizontalScrollView")).setAsHorizontalList().scrollForward()'
    #             self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_automator)
    #
    #         elif direction == "down":
    #             ui_automator = 'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()'
    #             for _ in range(amount):
    #                 self._driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_automator)
    #
    #         else:
    #             raise ValueError(f"Unsupported scroll direction: {direction}")
    #     except Exception as e:
    #         logger.error(f"Failed to perform scroll {direction}: {str(e)}")
    #         raise

    def swipe_picker_wheel_down(self, locator, swipe_percent=0.3):
        element = self.find_element(locator)
        rect = element.rect
        center_x = rect['x'] + rect['width'] // 2
        start_y = rect['y'] + rect['height'] * 0.7  # Start from 70% down the element
        end_y = rect['y'] + rect['height'] * 0.3  # End at 30% down the element

        # Setup finger input
        finger = PointerInput("touch", "finger1")
        actions = ActionBuilder(self._driver, mouse=finger)

        actions.pointer_action.move_to_location(center_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.2)
        actions.pointer_action.move_to_location(center_x, end_y)
        actions.pointer_action.release()
        actions.perform()

    def swipe_left_on_element(self, locator):
        element = self.find_element(locator)
        rect = element.rect

        # Setup finger input
        finger = PointerInput("touch", "finger1")
        actions = ActionBuilder(self._driver, mouse=finger)

        start_x = rect['x'] + rect['width'] * 0.95
        end_x = rect['x'] + rect['width'] * 0.25
        y = rect['y'] + rect['height'] / 2

        actions.pointer_action.move_to_location(start_x, y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.move_to_location(end_x, y)
        actions.pointer_action.release()
        actions.perform()
