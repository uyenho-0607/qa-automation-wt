import json
import os
import re
from pathlib import Path
from typing import Dict, Any

import allure

from src.data.consts import ROOTDIR
from src.data.project_info import StepLogs
from src.utils.logging_utils import logger


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

            _add_attachments_prop(data)  # add empty attachments prop for each test report
            _remove_zero_duration(data)

            if data.get("status", "") == "failed":
                _process_failed_status(data)  # Process failed status if any

            elif data.get("status", "") == "broken":
                _process_broken_status(data)  # Process broken status if any

            _cleanup_and_customize_report(data)  # Clean up and customize report
            _clean_log_files(allure_dir)

            # Write back the modified data
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            logger.error(f"Error processing file {os.path.basename(file_path)}: {str(type(e).__name__)}, {str(e)}")
            continue


def _add_attachments_prop(data: Dict[str, Any]) -> None:
    for item in data.get("steps", []):
        item["attachments"] = []


def _process_failed_status(data: Dict[str, Any]) -> None:
    """Process failed test status and update steps."""
    if not data.get("steps"):
        return

    test_id = [item["value"] for item in data["labels"] if item["name"] == "as_id"][0]
    filtered_logs = [StepLogs.failed_logs_dict[key] for key in StepLogs.failed_logs_dict if key == test_id]

    if not filtered_logs:
        return

    steps_map = {s["name"].lower(): s for s in data["steps"]}
    failed_logs = filtered_logs[0]

    for failed_step, _ in failed_logs:
        v_step = steps_map.get(failed_step.lower())

        if v_step:
            if "verify" in v_step["name"].lower():
                v_step["status"] = "failed"

            else:  # this is a broken step
                v_step["status"] = "broken"


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
    data.get("statusDetails", {}).pop("trace", None)
    data["name"] = data["fullName"].split(".")[-1].replace("#test", "")
    data["name"] = " ".join(data["name"].split("_"))


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


def _remove_zero_duration(data: Dict[str, Any]):
    for item in data.get("steps", []):
        start = item.get("start", 0)
        stop = item.get("stop", 0)
        if stop == start:
            item["stop"] += 1
