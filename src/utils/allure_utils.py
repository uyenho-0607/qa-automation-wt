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


def attach_verify_table(actual: dict, expected: dict, title="Table Details"):
    """
    Attach a dynamic HTML table to Allure report.
    """

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
        </style>
        <table>
        <thead>
            <tr>
                <th>Compare Field</th>
                <th>Actual</th>
                <th>Expected</th>
            </tr>
        </thead>
        <tbody>
        """

    # Get all unique keys from both dictionaries
    all_keys = sorted(set(actual.keys()) | set(expected.keys()))

    for key in all_keys:
        actual_val = actual.get(key, "")
        expected_val = expected.get(key, "")

        highlight = "highlight" if actual_val != expected_val else ""
        html += f"""
            <tr>
                <td>{' '.join(item.capitalize() for item in key.split('_'))}</td>
                <td class="{highlight}">{actual_val}</td>
                <td class="">{expected_val}</td>
            </tr>
            """

    html += "</table>"
    allure.attach(html, name=title, attachment_type=allure.attachment_type.HTML)
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
