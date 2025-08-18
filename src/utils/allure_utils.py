import base64
import glob
import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Dict, Any

import allure
from pytest_selenium import driver

from src.data.consts import GRID_VIDEO_URL
from src.data.consts import ROOTDIR, CHECK_ICON, FAILED_ICON, VIDEO_DIR
from src.data.project_info import DriverList
from src.data.project_info import StepLogs, RuntimeConfig
from src.utils.common_utils import convert_timestamp
from src.utils.logging_utils import logger


def attach_session_video():
    driver = DriverList.all_drivers.get(RuntimeConfig.platform.lower())
    if driver:
        # s3_video_url = f'<a href="{GRID_VIDEO_URL}/{Config.config.env}/videos/{driver.session_id}.mp4">Session Video</a>'
        s3_video_url = f'<a href="{GRID_VIDEO_URL}/videos/{driver.session_id}.mp4">Session Video</a>'
        allure.attach(s3_video_url, name="Screen Recording", attachment_type=allure.attachment_type.HTML)


def save_recorded_video(video_raw):
    """Save recorded videos for android"""
    raw_path = os.path.join(VIDEO_DIR, f"test_video_{round(time.time())}.mp4")

    with open(raw_path, "wb") as f:
        f.write(base64.b64decode(video_raw))

    return raw_path


def attach_video(driver):
    """attach video to allure report"""
    if not RuntimeConfig.is_web():
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

    # clean all log files
    _clean_log_files(allure_dir)

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
            _attach_verify_details(data) # add verify details text

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
                        # data["status"] = "broken"
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
        data["attachments"] = [item for item in attachments if item["name"] in ["Screen Recording", "Screen Recording Link", "Chart Comparison Summary" , "setup"]]

        if data.get("status") != "passed":
            data["attachments"].extend(
                [item for item in attachments if item["type"] == "text/plain" and item["name"] == "log"]
            )

    # Remove trace
    data.get("statusDetails", {}).pop("trace", None)

    # Customize test case name
    data["name"] = data["fullName"].split(".")[-1].replace("#test", "")
    data["name"] = " ".join(data["name"].split("_"))

    # Customize test's properties
    data["fullName"] = f"{data['fullName']}[{RuntimeConfig.client}][{RuntimeConfig.server}]"
    data["historyId"] = uuid.uuid4().hex


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

def _attach_verify_details(data: Dict[str, Any]):
    detail_attachments = list(
        filter(lambda x: "verification details" in x["name"].lower(), data.get("attachments", []))
    )

    for item in detail_attachments:
        item["name"] = item["name"].split("-")[-1].strip()

    if not detail_attachments:
        return

    for item in data.get("steps", []):
        if "verify" in item["name"].lower():
            matched = next((table for table in detail_attachments if table["name"] == item["name"]), None)

            if matched:
                item["attachments"].append(matched)
                del detail_attachments[:1]

                if not detail_attachments:
                    break


def _clean_log_files(allure_dir):

    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    logger_prefix = re.compile(r'pythonLog:[^:\s]+\.py:\d+\s*-?\s*')
    allure_results_dir = ROOTDIR / allure_dir

    for txt_file in Path(allure_results_dir).glob("*.txt"):
        content = txt_file.read_text(encoding="utf-8")
        # Remove ANSI colors
        content = ansi_escape.sub('', content)
        # Remove pythonLog:filename.py:line
        content = logger_prefix.sub('', content)
        txt_file.write_text(content, encoding="utf-8")


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

        if "_date" in key:
            # convert back to str time for human-readable
            actual_val = convert_timestamp(actual.get(key)) if actual_val else ""
            expected_val = convert_timestamp(expected.get(key)) if expected_val else ""

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
            diff_percent = float(tolerance_data["diff_percent"]) if tolerance_data["diff_percent"] else 0
            
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

def log_verification_result(actual: any, expected: any, res: bool, desc: str = "", name="Verification Details"):
    """Log verification results in a structured way."""
    result_text = ""
    result_text += f"Status: {'PASS' if res else 'FAIL'}\n"
    result_text += f"Actual: {actual}\n"
    result_text += f"Expected: {expected}\n"
    result_text += desc

    allure.attach(
        result_text,
        name=name,
        attachment_type=allure.attachment_type.TEXT
    )
