class UIMessages:
    """Constants for all UI text messages including error messages, notifications, and popup text"""

    # ===== Authentication Messages =====
    # Login
    LOGIN_INVALID_CREDENTIALS = "Invalid credentials, please try again"
    LOGIN_INVALID = "Invalid Login"
    NEW_LOGIN_DETECTED = "New Login Detected"
    REVIEW_LINKED_DEVICE = "Review Linked Device if this is not you"

    # Password Management
    PASSWORD_INVALID_FORMAT = (
        "Password format is incorrect. Password must include at least 12-20 characters, "
        "including 1 capital letter, 1 small letter, 1 number, 1 special characters."
    )
    PASSWORD_CONFIRMATION_MISMATCH = "New password does not match confirm password"
    PASSWORD_CURRENT_INVALID = "Invalid current password"
    PASSWORD_SAME_AS_OLD = "New password and old password are the same"
    PASSWORD_PREVIOUSLY_USED = "New password cannot be the same as previous 5 old password"
    FORGOT_PASSWORD_DES = (
        "An email has been sent to your registered account to reset your password. "
        "If you have not received it, please contact our support team."
    )

    # ===== Form Validation Messages =====
    IS_REQUIRED = "{} is required"
    ACCEPT_TERM_CONDITION = "Please review and accept the Terms and Conditions"
    EMAIL_FORMAT_INVALID = "Email format invalid"
    PHONE_NUMBER_INVALID = "Phone number is invalid"

    # ===== Order Management Messages =====
    # Order Submission
    ORDER_SUBMITTED_BANNER_TITLE = "{} Order Submitted"
    ORDER_PLACED_BANNER_DES = "{} - {} ORDER placed, Volume: {} / Units: {}."
    ORDER_UPDATED_BANNER_TITLE = "{} Order Updated"
    ORDER_UPDATED_BANNER_DES = "{} - {} ORDER updated, Volume: {} / Units: {}."

    # Order Validation
    INVALID_ORDER_BANNER_TITLE = "Invalid order"
    INVALID_SL_TP_BANNER_DES = "Invalid Stop loss or Take profit"
    INVALID_PRICE_BANNER_DES = "Invalid Price submitted"

    # Position Management
    OPEN_POSITION_NOTI_RESULT = "Open Position: #{} {}: Volume {} / Units {} @ {}"
    NO_OPEN_POSITION = "No open positions for {}"
    NO_PENDING_POSITION = "No pending orders for {}"

    # Order Closure
    CLOSE_ORDER_BANNER_TITLE = "Close Order"
    CLOSE_ORDER_BANNER_DES = "{} - {} order closed successfully."
    POSITION_CLOSED_NOTI_RESULT = "Position Closed: #{} {}: Volume {} / Units {} @ {}"
    BULK_CLOSE_OP_BANNER_TITLE = "Bulk closure of open positions"

    # Order Deletion
    DELETE_ORDER_BANNER_TITLE = "Delete Order"
    DELETE_ORDER_BANNER_DES = "{} - {} order deleted successfully."
    BULK_DELETE_BANNER_TITLE = "Bulk deletion of pending orders"
    BULK_DELETE_BANNER_DES = "Pending orders #{}, #{}, #{} and {} others have been deleted."

    # ===== General UI Messages =====
    HELP_ON_THE_WAY = "Help is on the way!"
    ALL_CHANGES_SAVED = "All changes are saved."
    DEMO_ACCOUNT_READY = "Your Demo Account is Ready!"
    DEMO_ACCOUNT_OPEN_SUCCESS = "Your demo account has been opened successfully."
    NO_ITEM_AVAILABLE = "No items available"
    TYPE_SOMETHING_TO_SEARCH = "Type something to search"
