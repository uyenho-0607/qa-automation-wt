import json
import os
from datetime import datetime, timezone, timedelta

import allure
import pandas as pd

from src.data.consts import DATA_DIR
from src.data.enums import Server, ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.assert_utils import soft_assert, compare_dict_with_keymap
from src.utils.logging_utils import logger

CSV_DIR = {
    Server.MT5: r"~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files/",
    Server.MT4: r"~/Library/Application Support/net.metaquotes.wine.metatrader4/drive_c/Program Files (x86)/MetaTrader 4/MQL4/Files/"
}

OUTPUT_DIR = DATA_DIR / ".chart_data"


def _map_timestamp(time_str: str):
    """Convert time as human date to timestamp and subtract 3 hours (map UTC)"""
    dt = datetime.strptime(time_str, "%Y.%m.%d %H:%M").replace(tzinfo=timezone.utc)
    dt_adjusted = dt - timedelta(hours=3)  # Subtract 3 hours to map UTC time
    return int(dt_adjusted.timestamp() * 1000)


def _ms_to_date(milliseconds):
    """Convert milliseconds timestamp to human-readable date"""
    dt = datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def _csv_to_json(df, symbol: str, timeframe: ChartTimeframe):
    """Save DataFrame to JSON format as specified"""
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


def _process_metatrader_data(symbol: str, timeframe: ChartTimeframe):
    """Process MetaTrader CSV data and convert to JSON format"""
    timeframe = timeframe.get_timeframe().split("_")[-1]
    file = os.path.join(os.path.expanduser(CSV_DIR[RuntimeConfig.server]), f"{symbol}_{timeframe}.csv")

    # Check if file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f"CSV file not found: {file}")

    if RuntimeConfig.server == "mt4":
        df = pd.read_csv(file, delimiter=';')   # mt4
    else:
        df = pd.read_csv(file, sep='\t')  # mt5

    df['Time_ms'] = df['Time'].apply(_map_timestamp)
    json_filepath = _csv_to_json(df, symbol, timeframe)

    return json_filepath


def parse_metatrader_data(symbol: str, timeframe: ChartTimeframe):
    """Parse metatrader data from json file"""
    parsed_filepath = _process_metatrader_data(symbol, timeframe)
    with open(parsed_filepath, 'r') as f:
        parsed_data = json.load(f)

    return parsed_data


def timeframe_to_ms(timeframe: ChartTimeframe):
    # Convert timeframe to expected interval in milliseconds
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


def _exp_interval(interval_min, timeframe):
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


def check_timestamp_interval(api_data, chart_data, timeframe: ChartTimeframe):
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
        e_delta = expected[i + 1] - expected[i]

        # If expected and actual both wrong, it's acceptable
        if a_delta != expected_interval and e_delta != expected_interval:
            continue

        # If actual wrong and expected is correct → failure
        if a_delta != expected_interval and e_delta == expected_interval:
            actual_ms_items = f"{actual[i]} <-> {actual[i + 1]}"
            actual_date_items = f"{_ms_to_date(actual[i])} <-> {_ms_to_date(actual[i + 1])}"
            failed.append(dict(ms=actual_ms_items, date=actual_date_items, interval=actual[i + 1] - actual[i]))

    return {"result": len(failed) == 0, "failed": failed}


def compare_chart_data(chart_data, api_data, timeframe=None):
    """Compare chart data (MetaTrader) with API data based on chartTime"""

    final_res = []
    compare_res = {}

    # clean data
    api_data = [{k: v for k, v in item.items() if k not in ["ask", "source"]} for item in api_data]

    # overall dataset amount
    res_amount = soft_assert(len(api_data), len(chart_data), error_message=f"Dataset amount mismatch: actual={len(api_data)} <> expected={len(chart_data)}")
    compare_res["dataset_amount"] = {'actual': len(api_data), 'expected': len(chart_data)}

    if not res_amount:
        final_res.append(False)
        compare_res['dataset_amount'] = {'actual': len(api_data), 'expected': len(chart_data)}

    # chart data comparison
    res = compare_dict_with_keymap(api_data, chart_data, 'chartTime', tolerance=0.0003)

    if not res['result']:
        final_res.append(False)
        logger.error(f"❌ Chart data comparison failed")
        error_msg = f"Chart data comparison failed"

        if res['mismatches']:
            compare_res['mismatches'] = res['mismatches']

            logger.error(f"❌ Mismatched: {len(res['mismatches'])} items")
            for item in res['mismatches']:
                error_msg += f"\n - Mismatched item {item['chartTime']} ({_ms_to_date(item['chartTime'])}): {item['actual']} <-> {item['expected']}"

        if res['missing']:
            compare_res['missing'] = res['missing']

            logger.error(f"❌ Missing: {len(res['missing'])} items")
            for item in res['missing']:
                error_msg += f"\n - Missing item: {item} ({_ms_to_date(item)})"

        if res['redundant']:
            compare_res['redundant'] = res['redundant']
            logger.error(f"❌ Redundant: {len(res['redundant'])} items")
            for item in res['redundant']:
                error_msg += f"\n - Redundant item: {item} ({_ms_to_date(item)})"

        soft_assert(True, False, error_message=error_msg)

    if timeframe:
        res_int = check_timestamp_interval(api_data, chart_data, timeframe)

        if not res_int["result"]:
            compare_res['interval'] = res_int['failed']
            compare_res['timeframe'] = timeframe

            final_res.append(False)
            logger.error(f"❌ Invalid interval time: {len(res_int['failed'])}")
            error_msg = f"Timeframe interval validation failed - Expected {timeframe.name} - Got: "

            for item in res_int['failed']:
                act_interval = _exp_interval(item['interval'], timeframe)
                error_msg += f"\n - {act_interval} - {item['ms']} ({item['date']})"

            soft_assert(True, False, error_message=error_msg)

    if all(final_res):
        logger.info(f"✅ Chart data comparison passed")

    else:
        attach_chart_comparison_summary(compare_res)


def attach_chart_comparison_summary(comparison_result):
    """Attach a summary table of chart data comparison results to Allure report."""
    html = """
        <style>
            .summary-table {
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
                margin: 15px 0;
                background-color: #f9f9f9;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .summary-table th {
                background-color: #4CAF50;
                color: white;
                padding: 12px 15px;
                text-align: left;
                font-weight: bold;
                font-size: 14px;
            }
            .summary-table td {
                padding: 10px 15px;
                border-bottom: 1px solid #ddd;
                font-size: 13px;
                vertical-align: top;
            }
            .summary-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .summary-table tr:hover {
                background-color: #e8f5e8;
            }
            .status-pass {
                color: #4CAF50;
                font-weight: bold;
            }
            .status-fail {
                color: #f44336;
                font-weight: bold;
            }
            .status-warning {
                color: #ff9800;
                font-weight: bold;
            }
            .header-info {
                background-color: #2196F3;
                color: white;
                padding: 10px 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                font-weight: bold;
                text-align: center;
            }
            .error-details {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 8px;
                margin: 5px 0;
                font-size: 11px;
                max-height: 200px;
                overflow-y: auto;
            }
            .error-item {
                background-color: #f8f9fa;
                border-left: 3px solid #dc3545;
                padding: 6px;
                margin: 3px 0;
                border-radius: 3px;
                font-size: 10px;
            }
            .warning-item {
                background-color: #f8f9fa;
                border-left: 3px solid #ffc107;
                padding: 6px;
                margin: 3px 0;
                border-radius: 3px;
                font-size: 10px;
            }
        </style>
        <div class="header-info">
            📊 Chart Data Comparison Summary
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

    # Add dataset amount row
    data_amount = comparison_result.get("dataset_amount")
    data_diff = data_amount['actual'] == data_amount['expected']
    dataset_status = "status-fail" if not data_diff else "status-pass"
    dataset_text = "FAIL" if not data_diff else "PASS"
    dataset_details = f"API: {data_amount['actual']} | MetaTrader: {data_amount['expected']}"

    html += f"""
        <tr>
            <td>📊 Dataset Amount</td>
            <td>{data_amount['actual'] - data_amount['expected']}</td>
            <td class="{dataset_status}">{dataset_text}</td>
            <td>{dataset_details}</td>
        </tr>
    """

    # Add missing data row
    missing_count = len(comparison_result.get("missing", []))
    missing_status = "status-fail" if missing_count else "status-pass"
    missing_text = "FAIL" if missing_count else "PASS"
    missing_details = "Data points present in MetaTrader but missing in API"

    if missing_count:
        missing_details += f"<br><div class='error-details'>"
        for i, item in enumerate(comparison_result.get("missing", [])):
            date_str = _ms_to_date(item)
            missing_details += f"""
                <div class="error-item">
                    <strong>Missing #{i + 1}:</strong> {date_str}<br>
                </div>
            """
        missing_details += "</div>"

    html += f"""
        <tr>
            <td>❌ Missing Data Points</td>
            <td>{missing_count}</td>
            <td class="{missing_status}">{missing_text}</td>
            <td>{missing_details}</td>
        </tr>
    """

    # Add redundant data row
    redundant_count = len(comparison_result.get("redundant", []))
    redundant_status = "status-warning" if redundant_count else "status-pass"
    redundant_text = "WARNING" if redundant_count else "PASS"
    redundant_details = "Data points present in API but not in MetaTrader"

    if redundant_count:
        redundant_details += f"<br><div class='error-details'>"
        for i, item in enumerate(comparison_result.get("redundant", [])):
            date_str = _ms_to_date(item)
            redundant_details += f"""
                <div class="warning-item">
                    <strong>Redundant #{i + 1}:</strong> {date_str}<br>
                </div>
            """
        redundant_details += "</div>"

    html += f"""
        <tr>
            <td>⚠️ Redundant Data Points</td>
            <td>{redundant_count}</td>
            <td class="{redundant_status}">{redundant_text}</td>
            <td>{redundant_details}</td>
        </tr>
    """

    # Add different data row
    different_count = len(comparison_result.get("mismatches", []))
    different_status = "status-fail" if different_count else "status-pass"
    different_text = "FAIL" if different_count else "PASS"
    different_details = "Data points with different values between MetaTrader and API"

    if different_count:
        different_details += f"<br><div class='error-details'>"
        for i, item in enumerate(comparison_result.get("mismatches", [])):
            chart_time = item.get("chartTime", "")
            date_str = _ms_to_date(chart_time) if chart_time else "Unknown"

            different_details += f"""
                <div class="error-item">
                    <strong>Different #{i + 1}:</strong> {date_str}<br>
            """
            different_details += f"expected={item.get('expected')}, actual={item.get('actual')}<br>"
            different_details += """
                </div>
            """
        different_details += "</div>"

    html += f"""
        <tr>
            <td>🔄 Different Data Points</td>
            <td>{different_count}</td>
            <td class="{different_status}">{different_text}</td>
            <td>{different_details}</td>
        </tr>
    """

    # Add invalid interval data row
    int_count = len(comparison_result.get("interval", []))
    int_status = "status-fail" if int_count else "status-pass"
    int_text = "FAIL" if int_count else "PASS"
    int_details = "Data points with invalid interval (API response ONLY)"

    if int_count:
        int_details += f"<br><div class='error-details'>"
        for i, item in enumerate(comparison_result.get("interval", [])):
            int_details += f"""
                    <div class="error-item">
                        <strong>Invalid #{i + 1}:</strong>
                """
            int_details += f"ms={item.get('ms')}, date={item.get('date')}, interval={_exp_interval(item.get('interval', 0), comparison_result.get('timeframe'))}<br>"
            int_details += """
                    </div>
                """
        int_details += "</div>"

    html += f"""
            <tr>
                <td>🔄 Invalid Interval Data Points</td>
                <td>{int_count}</td>
                <td class="{int_status}">{int_text}</td>
                <td>{int_details}</td>
            </tr>
        """

    html += """
        </tbody>
        </table>
    """

    # Attach to Allure report
    allure.attach(
        html,
        name=f"Chart Comparison Summary",
        attachment_type=allure.attachment_type.HTML
    )
