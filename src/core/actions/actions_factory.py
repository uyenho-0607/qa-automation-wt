from typing import Union, Optional

from src.core.actions.mobile_actions import MobileActions
from src.core.actions.web_actions import WebActions
from src.data.project_info import RuntimeConfig


class ActionsFactory:
    """Factory class for creating platform-specific action instances."""
    
    @staticmethod
    def create_actions(driver=None, platform: Optional[str] = None) -> Union[WebActions, MobileActions]:
        """Create appropriate actions instance based on platform.
        
        Args:
            driver: WebDriver instance
            platform: Platform type ('web', 'web_app', 'android', 'ios')
            
        Returns:
            Platform-specific actions instance
            
        Raises:
            ValueError: If platform is not supported
        """
        platform = platform or RuntimeConfig.platform
        
        match platform.lower():
            case "web" | "web_app":
                return WebActions(driver)
            case "android" | "ios":
                return MobileActions(driver)
            case _:
                raise ValueError(f"Unsupported platform: {platform}. Supported platforms: web, web_app, android, ios")