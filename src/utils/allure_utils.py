import base64
import glob
import json
import os
import time
from typing import Dict, Any

import allure

from src.data.consts import ROOTDIR, CHECK_ICON, FAILED_ICON, VIDEO_DIR
from src.data.project_info import StepLogs, ProjectConfig
from src.utils.logging_utils import logger


def save_recorded_video(video_raw):
    """Save recorded videos for android"""
    raw_path = os.path.join(VIDEO_DIR, f"test_video_{round(time.time())}.mp4")

    with open(raw_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    return raw_path


def attach_video(driver):
    """attach video to allure report"""
    if not ProjectConfig.is_web():
        video_data = driver.stop_recording_screen()
        video_path = save_recorded_video(video_data)
        allure.attach.file(
            video_path,
            name="Screen Recording",
            attachment_type=allure.attachment_type.MP4
        )


def attach_screenshot(driver, name="screenshot"):
    """attach screenshot to allure report"""
    try:
        allure.attach(driver.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        logger.error(f"Failed to capture screenshot: {str(e)}")


def log_step_to_allure():
    """Add recorded steps from logger to allure"""
    for item in StepLogs.test_steps:
        with allure.step(item):
            pass

    del StepLogs.test_steps[:]


def custom_allure_report(allure_dir: str) -> None:
    """Process and customize Allure test result files in the specified directory."""
    allure_dir_path = ROOTDIR / allure_dir
    allure_result_files = [f for f in os.listdir(allure_dir_path) if f.endswith("result.json")]  # get all allure result files
    files = [os.path.join(allure_dir_path, f) for f in allure_result_files]  # Sort result files based on created time (oldest first)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=False)

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Skip processing and delete file if test status is skipped
            if data.get("status") == "skipped":
                _remove_skipped_tests(file_path)
                continue

            _add_attachments_prop(data)  # add empty attachments prop for each test report
            _remove_zero_duration(data)
            _attach_table_details(data)  # add verify tables

            if data.get("status", "") == "failed":
                _process_failed_status(data)  # Process failed status if any

            elif data.get("status", "") == "broken":
                _process_broken_status(data)  # Process broken status if any

            _cleanup_and_customize_report(data)  # Clean up and customize report
            _add_check_icon(data)

            # Write back the modified data
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            logger.error(f"Error processing file {os.path.basename(file_path)}: {str(type(e).__name__)}, {str(e)}")
            continue


def _remove_skipped_tests(file_path):
    try:
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Error deleting skipped test file {os.path.basename(file_path)}: {str(e)}")


def _add_attachments_prop(data: Dict[str, Any]) -> None:
    for item in data.get("steps", []):
        item["attachments"] = []


def _process_failed_status(data: Dict[str, Any]) -> None:
    """Process failed test status and update steps."""
    if not data.get("steps"):
        return

    failed_logs = StepLogs.all_failed_logs[:]
    failed_attachments = list(filter(lambda x: x["name"] == "screenshot", data.get("attachments", [])))
    v_steps = [item for item in data["steps"]]

    should_break = False
    while failed_logs and not should_break:
        for failed_step, msg_detail in failed_logs:
            if failed_step == "end_test":
                StepLogs.all_failed_logs.pop(0)
                should_break = True
                break

            for index, v_step in enumerate(v_steps):
                step_name = v_step.get("name", "").lower()

                if step_name == failed_step.lower():
                    StepLogs.all_failed_logs.pop(0)

                    if "verify" in step_name:
                        v_step["status"] = "failed"
                        v_step["statusDetails"] = dict(message=msg_detail)
                        del v_steps[:index + 1]

                        # Attach screenshot if available
                        if failed_attachments:
                            v_step["attachments"].extend(failed_attachments[:1])
                            del failed_attachments[:1]

                        break  # Move to next failed_log after first match

                    else:  # this is a broken step
                        v_step["status"] = "broken"
                        data["status"] = "broken"
                        data["steps"][-1]["attachments"].extend(list(
                            filter(lambda x: x["name"] == "broken", data.get("attachments", []))
                        ))


def _process_broken_status(data: Dict[str, Any]) -> None:
    """Process broken test status and update steps."""
    if data.get("steps"):
        data["steps"][-1]["attachments"].extend(list(
            filter(lambda x: x["name"] == "broken", data.get("attachments", []))
        ))

    if data.get("steps"):
        data["steps"][-1]["status"] = "broken"


def _cleanup_and_customize_report(data: Dict[str, Any]) -> None:
    """Clean up attachments and customize report details."""
    # Clean up attachments and status details
    if data.get("attachments"):

        attachments = data["attachments"]
        data["attachments"] = [item for item in attachments if item["name"] in ["Screen Recording", "Chart Comparison Summary"]]

        if data.get("status") != "passed":
            data["attachments"].extend(
                [item for item in attachments if item["type"] == "text/plain"]
            )

    # Remove trace
    data.get("statusDetails", {}).pop("trace", None)

    # Customize test case name
    data["name"] = data["fullName"].split(".")[-1].replace("#test", "")
    data["name"] = " ".join(data["name"].split("_"))


def _add_check_icon(data):
    for item in data.get("steps", []):
        if "verify" in item["name"].lower():

            if item["status"] == "passed":
                item["name"] = f"{CHECK_ICON} {item['name']}"

            if item["status"] == "failed":
                item["name"] = f"{FAILED_ICON} {item['name']}"


def _remove_zero_duration(data: Dict[str, Any]):
    for item in data.get("steps", []):
        start = item.get("start", 0)
        stop = item.get("stop", 0)
        if stop == start:
            item["stop"] += 1


def _attach_table_details(data: Dict[str, Any]):
    table_attachments = list(
        filter(lambda x: "table" in x["name"].lower(), data.get("attachments", []))
    )

    for item in table_attachments:
        item["name"] = item["name"].split("-")[-1].strip()

    if not table_attachments:
        return

    for item in data.get("steps", []):
        if "verify" in item["name"].lower():
            matched = next((table for table in table_attachments if table["name"] == item["name"]), None)

            if matched:
                item["attachments"].append(matched)
                del table_attachments[:1]

                if not table_attachments:
                    break


def clean_allure_log_files(allure_dir):
    """
    Check and delete all .txt log files in the allure-results directory.
    This helps keep the test results clean and prevents accumulation of log files.
    """
    allure_results_dir = ROOTDIR / allure_dir
    if not os.path.exists(allure_dir):
        return

    # Find all .txt files in allure-results directory
    log_files = glob.glob(str(allure_results_dir / '*.txt'))

    # Delete each log file
    for log_file in log_files:
        try:
            os.remove(log_file)

        except Exception as e:
            logger.error(f"Error deleting log file {log_file}: {str(e)}")


def attach_verify_table(actual: dict, expected: dict, tolerance_percent: float = None, tolerance_fields: list = None, title="Table Details", comparison_result: dict = None):
    """
    Attach a dynamic HTML table to Allure report.
    
    Args:
        actual: Actual dictionary
        expected: Expected dictionary  
        tolerance_percent: Tolerance percentage for comparison
        tolerance_fields: List of fields to apply tolerance to
        title: Title for the table attachment
        comparison_result: Optional pre-calculated comparison result to avoid re-computation
    """

    res = comparison_result

    # Use provided comparison result or calculate it
    # if comparison_result is not None:
    #     res = comparison_result
    # else:
    #     res = compare_dict(actual, expected, tolerance_percent=tolerance_percent, tolerance_fields=tolerance_fields)
    
    tolerance_info = res.get("tolerance_info", {})
    
    # Determine if we should show tolerance columns
    show_tolerance = tolerance_percent is not None and tolerance_fields

    html = """
        <style>
            table {
                border-collapse: collapse;
                width: 90%;
                font-family: Arial, sans-serif;
                margin: 10px 0;
                table-layout: fixed;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 6px 10px;
                text-align: center;
                vertical-align: middle;
                font-size: 13px;
                word-break: break-all;
            }
            th {
                background-color: #f2f2f2;
            }
            .highlight {
                background-color: #ffcccc;
                font-weight: bold;
            }
            .tolerance-info {
                font-size: 11px; 
            }
            .tolerance-pass {
                background-color: #d4edda;
                color: #155724;
            }
            .tolerance-fail {
                background-color: #f8d7da;
                color: #721c24;
            }
            .missing {
                background-color: #f8d7da;
                color: #721c24;
            }
            .redundant {
                background-color: #f8d7da;
                color: #721c24;
            }
        </style>
        <table>
        <thead>
            <tr>
                <th>Compare Field</th>
                <th>Actual</th>
                <th>Expected</th>"""

    if show_tolerance:
        html += """
                <th>Tolerance</th>
                <th>Diff %</th>"""

    html += """
            </tr>
        </thead>
        <tbody>
        """

    # Get all keys from both dictionaries
    all_keys = sorted(set(actual.keys()) | set(expected.keys()))

    for key in all_keys:
        actual_val = actual.get(key, "")
        expected_val = expected.get(key, "")
        
        # Check field status using compare_dict results
        is_missing = key in res.get("missing", [])
        is_redundant = key in res.get("redundant", [])
        is_different = key in res.get("diff", [])
        has_tolerance = key in tolerance_info
        
        # Determine highlight class based on field status
        if is_missing:
            highlight_class = "missing"
            actual_val = "MISSING"
        elif is_redundant:
            highlight_class = "redundant"
            expected_val = "REDUNDANT"
        elif has_tolerance:
            tolerance_data = tolerance_info[key]
            diff_percent = float(tolerance_data["diff_percent"])
            
            # Only highlight if there's an actual difference (diff > 0)
            if diff_percent > 0:
                if diff_percent <= tolerance_percent:
                    highlight_class = "tolerance-pass"
                else:
                    highlight_class = "tolerance-fail"
            else:
                # Values are exactly the same, no highlighting needed
                highlight_class = ""
        elif is_different:
            highlight_class = "highlight"
        else:
            highlight_class = ""

        html += f"""
            <tr>
                <td>{' '.join(item.capitalize() for item in key.split('_'))}</td>
                <td class="{highlight_class}">{actual_val}</td>
                <td class="{highlight_class}">{expected_val}</td>"""

        if show_tolerance:
            if has_tolerance:
                tolerance_data = tolerance_info[key]
                html += f"""
                <td class="tolerance-info">{tolerance_data["tolerance"]}</td>
                <td class="tolerance-info">{tolerance_data["diff_percent"]}</td>"""
            else:
                html += """
                <td class="tolerance-info">-</td>
                <td class="tolerance-info">-</td>"""

        html += """
            </tr>
            """

    html += "</table>"
    allure.attach(html, name=title, attachment_type=allure.attachment_type.HTML)


# def log_comparison_step(step_name: str, actual: dict, expected: dict, tolerance_percent: float = None, tolerance_fields: list = None, comparison_result: dict = None):
#     """
#     Log comparison results as Allure steps instead of HTML attachments.
    
#     Args:
#         step_name: Name of the comparison step
#         actual: Actual dictionary
#         expected: Expected dictionary  
#         tolerance_percent: Tolerance percentage for comparison
#         tolerance_fields: List of fields to apply tolerance to
#         comparison_result: Optional pre-calculated comparison result
#     """
#     with allure.step(f"Compare {step_name}"):
#         # Use provided comparison result or calculate it
#         if comparison_result is not None:
#             res = comparison_result
#         else:
#             res = compare_dict(actual, expected, tolerance_percent=tolerance_percent, tolerance_fields=tolerance_fields)
        
#         # Log the comparison result
#         allure.attach(
#             f"Comparison Result: {'PASS' if res['res'] else 'FAIL'}",
#             name="Comparison Status",
#             attachment_type=allure.attachment_type.TEXT
#         )
        
#         # Log tolerance information if applicable
#         if tolerance_percent and tolerance_fields:
#             tolerance_info = res.get("tolerance_info", {})
#             tolerance_text = f"Tolerance: {tolerance_percent}%\nTolerance Fields: {', '.join(tolerance_fields)}\n\n"
            
#             for field, info in tolerance_info.items():
#                 tolerance_text += f"{field}:\n"
#                 tolerance_text += f"  Actual: {info.get('actual')}\n"
#                 tolerance_text += f"  Expected: {info.get('expected')}\n"
#                 tolerance_text += f"  Difference: {info.get('difference')}\n"
#                 tolerance_text += f"  Status: {'PASS' if info.get('pass') else 'FAIL'}\n\n"
            
#             allure.attach(
#                 tolerance_text,
#                 name="Tolerance Details",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         # Log detailed field-by-field comparison
#         detailed_comparison = "Field-by-Field Comparison:\n"
#         for field, info in res.get("field_comparison", {}).items():
#             detailed_comparison += f"\n{field}:\n"
#             detailed_comparison += f"  Actual: {info.get('actual')}\n"
#             detailed_comparison += f"  Expected: {info.get('expected')}\n"
#             detailed_comparison += f"  Match: {'✓' if info.get('match') else '✗'}\n"
        
#         allure.attach(
#             detailed_comparison,
#             name="Detailed Comparison",
#             attachment_type=allure.attachment_type.TEXT
#         )


# def log_notification_comparison_from_component(actual_notification: str, expected_notification: str, tolerance_percent: float = 0.01):
#     """
#     Log notification comparison results as Allure steps.
#     This function is designed to be called from notification components to avoid circular imports.
    
#     Args:
#         actual_notification: Actual notification text
#         expected_notification: Expected notification text
#         tolerance_percent: Tolerance percentage for price comparison
#     """
#     with allure.step("Compare Notification Messages"):
#         # Import here to avoid circular import
#         from src.utils.notification_utils import extract_prices
        
#         # Extract prices from both notifications
#         actual_prices = extract_prices(actual_notification)
#         expected_prices = extract_prices(expected_notification)
        
#         # Log the notification texts
#         allure.attach(
#             f"Actual Notification:\n{actual_notification}\n\nExpected Notification:\n{expected_notification}",
#             name="Notification Texts",
#             attachment_type=allure.attachment_type.TEXT
#         )
        
#         # Log extracted prices
#         if actual_prices:
#             actual_prices_text = "Extracted Prices from Actual:\n"
#             for key, value in actual_prices.items():
#                 actual_prices_text += f"  {key}: {value}\n"
#             allure.attach(
#                 actual_prices_text,
#                 name="Actual Prices",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         if expected_prices:
#             expected_prices_text = "Extracted Prices from Expected:\n"
#             for key, value in expected_prices.items():
#                 expected_prices_text += f"  {key}: {value}\n"
#             allure.attach(
#                 expected_prices_text,
#                 name="Expected Prices",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         # Log price comparison if both have prices
#         if actual_prices and expected_prices:
#             price_comparison = "Price Comparison:\n"
#             for key in set(actual_prices.keys()) | set(expected_prices.keys()):
#                 actual_val = actual_prices.get(key, "N/A")
#                 expected_val = expected_prices.get(key, "N/A")
#                 if actual_val != "N/A" and expected_val != "N/A":
#                     diff = abs(actual_val - expected_val)
#                     tolerance = expected_val * tolerance_percent
#                     status = "PASS" if diff <= tolerance else "FAIL"
#                     price_comparison += f"  {key}: {actual_val} vs {expected_val} (diff: {diff:.6f}, tolerance: {tolerance:.6f}) - {status}\n"
#                 else:
#                     price_comparison += f"  {key}: {actual_val} vs {expected_val} - SKIP\n"
            
#             allure.attach(
#                 price_comparison,
#                 name="Price Comparison",
#                 attachment_type=allure.attachment_type.TEXT
#             )


# def log_test_data(data_name: str, data: dict, description: str = ""):
#     """
#     Log test data as Allure step with structured information.
    
#     Args:
#         data_name: Name of the data being logged
#         data: Dictionary containing the data
#         description: Optional description
#     """
#     with allure.step(f"Test Data: {data_name}"):
#         if description:
#             allure.attach(
#                 description,
#                 name="Description",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         # Format data as readable text
#         data_text = ""
#         for key, value in data.items():
#             if isinstance(value, dict):
#                 data_text += f"\n{key}:\n"
#                 for sub_key, sub_value in value.items():
#                     data_text += f"  {sub_key}: {sub_value}\n"
#             else:
#                 data_text += f"{key}: {value}\n"
        
#         allure.attach(
#             data_text,
#             name=f"{data_name} Data",
#             attachment_type=allure.attachment_type.TEXT
#         )


# def log_api_response(response_data: dict, endpoint: str = "", status_code: int = None):
#     """
#     Log API response details as Allure step.
    
#     Args:
#         response_data: API response data
#         endpoint: API endpoint that was called
#         status_code: HTTP status code
#     """
#     with allure.step(f"API Response: {endpoint}"):
#         if status_code:
#             allure.attach(
#                 f"Status Code: {status_code}",
#                 name="HTTP Status",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         # Log response headers if available
#         if isinstance(response_data, dict) and 'headers' in response_data:
#             headers_text = "Response Headers:\n"
#             for key, value in response_data['headers'].items():
#                 headers_text += f"  {key}: {value}\n"
#             allure.attach(
#                 headers_text,
#                 name="Response Headers",
#                 attachment_type=allure.attachment_type.TEXT
#             )
        
#         # Log response body
#         if isinstance(response_data, dict) and 'body' in response_data:
#             body = response_data['body']
#         else:
#             body = response_data
        
#         if isinstance(body, dict):
#             body_text = "Response Body:\n"
#             for key, value in body.items():
#                 body_text += f"{key}: {value}\n"
#         else:
#             body_text = f"Response Body:\n{body}"
        
#         allure.attach(
#             body_text,
#             name="Response Body",
#             attachment_type=allure.attachment_type.TEXT
#         )


# def log_error_details(error_message: str, error_type: str = "Error", additional_info: dict = None):
#     """
#     Log error details as Allure step with structured information.
    
#     Args:
#         error_message: The error message
#         error_type: Type of error (Error, Warning, Info)
#         additional_info: Additional error context
#     """
#     with allure.step(f"{error_type}: {error_message[:50]}..."):
#         allure.attach(
#             error_message,
#             name="Error Message",
#             attachment_type=allure.attachment_type.TEXT
#         )
        
#         if additional_info:
#             info_text = "Additional Information:\n"
#             for key, value in additional_info.items():
#                 info_text += f"{key}: {value}\n"
#             allure.attach(
#                 info_text,
#                 name="Error Context",
#                 attachment_type=allure.attachment_type.TEXT
#             )


# def log_performance_metrics(metrics: dict, test_name: str = ""):
#     """
#     Log performance metrics as Allure step.
    
#     Args:
#         metrics: Dictionary containing performance metrics
#         test_name: Name of the test for context
#     """
#     with allure.step(f"Performance Metrics: {test_name}"):
#         metrics_text = "Performance Metrics:\n"
#         for metric_name, value in metrics.items():
#             if isinstance(value, (int, float)):
#                 metrics_text += f"{metric_name}: {value:.2f}\n"
#             else:
#                 metrics_text += f"{metric_name}: {value}\n"
        
#         allure.attach(
#             metrics_text,
#             name="Performance Data",
#             attachment_type=allure.attachment_type.TEXT
#         )


# def log_environment_info():
#     """Log current environment information as Allure step."""
#     with allure.step("Environment Information"):
#         env_info = f"""
# Platform: {ProjectConfig.platform}
# Environment: {ProjectConfig.env}
# Client: {ProjectConfig.client}
# Server: {ProjectConfig.server}
# Account Type: {ProjectConfig.account_type}
#         """.strip()
        
#         allure.attach(
#             env_info,
#             name="Environment Details",
#             attachment_type=allure.attachment_type.TEXT
#         )


# def log_comprehensive_test_info(test_name: str, test_data: dict, api_responses: list = None, errors: list = None, performance_metrics: dict = None):
#     """
#     Comprehensive logging function that demonstrates all Allure utilities.
    
#     Args:
#         test_name: Name of the test
#         test_data: Test input data
#         api_responses: List of API responses during test
#         errors: List of errors encountered
#         performance_metrics: Performance metrics
#     """
#     with allure.step(f"Test Execution: {test_name}"):
#         # Log environment information
#         log_environment_info()
        
#         # Log test data
#         if test_data:
#             log_test_data("Input", test_data, "Test input parameters and configuration")
        
#         # Log API responses
#         if api_responses:
#             for i, response in enumerate(api_responses):
#                 endpoint = response.get('endpoint', f'API Call {i+1}')
#                 status_code = response.get('status_code')
#                 log_api_response(response, endpoint, status_code)
        
#         # Log errors
#         if errors:
#             for error in errors:
#                 error_msg = error.get('message', 'Unknown error')
#                 error_type = error.get('type', 'Error')
#                 additional_info = error.get('context', {})
#                 log_error_details(error_msg, error_type, additional_info)
        
#         # Log performance metrics
#         if performance_metrics:
#             log_performance_metrics(performance_metrics, test_name)


# # Example usage in tests:
# """
# # Instead of HTML attachments, use these functions:

# # 1. For comparison results:
# log_comparison_step(
#     "Trade Data", 
#     actual_trade_data, 
#     expected_trade_data, 
#     tolerance_percent=0.01, 
#     tolerance_fields=["price", "volume"]
# )

# # 2. For notification comparisons:
# log_notification_comparison(actual_notification, expected_notification, 0.01)

# # 3. For test data:
# log_test_data("Trade Order", trade_order_data, "Order details for the test")

# # 4. For API responses:
# log_api_response(api_response, "/api/trade", 200)

# # 5. For errors:
# log_error_details("Connection timeout", "Warning", {"retry_count": 3, "timeout": 30})

# # 6. For performance:
# log_performance_metrics({"response_time": 1.5, "memory_usage": 256}, "Trade API Test")

# # 7. Comprehensive logging:
# log_comprehensive_test_info(
#     "Trade Order Test",
#     {"symbol": "EURUSD", "volume": 0.1, "type": "BUY"},
#     [{"endpoint": "/api/order", "status_code": 200, "body": {"order_id": "123"}}],
#     [{"message": "Price slightly different", "type": "Warning", "context": {"tolerance": 0.01}}],
#     {"response_time": 1.2, "order_processing_time": 0.8}
# )
# """


# # Practical Example: Replacing HTML table with text-based reporting
# """
# # OLD WAY (HTML attachment):
# def test_trade_comparison():
#     actual_data = {"price": 1.2345, "volume": 0.1}
#     expected_data = {"price": 1.2340, "volume": 0.1}
    
#     # This creates an HTML table attachment
#     attach_verify_table(actual_data, expected_data, 0.01, ["price"])

# # NEW WAY (Text-based with Allure steps):
# def test_trade_comparison():
#     actual_data = {"price": 1.2345, "volume": 0.1}
#     expected_data = {"price": 1.2340, "volume": 0.1}
    
#     # Add test metadata
#     add_test_description("Verify trade data matches expected values with tolerance", "TC-123", "critical")
#     add_test_labels(feature="Trading", story="Order Placement", tags=["regression", "trading"])
    
#     # Log comparison using new utility
#     log_comparison_step(
#         "Trade Data", 
#         actual_data, 
#         expected_data, 
#         tolerance_percent=0.01, 
#         tolerance_fields=["price"]
#     )
    
#     # Log individual verifications
#     log_verification_result("Price", actual_data["price"], expected_data["price"], 
#                           abs(actual_data["price"] - expected_data["price"]) <= 0.01, 0.01)
#     log_verification_result("Volume", actual_data["volume"], expected_data["volume"], 
#                           actual_data["volume"] == expected_data["volume"])

# # Benefits of the new approach:
# # 1. Better searchability in Allure reports
# # 2. Structured information in test steps
# # 3. No HTML parsing required
# # 4. Better integration with Allure's filtering and categorization
# # 5. More readable in the Allure UI
# # 6. Easier to maintain and modify
# """


# def add_test_description(description: str, test_case_id: str = None, severity: str = "normal"):
#     """
#     Add test description and metadata using Allure's built-in features.
    
#     Args:
#         description: Test description
#         test_case_id: Test case ID for linking
#         severity: Test severity (blocker, critical, normal, minor, trivial)
#     """
#     # Add description
#     allure.dynamic.description(description)
    
#     # Add test case ID as link if provided
#     if test_case_id:
#         allure.dynamic.link(
#             url=f"https://your-test-management-system.com/testcase/{test_case_id}",
#             name=f"Test Case {test_case_id}",
#             link_type=allure.link_type.TEST_CASE
#         )
    
#     # Add severity
#     severity_map = {
#         "blocker": allure.severity_level.BLOCKER,
#         "critical": allure.severity_level.CRITICAL,
#         "normal": allure.severity_level.NORMAL,
#         "minor": allure.severity_level.MINOR,
#         "trivial": allure.severity_level.TRIVIAL
#     }
#     allure.dynamic.severity(severity_map.get(severity.lower(), allure.severity_level.NORMAL))


# def add_test_labels(feature: str = None, story: str = None, epic: str = None, tags: list = None):
#     """
#     Add test labels and categorization using Allure's built-in features.
    
#     Args:
#         feature: Feature name
#         story: Story name
#         epic: Epic name
#         tags: List of custom tags
#     """
#     if feature:
#         allure.dynamic.feature(feature)
    
#     if story:
#         allure.dynamic.story(story)
    
#     if epic:
#         allure.dynamic.epic(epic)
    
#     if tags:
#         for tag in tags:
#             allure.dynamic.tag(tag)


# def log_step_with_parameters(step_name: str, parameters: dict):
#     """
#     Log a step with parameters in a structured way.
    
#     Args:
#         step_name: Name of the step
#         parameters: Dictionary of parameters
#     """
#     with allure.step(step_name):
#         if parameters:
#             params_text = "Parameters:\n"
#             for key, value in parameters.items():
#                 params_text += f"  {key}: {value}\n"
#             allure.attach(
#                 params_text,
#                 name="Step Parameters",
#                 attachment_type=allure.attachment_type.TEXT
#             )


# def log_verification_result(verification_name: str, actual: any, expected: any, passed: bool, tolerance: float = None):
#     """
#     Log verification results in a structured way.
    
#     Args:
#         verification_name: Name of the verification
#         actual: Actual value
#         expected: Expected value
#         passed: Whether verification passed
#         tolerance: Tolerance value if applicable
#     """
#     with allure.step(f"Verify {verification_name}"):
#         result_text = f"Verification: {verification_name}\n"
#         result_text += f"Status: {'PASS' if passed else 'FAIL'}\n"
#         result_text += f"Actual: {actual}\n"
#         result_text += f"Expected: {expected}\n"
        
#         if tolerance is not None:
#             result_text += f"Tolerance: {tolerance}\n"
        
#         if not passed:
#             if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
#                 diff = abs(actual - expected)
#                 result_text += f"Difference: {diff}\n"
        
#         allure.attach(
#             result_text,
#             name="Verification Details",
#             attachment_type=allure.attachment_type.TEXT
#         )


#
#
# def split_by_separator(data, separator=('end_test', '')):
#     chunks = []
#     current = []
#     for item in data:
#         if item == separator:
#             if current:
#                 chunks.append(current)
#                 current = []
#         else:
#             current.append(item)
#
#     if current:
#         chunks.append(current)
#
#     return chunks
