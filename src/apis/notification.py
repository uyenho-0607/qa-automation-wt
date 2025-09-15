from src.apis.api_base import BaseAPI
from src.data.enums import NotificationTab
from src.utils.logging_utils import logger

class NotificationAPI(BaseAPI):
    _counts_endpoint = "/notification/v1/summary"

    def __init__(self):
        super().__init__()

    def get_notification_counts(self, notification_type: NotificationTab = NotificationTab.ORDER):
        """
        Get current order counts of open positions or notifications
        :param notification_type: Notification type to filter by (default: ORDER)
        :type notification_type: NotificationTab
        :return: Return count of unread notifications for the specified type
        """
        logger.debug(f"[API] Get notification tab amount (Notification Tab:{notification_type.value})")
        resp = self.get(endpoint=self._counts_endpoint)
        return next((item["unread"] for item in resp if item["notificationType"] == notification_type.value.upper()), 0)
