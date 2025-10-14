import json
import os
import platform
import time
from datetime import datetime, timezone, timedelta

import allure
import pandas as pd

from src.data.consts import ROOTDIR, CSV_DIR, TOLERANCE_PERCENT
from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.assert_utils import soft_assert, compare_dict_with_keymap
from src.utils.logging_utils import logger

OUTPUT_DIR = ROOTDIR / ".chart_data"
METATRADER_TIMEZONE = timedelta(hours=3)
RECOVERED_TIME = None


def _get_recovered_time(timeframe: ChartTimeframe):
    """Get most recent scheduler time triggered, return time in timestamp millisecond"""
    # Singapore timezone (UTC+8)
    sg_tz = timezone(timedelta(hours=8))
    now = datetime.now(sg_tz)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Scheduler intervals
    sched_time = 1 if timeframe in [ChartTimeframe.one_min, ChartTimeframe.five_min] else 2

    # Hours since midnight
    elapsed_hours = (now - midnight).total_seconds() / 3600

    # Compute most recent hours
    most_recent_sched = int(elapsed_hours // sched_time) * sched_time

    # Convert to datetime in Singapore TZ
    last_triggered_sg = midnight + timedelta(hours=most_recent_sched)

    # Convert to UTC
    last_triggered_utc = last_triggered_sg.astimezone(timezone.utc)

    global RECOVERED_TIME
    RECOVERED_TIME = last_triggered_sg

    # Convert to milliseconds
    ts_triggered_ms = int(last_triggered_utc.timestamp() * 1000)
    return ts_triggered_ms


def _map_utc_timestamp(time_str: str):
    """Convert time as human date to timestamp and subtract 3 hours (map UTC)"""
    dt = datetime.strptime(time_str, "%Y.%m.%d %H:%M").replace(tzinfo=timezone.utc)
    dt_adjusted = dt - METATRADER_TIMEZONE  # Subtract 3 hours to map UTC time
    return int(dt_adjusted.timestamp() * 1000)


def _ms_to_metatrader_time(milliseconds, string_time=True):
    """Convert millisecond timestamp to UTC + 3 (meta trader timezone) with human-readable format option"""
    utc_plus_3 = timezone(METATRADER_TIMEZONE)
    dt = datetime.fromtimestamp(milliseconds / 1000, tz=utc_plus_3)
    if string_time:
        return dt.strftime("%Y-%m-%d %H:%M:%S (UTC+3)")

    # return timestamp value in UTC + 3
    return int((datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc) + METATRADER_TIMEZONE).timestamp())


def _csv_to_json(df, symbol: str, timeframe: ChartTimeframe):
    """Parse CSV exported data from metatrader to JSON file for precessing comparison"""
    os.makedirs(str(OUTPUT_DIR), exist_ok=True)
    df_reversed = df.iloc[::-1].reset_index(drop=True)

    # Convert to JSON format
    json_data = []
    for _, row in df_reversed.iterrows():
        json_entry = {
            "chartTime": int(row['Time_ms']),
            "close": float(row['Close']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "open": float(row['Open']),
        }
        json_data.append(json_entry)

    filepath = OUTPUT_DIR / f"{symbol}_{timeframe}_chart_data.json"

    with open(filepath, 'w') as f:
        json.dump(json_data, f, indent=4)

    return filepath


def load_metatrader_data(symbol: str, timeframe: ChartTimeframe):
    """Process MetaTrader CSV data and convert to JSON format"""
    timeframe = timeframe.get_timeframe().split("_")[-1]
    file = os.path.join(os.path.expanduser(CSV_DIR[RuntimeConfig.server]), f"{symbol}_{timeframe}.csv")

    # Check if file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"CSV file not found: {file}")

    if RuntimeConfig.server == "mt4":
        df = pd.read_csv(file, delimiter=';')  # mt4
    else:
        df = pd.read_csv(file, sep='\t')  # mt5

    # map timestamp back to UTC
    df['Time_ms'] = df['Time'].apply(_map_utc_timestamp)
    json_filepath = _csv_to_json(df, symbol, timeframe)

    # load out json file
    with open(json_filepath, 'r') as f:
        parsed_data = json.load(f)

    return parsed_data


def timeframe_to_ms(timeframe: ChartTimeframe):
    """Match timeframe with its expected interval time in milliseconds"""
    timeframe_intervals = {
        ChartTimeframe.one_min: 1,  # 1 minute = 60000 milliseconds
        ChartTimeframe.five_min: 5,  # 5 minutes = 300000 milliseconds
        ChartTimeframe.fifteen_min: 15,  # 15 minutes = 900000 milliseconds
        ChartTimeframe.thirty_min: 30,  # 30 minutes = 1800000 milliseconds
        ChartTimeframe.one_hour: 60,  # 1 hour = 3600000 milliseconds
        ChartTimeframe.four_hour: 4 * 60,  # 4 hours = 14400000 milliseconds
        ChartTimeframe.one_day: 24 * 60,  # 1 day = 86400000 milliseconds
        ChartTimeframe.one_week: 7 * 24 * 60,  # 1 week = 604800000 milliseconds
        ChartTimeframe.one_month: 30 * 24 * 60,  # 1 month = 2592000000 milliseconds (approximate)
    }

    return timeframe_intervals.get(timeframe) * 60 * 1000


def _format_exp_interval(interval_min, timeframe):
    """Format interval in milliseconds to human-readable format based on timeframe"""
    interval_min = interval_min / (60 * 1000)

    if timeframe in [ChartTimeframe.one_min, ChartTimeframe.five_min, ChartTimeframe.fifteen_min, ChartTimeframe.thirty_min]:
        unit = "min(s)"
        res = interval_min

    if timeframe in [ChartTimeframe.one_hour, ChartTimeframe.four_hour]:
        unit = "hour(s)"
        res = interval_min / 60

    if timeframe == ChartTimeframe.one_day:
        unit = "day(s)"
        res = interval_min / (24 * 60)

    if timeframe == ChartTimeframe.one_week:
        res = interval_min / (24 * 60)
        if round(res) == 7:
            unit = "week"

        else:
            unit = "days"

    if timeframe == ChartTimeframe.one_month:
        res = interval_min / (24 * 60)
        if round(res) == 30:
            unit = "month"
        else:
            unit = "days"

    return f"{round(res)} {unit}"


def _check_timestamp_interval(api_data, chart_data, timeframe: ChartTimeframe) -> dict:
    """
    Check if each dataset distance from previous is equal to the expected interval
    NOTE: if wrong dataset is present on both chart_data and api_data, it's acceptable
    """
    expected_interval = timeframe_to_ms(timeframe)
    failed = []

    # Ensure input is sorted
    api_data = sorted(api_data, key=lambda x: x['chartTime'])
    chart_data = sorted(chart_data, key=lambda x: x['chartTime'])

    actual = [item['chartTime'] for item in api_data]
    expected = [item['chartTime'] for item in chart_data]

    min_len = min(len(api_data), len(chart_data))

    for i in range(min_len - 1):
        a_delta = actual[i + 1] - actual[i]

        if a_delta != expected_interval:
            try:
                if expected.index(actual[i + 1]) - expected.index(actual[i]) == 1:
                    continue
            except ValueError:
                pass

            actual_ms_items = f"{actual[i]} <-> {actual[i + 1]}"
            actual_date_items = f"{_ms_to_metatrader_time(actual[i])} <-> {_ms_to_metatrader_time(actual[i + 1])}"
            failed.append(dict(ms=actual_ms_items, date=actual_date_items, interval=actual[i + 1] - actual[i]))

    return {"result": len(failed) == 0, "failed": failed}


def compare_chart_data(chart_data, api_data, timeframe, symbol=None):
    """Compare chart data (MetaTrader) with API data based on chartTime"""
    # skip checking for the last chart stick
    if api_data[-1]['chartTime'] == chart_data[-1]['chartTime']:
        # map value of chart data to API data for skipping check
        for key, value in chart_data[-1].items():
            if key != 'chartTime':
                api_data[-1][key] = value

    compare_res = {"scanned": {}, "not_scanned": {}}
    final_res = []

    # filter not compare keys
    api_data = [{k: v for k, v in item.items() if k not in ["ask", "source"]} for item in api_data]

    ############### DATASET AMOUNT ###############
    logger.info(f"{'-' * 10} COMPARE DATASET AMOUNT {'-' * 10}")
    final_res.append(soft_assert(len(api_data), len(chart_data), error_message=f"Dataset amount mismatch: actual={len(api_data)} <> expected={len(chart_data)}"))
    compare_res['dataset_amount'] = {'actual': len(api_data), 'expected': len(chart_data)}

    ############### MISMATCH/ MISSING ###############
    logger.info(f"{'-' * 10} COMPARE CHART DATA {'-' * 10}")

    # divide into scanned and not scanned range for compare
    most_recover_time = _get_recovered_time(timeframe)
    _split_data = lambda data, t: ([d for d in data if d['chartTime'] < t - timeframe_to_ms(timeframe)], [d for d in data if d['chartTime'] >= t - timeframe_to_ms(timeframe)])

    act_recovered, act_unrecovered = _split_data(api_data, most_recover_time)
    exp_recovered, exp_unrecovered = _split_data(chart_data, most_recover_time)

    # data failed in this range should be bugged
    res_recovered = compare_dict_with_keymap(act_recovered, exp_recovered, "chartTime", tolerance_percent=TOLERANCE_PERCENT)

    # recheck if missing the latest item due to APIs BE logic
    if res_recovered["missing"]:
        # filter the missing item
        res_recovered["missing"] = [item for item in res_recovered["missing"] if item >= min(item['chartTime'] for item in chart_data)]
        if not res_recovered and not res_recovered["mismatches"]:
            res_recovered["res"] = True

    # data failed in this range can be fixed by recover job
    res_unrecovered = compare_dict_with_keymap(act_unrecovered, exp_unrecovered, "chartTime", tolerance_percent=TOLERANCE_PERCENT)

    # append only recovered chart data comparison result
    final_res.extend([res_recovered['res']])

    # handle log for recovered result -> bug
    if not res_recovered['res']:
        logger.error(f"❌ Chart data comparison failed - Recovered data")
        error_msg = f"Chart data comparison failed"

        if res_recovered['mismatches']:
            compare_res["scanned"]['mismatches'] = res_recovered['mismatches']

            logger.error(f"❌ Mismatched - Recovered data: {len(res_recovered['mismatches'])} items")
            error_msg += "\n➡️ Mismatched Recovered data"

        if res_recovered['missing']:
            compare_res["scanned"]['missing'] = res_recovered['missing']

            logger.error(f"❌ Missing - Recovered data: {len(res_recovered['missing'])} items")
            error_msg += "\n➡️ Missing Recovered data"

        # failed the checkpoint
        soft_assert(True, False, error_message=error_msg)

    # handle log for scanned result -> only warning
    if not res_unrecovered['res']:
        logger.warning(f"⚠️ Chart data comparison failed - NOT recovered data")

        if res_unrecovered['mismatches']:
            compare_res["not_scanned"]['mismatches'] = res_unrecovered['mismatches']
            logger.warning(f"⚠️ Mismatched - NOT recovered data: {len(res_unrecovered['mismatches'])} items")

        if res_unrecovered['missing']:
            compare_res["not_scanned"]['missing'] = res_unrecovered['missing']
            logger.warning(f"⚠️ Missing - NOT recovered data: {len(res_unrecovered['missing'])} items")

    ############### TIMEFRAME INTERVAL ###############
    logger.info(f"{'-' * 10} COMPARE TIMEFRAME INTERVAL {'-' * 10}")
    res_int = _check_timestamp_interval(api_data, chart_data, timeframe)

    # append timeframe interval result
    final_res.append(res_int["result"])

    if not res_int["result"]:
        compare_res['interval'] = res_int['failed']
        compare_res['timeframe'] = timeframe

        logger.error(f"❌ Invalid interval time: {len(res_int['failed'])}")
        error_msg = f"Timeframe interval validation failed"

        # failed the checkpoint
        soft_assert(True, False, error_message=error_msg)

    if all(final_res):
        logger.info(f"{'-' * 10} PASSED ✅ {'-' * 10}")

    attach_compare_files(compare_res, symbol, timeframe)


def attach_compare_files(comparison_result, symbol, timeframe):
    """Attach a summary table of chart data comparison results to Allure report."""
    ############### COMPARISON TABLE ####################
    timeframe_display = timeframe.replace("_", " ").upper()
    title = f"📊 Chart Data Comparison Summary - {symbol} - {timeframe_display}"

    html = f"""
        <style>
            .summary-table {{
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
                margin: 15px 0;
                background-color: #f9f9f9;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .summary-table th {{
                background-color: #4CAF50;
                color: white;
                padding: 12px 15px;
                text-align: left;
                font-weight: bold;
                font-size: 14px;
            }}
            .summary-table td {{
                padding: 10px 15px;
                border-bottom: 1px solid #ddd;
                font-size: 13px;
                vertical-align: top;
            }}
            .summary-table tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .summary-table tr:hover {{
                background-color: #e8f5e8;
            }}
            .status-pass {{
                color: #4CAF50;
                font-weight: bold;
            }}
            .status-fail {{
                color: #f44336;
                font-weight: bold;
            }}
            .status-warning {{
                color: #ff9800;
                font-weight: bold;
            }}
            .header-info {{
                background-color: #2196F3;
                color: white;
                padding: 10px 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }}
            .error-details {{
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px;
                margin: 5px 0;
                font-size: 11px;
                max-height: 200px;
                overflow-y: auto;
            }}
            .error-item {{
                background-color: #f8f9fa;
                border-left: 3px solid #dc3545;
                padding: 6px;
                margin: 3px 0;
                border-radius: 3px;
                font-size: 12px;
            }}
            .warning-item {{
                background-color: #f8f9fa;
                border-left: 3px solid #ffc107;
                padding: 6px;
                margin: 3px 0;
                border-radius: 3px;
                font-size: 12px;
            }}
        </style>
        <div class="header-info">
            {title}
        </div>
        <table class="summary-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Count</th>
                <th>Status</th>
                <th>Details</th>
            </tr>
        </thead>
        <tbody>
    """

    # --------- dataset amount  --------- #
    data_amount = comparison_result.get("dataset_amount")
    data_diff = data_amount['actual'] == data_amount['expected']

    html += f"""
        <tr>
            <td>📊 Dataset Amount</td>
            <td>{data_amount['actual'] - data_amount['expected']}</td>
            <td class="{"status-fail" if not data_diff else "status-pass"}">{"FAIL" if not data_diff else "PASS"}</td>
            <td>{f"API: {data_amount['actual']} | MetaTrader: {data_amount['expected']}"}</td>
        </tr>
    """

    # Compare result metrics
    missing_recovered = comparison_result["scanned"].get("missing", [])
    diff_recovered = comparison_result["scanned"].get("mismatches", [])
    missing_unrecovered = comparison_result["not_scanned"].get("missing", [])
    diff_unrecovered = comparison_result["not_scanned"].get("mismatches", [])
    interval = comparison_result.get("interval", [])

    # --------- RECOVERED DATA --------- #
    #### missing data
    missing_count = len(missing_recovered)
    missing_details = "RECOVERED data points present in MetaTrader but missing in API"

    if missing_count:
        missing_details += f"<br><div class='error-details'>"
        for i, item in enumerate(missing_recovered):
            missing_details += f"""
                <div class="error-item">
                    <strong>Missing #{i + 1}:</strong> {item}, chart_time: {_ms_to_metatrader_time(item)}<br>
                </div>
            """
        missing_details += "</div>"

    html += f"""
        <tr>
            <td>❌ Missing RECOVERED Data Points</td>
            <td>{missing_count}</td>
            <td class="{"status-fail" if missing_count else "status-pass"}">{"FAIL" if missing_count else "PASS"}</td>
            <td>{missing_details}</td>
        </tr>
    """

    ##### different data
    diff_count = len(diff_recovered)
    different_details = "RECOVERED data points with different values between MetaTrader and API"

    if diff_count:
        different_details += f"<br><div class='error-details'>"
        for i, item in enumerate(diff_recovered):
            chart_time = item.get("chartTime", "")
            original_chart_str = _ms_to_metatrader_time(chart_time) if chart_time else "Unknown"

            different_details += f"""
                <div class="error-item">
                    <strong>Different #{i + 1}:</strong> API data: {chart_time}, chart_time: {original_chart_str}<br>
            """
            different_details += f"expected={item.get('expected')}, actual={item.get('actual')}<br>"
            different_details += """
                </div>
            """
        different_details += "</div>"

    html += f"""
        <tr>
            <td>🔄 Different RECOVERED Data Points</td>
            <td>{diff_count}</td>
            <td class="{"status-fail" if diff_count else "status-pass"}">{"FAIL" if diff_count else "PASS"}</td>
            <td>{different_details}</td>
        </tr>
    """

    # --------- NOT RECOVERED DATA --------- #
    ##### missing
    missing_count = len(missing_unrecovered)
    missing_details = "NOT RECOVERED data points present in MetaTrader but missing in API"

    if missing_count:
        missing_details += f"<br><div class='error-details'>"
        for i, item in enumerate(missing_unrecovered):
            missing_details += f"""
                    <div class="error-item">
                        <strong>Missing #{i + 1}:</strong> {item}, chart_time: {_ms_to_metatrader_time(item)}<br>
                    </div>
                """
        missing_details += "</div>"

    html += f"""
            <tr>
                <td>⚠️ Missing NOT RECOVERED Data Points</td>
                <td>{missing_count}</td>
                <td class="{"status-warning" if missing_count else "status-pass"}">{"WARNING" if missing_count else "PASS"}</td>
                <td>{missing_details}</td>
            </tr>
        """

    ##### different
    diff_count = len(diff_unrecovered)
    different_details = "NOT RECOVERED data points with different values between MetaTrader and API"

    if diff_count:
        different_details += f"<br><div class='error-details'>"
        for i, item in enumerate(diff_unrecovered):
            chart_time = item.get("chartTime", "")
            original_chart_str = _ms_to_metatrader_time(chart_time) if chart_time else "Unknown"

            different_details += f"""
                    <div class="error-item">
                        <strong>Different #{i + 1}:</strong> API data: {chart_time}, chart_time: {original_chart_str}<br>
                """
            different_details += f"expected={item.get('expected')}, actual={item.get('actual')}<br>"
            different_details += """
                    </div>
                """
        different_details += "</div>"

    html += f"""
            <tr>
                <td>⚠️ Different NOT RECOVERED Data Points</td>
                <td>{diff_count}</td>
                <td class="{"status-warning" if diff_count else "status-pass"}">{"WARNING" if diff_count else "PASS"}</td>
                <td>{different_details}</td>
            </tr>
        """

    # Add invalid interval data row
    int_count = len(interval)
    int_details = "Data points with invalid interval (API response ONLY)"

    if int_count:
        int_details += f"<br><div class='error-details'>"
        for i, item in enumerate(interval):
            int_details += f"""
                    <div class="error-item">
                        <strong>Invalid #{i + 1}:</strong>
                """
            int_details += f"ms={item.get('ms')}, chart_time={item.get('date')}, interval={_format_exp_interval(item.get('interval', 0), comparison_result.get('timeframe'))}<br>"
            int_details += """
                    </div>
                """
        int_details += "</div>"

    html += f"""
            <tr>
                <td>🔄 Invalid Interval Data Points</td>
                <td>{int_count}</td>
                <td class="{"status-fail" if int_count else "status-pass"}">{"FAIL" if int_count else "PASS"}</td>
                <td>{int_details}</td>
            </tr>
        """

    html += """
        </tbody>
        </table>
    """

    # Attach compare table to Allure report
    allure.attach(
        html,
        name=f"Chart Comparison Summary - {symbol} - {timeframe_display}",
        attachment_type=allure.attachment_type.HTML
    )

    ############### META TRADER CSV FILE ####################
    file_path = os.path.join(os.path.expanduser(CSV_DIR[RuntimeConfig.server]), f"{symbol}_{timeframe.get_timeframe().split("_")[-1]}.csv")

    # convert to html format for human-readable
    df = pd.read_csv(file_path, sep=None, engine="python")

    # Reset index to start from 1
    df.index = df.index + 1

    html_table = df.to_html(
        index=True,
        border=2,
        justify="center",
        classes="styled-table",
        escape=False
    )
    # Clean modern CSS (one color)
    css = """
    <style>
    body {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 14px;
        color: #333;
        margin: 10px;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        background-color: #fafafa;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 6px 10px;
        text-align: center;
        white-space: nowrap;
    }
    
    /* Table header */
    thead th {
        background-color: #4287f5;
        color: white;
    }
    
    /* Row hover background */
    tr:hover {
        background-color: #f2f2f2;
    }
    
    /* Row highlight colors */
    .highlight-diff { background-color: #ff8c00 !important; } 
    .highlight-missing { background-color: #ff6666 !important; }
    .highlight-warning { background-color: #fff3cd !important; }
    .highlight-white { background-color: #ffffff !important; }
    .highlight-recover { background-color: #90ee90 !important; }
    
    /* Subtle grey for Timestamp column */
    td:nth-child(3) {
        color: #888;
        font-style: italic;
    }  
    
    /* Row-level tooltip */
    td.row-tooltip-container {
        position: relative;
        cursor: pointer;
    }
    
    td.row-tooltip-container span.row-tooltip {
        visibility: hidden;
        background-color: #333;
        color: #fff;
        padding: 8px 12px;   
        font-size: 14px; 
        font-weight: bold; 
        border-radius: 4px;
        position: absolute;
        top: 0;
        left: 300px;
        width: max-content;
        max-width: 300px;
        min-width: 120px;
        white-space: pre-wrap;
        text-align: center;
        opacity: 0;
        transition: opacity 0.1s ease-in-out;
        z-index: 9999;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
    }
    
    /* Show tooltip when hovering the row */
    tr:hover td.row-tooltip-container span.row-tooltip {
        visibility: visible;
        opacity: 1;
    }
    /* Scrollable table with sticky header */
    .table-wrapper {
        position: relative;
        max-height: 600px; /* adjust as needed */
        overflow-y: auto;
        border: 1px solid #ddd;
    }
    
    /* Make table headers sticky */
    table thead th {
        position: sticky;
        top: 0;
        background-color: #4287f5; /* same as before */
        color: white;
        z-index: 2; /* stay on top of rows */
    }
    </style>

    """

    # Highlight issue data: RED - failed recovered, YELLOW - failed unrecovered
    _diff_recovered = diff_recovered[:]
    _diff_unrecovered = diff_unrecovered[:]

    # Convert chartTime to MT time (ms) for highlighting
    for item in _diff_recovered + _diff_unrecovered:
        item["chartTime"] = _ms_to_metatrader_time(item["chartTime"], string_time=False)

    missing_recovered_times = [_ms_to_metatrader_time(item, string_time=False) for item in missing_recovered]
    missing_unrecovered_times = [_ms_to_metatrader_time(item, string_time=False) for item in missing_unrecovered]

    diff_recovered_times = [item['chartTime'] for item in _diff_recovered]
    unrecovered_times = [item['chartTime'] for item in _diff_unrecovered] + missing_unrecovered_times

    recovered_time = _ms_to_metatrader_time(_get_recovered_time(timeframe), string_time=False)
    highlight_times = diff_recovered_times + missing_recovered_times + unrecovered_times + [recovered_time]

    if highlight_times:
        lines = html_table.splitlines()
        new_lines = []
        current_row = []
        highlight_next = False
        tool_tip = ""

        for line in lines:
            # Start of a new row
            if "<tr>" in line:
                current_row = [line]
                highlight_next = False
                color = "white"
                tool_tip = ""
                continue

            # Collect row content
            if current_row:
                line_to_add = line

                # Detect if this row should be highlighted
                for t in highlight_times:
                    if f">{t}<" in line:
                        highlight_next = True

                        if t == recovered_time:
                            color = "recover"
                            tool_tip = "Recovered Time\n"

                            matched = [item for item in _diff_unrecovered if item['chartTime'] == t]
                            if matched:
                                failed_item = matched[0]
                                tool_tip += f'{str(failed_item['actual']).replace(",", "\n").replace("{", "").replace("}", "").replace("'", "")}'

                        # Determine color and tooltip
                        elif t in diff_recovered_times:
                            color = "diff"
                            matched = [item for item in _diff_recovered if item['chartTime'] == t]
                            if matched:
                                failed_item = matched[0]
                                tool_tip = f'{str(failed_item['actual']).replace(",", "\n").replace("{", "").replace("}", "").replace("'", "")}'
                            else:
                                tool_tip = "Issue data"

                        elif t in missing_recovered_times:
                            color = "missing"
                            tool_tip = "Missing datapoint"

                        else:  # warning / unrecovered
                            color = "warning"
                            matched = [item for item in _diff_unrecovered if item['chartTime'] == t]
                            if matched:
                                failed_item = matched[0]
                                tool_tip = f'{str(failed_item['actual']).replace(",", "\n").replace("{", "").replace("}", "").replace("'", "")}'
                            else:
                                tool_tip = "Missing datapoint"

                        break  # only first match per row

                current_row.append(line_to_add)

            # End of row
            if "</tr>" in line and current_row:
                current_row.append(line)
                row_html = "\n".join(current_row)

                if highlight_next:
                    # Add highlight class
                    row_html = row_html.replace("<tr>", f"<tr class='highlight-{color}'>", 1)

                    # Inject tooltip in first <td> only
                    if tool_tip:
                        row_html = row_html.replace(
                            "<td>",
                            f"<td class='row-tooltip-container'><span class='row-tooltip'>{tool_tip}</span>",
                            1
                        )

                new_lines.append(row_html)

                # Reset for next row
                current_row = []
                highlight_next = False
                color = "white"
                tool_tip = ""

            elif not current_row:
                # Lines outside table rows
                new_lines.append(line)

        html_table = "\n".join(new_lines)

    # Final wrapped HTML
    final_html = f"""
        <html>
        <head>{css}</head>
        <body>
            <h4>{symbol} — {timeframe_display}</h4>
            {html_table}
        </body>
        </html>
        """

    allure.attach(
        final_html,
        name=f"Metatrader CSV Data - {symbol} - {timeframe_display}",
        attachment_type=allure.attachment_type.HTML
    )

    # Build color-coded description summary
    summary_lines = [
        "<div style='background-color:#e8f0ff; color:#000000; padding:10px; border-radius:6px;'>"
        "📝 <strong>Note:</strong>"
        "<ul style='margin:6px 0 0 20px;'>"
        "<li>This test checks the latest 500 chart data points.</li>"
        "<li>The most recent candle is skipped because it is still forming and may not be stable.</li>"
        "</ul>"
        "</div>"
    ]

    if diff_recovered:
        summary_lines.append(f"<p style='color:#ff4d4d;'>❌ Total Mismatch records: <strong>{len(diff_recovered)}</strong></p>")

    if missing_recovered:
        summary_lines.append(f"<p style='color:#ff4d4d;'>❌ Total Missing records: <strong>{len(missing_recovered)}</strong></p>")

    if diff_unrecovered or missing_unrecovered:
        summary_lines.append(f"<p style='color:#ff9900;'>⚠️ Total NOT RECOVERED records (acceptable): <strong>{len(diff_unrecovered) + len(missing_unrecovered)}</strong></p>")

    # If everything passed
    if not summary_lines:
        summary_lines.append("<p style='color:#2E8B57;'><strong>✅ All data passed validation — no mismatches or missing records 🥳</strong></p>")

    # Add most recent recovery time
    summary_lines.append(
        f"<p>⏳ Recovery Time&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:&nbsp <strong style='color:#2E8B57;'>{RECOVERED_TIME.astimezone(timezone(timedelta(hours=3))).strftime("%Y-%m-%d - %H:%M:%S")} (UTC+3) - {RECOVERED_TIME.strftime("%Y-%m-%d - %H:%M:%S")} (SG Time) </strong></p>"
    )

    summary_lines.append(
        f"<p>🧪 Test Executed Time: &nbsp<strong>{datetime.now(timezone(timedelta(hours=3))).strftime('%Y-%m-%d - %H:%M:%S')} (UTC+3) - {datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d - %H:%M:%S')} (SG Time) </strong></p>"
    )

    # Attach to Allure
    allure.dynamic.description_html("\n".join(summary_lines))
