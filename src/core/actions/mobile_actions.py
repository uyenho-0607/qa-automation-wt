import builtins

from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

from src.core.actions.base_actions import BaseActions
from src.core.decorators import handle_stale_element
from src.data.consts import EXPLICIT_WAIT


class MobileActions(BaseActions):
    """Mobile-specific actions implementation."""
    
    def __init__(self, driver=None):
        super().__init__(driver or builtins.android_driver)

    @handle_stale_element
    def send_keys(
            self,
            locator: tuple[str, str], 
            value: str,
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True,
            hide_keyboard: bool = True
    ) -> None:
        """Send keys to an element."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if element and value is not None:
            element.click()
            element.clear()
            element.send_keys(str(value))
            
            if hide_keyboard:
                self.hide_keyboard()

    def get_content_desc(self, locator: tuple[str, str], timeout: float | int = EXPLICIT_WAIT) -> str:
        """Get content description attribute from element."""
        return self.get_attribute(locator, "content-desc", timeout=timeout) or ""

    def hide_keyboard(self) -> None:
        """Hide the keyboard if it's visible."""
        try:
            self._driver.hide_keyboard()
        except Exception:
            try:
                self._driver.execute_script("mobile: hideKeyboard")
            except Exception:
                self.press_back()

    def press_back(self) -> None:
        """Press device back button."""
        self._driver.press_keycode(4)

    def press_done(self) -> None:
        """Press the Done button on mobile keyboard."""
        try:
            self._driver.execute_script('mobile: performEditorAction', {'action': 'done'})
        except Exception:
            self.hide_keyboard()

    def scroll_down(self, start_x_percent: float = 0.85, scroll_step: float = 0.4) -> None:
        """Scroll down the viewport using W3C actions."""
        screen_size = self._driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']
        
        start_x = screen_width // 2
        start_y = int(screen_height * start_x_percent)
        scroll_distance = int(screen_height * scroll_step)
        end_y = max(int(screen_height * 0.1), start_y - scroll_distance)
        
        self._perform_swipe_action(start_x, start_y, start_x, end_y)

    def swipe_picker_wheel_down(self, locator: tuple[str, str]) -> None:
        """Swipe picker wheel down."""
        element = self.find_element(locator)
        if not element:
            return
            
        rect = element.rect
        center_x = rect['x'] + rect['width'] // 2
        start_y = rect['y'] + rect['height'] * 0.7
        end_y = rect['y'] + rect['height'] * 0.3
        
        self._perform_swipe_action(center_x, start_y, center_x, end_y, pause_duration=0.2)

    def swipe_element_horizontal(self, locator: tuple[str, str], direction: str = "left") -> None:
        """Perform horizontal swipe on an element."""
        element = self.find_element(locator)
        if not element:
            return
            
        rect = element.rect
        y = rect['y'] + rect['height'] / 2
        
        if direction == "left":
            start_x = rect['x'] + rect['width'] * 0.95
            end_x = rect['x'] + rect['width'] * 0.25
        else:
            start_x = rect['x'] + rect['width'] * 0.25
            end_x = rect['x'] + rect['width'] * 0.95
        
        self._perform_swipe_action(start_x, y, end_x, y)

    def click_by_offset(
            self,
            locator: tuple[str, str],
            x_offset: int = 0,
            y_offset: int = 0,
            timeout: float | int = EXPLICIT_WAIT,
            raise_exception: bool = True,
            show_log: bool = True
    ) -> None:
        """Click on an element by offset (mobile implementation)."""
        element = self.find_element(locator, timeout, raise_exception=raise_exception, show_log=show_log)
        if element:
            rect = element.rect
            click_x = rect['x'] + rect['width'] // 2 + x_offset
            click_y = rect['y'] + rect['height'] // 2 + y_offset
            
            finger = PointerInput("touch", "finger1")
            actions = ActionBuilder(self._driver, mouse=finger)
            actions.pointer_action.move_to_location(click_x, click_y)
            actions.pointer_action.pointer_down()
            actions.pointer_action.pointer_up()
            actions.perform()

    # ------- PRIVATE HELPER METHODS ------ #
    def _perform_swipe_action(
            self, 
            start_x: float, 
            start_y: float, 
            end_x: float, 
            end_y: float, 
            pause_duration: float = 0.1
    ) -> None:
        """Perform a swipe action with given coordinates."""
        finger = PointerInput("touch", "finger1")
        actions = ActionBuilder(self._driver, mouse=finger)
        
        actions.pointer_action.move_to_location(start_x, start_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(pause_duration)
        actions.pointer_action.move_to_location(end_x, end_y)
        actions.pointer_action.pause(pause_duration)
        actions.pointer_action.release()
        
        actions.perform()