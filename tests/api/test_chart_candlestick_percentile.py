from datetime import datetime, timedelta, UTC
from typing import List

import allure
import numpy as np
import pytest
import requests

from src.apis.api_client import APIClient
from src.data.enums import ChartTimeframe
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger

NUM_REQS = RuntimeConfig.num_requests
RENDER_TIME = RuntimeConfig.charttime
TIMEFRAMES = ChartTimeframe.display_list() if RuntimeConfig.is_mt4() else ChartTimeframe.list_values()


EXP_DICT = {
    ChartTimeframe.one_min: {"time_range": "3 days", "returned_time": 864},
    ChartTimeframe.five_min: {"time_range": "3 days", "returned_time": 864},
    ChartTimeframe.ten_min: {"time_range": "3 days", "returned_time": 432},
    ChartTimeframe.fifteen_min: {"time_range": "3 days", "returned_time": 288},
    ChartTimeframe.twenty_min: {"time_range": "7 days", "returned_time": 504},
    ChartTimeframe.thirty_min: {"time_range": "7 days", "returned_time": 336},
    ChartTimeframe.one_hour: {"time_range": "1 month", "returned_time": 720},
    ChartTimeframe.two_hour: {"time_range": "2 month", "returned_time": 720},
    ChartTimeframe.three_hour: {"time_range": "3 months", "returned_time": 720},
    ChartTimeframe.four_hour: {"time_range": "4 months", "returned_time": 720},
    ChartTimeframe.six_hour: {"time_range": "6 months", "returned_time": 720},
    ChartTimeframe.one_day: {"time_range": "1 year", "returned_time": 365},
    ChartTimeframe.one_week: {"time_range": "6 years", "returned_time": 260},
    ChartTimeframe.one_month: {"time_range": "12 years", "returned_time": 146},
    # "non specified": {"time_range": "3 days", "returned_time": None}
}


def calculate_percentile(response_times: List[float], percentile: int) -> float:
    """Calculate the nth percentile of response times"""
    return float(np.percentile(response_times, percentile))


def format_datetime(timestamp_ms: int) -> str:
    """Format datetime in a readable way"""
    dt = datetime.fromtimestamp(timestamp_ms / 1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def calculate_time_range(timeframe: ChartTimeframe) -> tuple[int, int]:
    """Calculate from and to timestamps based on timeframe to get at least 146 items"""
    now = datetime.now(UTC)

    # Map timeframe to timedelta
    timeframe_mapping = {
        ChartTimeframe.one_min: timedelta(days=3),
        ChartTimeframe.five_min: timedelta(days=3),
        ChartTimeframe.ten_min: timedelta(days=3),
        ChartTimeframe.fifteen_min: timedelta(days=3),
        ChartTimeframe.twenty_min: timedelta(days=7),
        ChartTimeframe.thirty_min: timedelta(days=7),
        ChartTimeframe.one_hour: timedelta(days=1 * 30),
        ChartTimeframe.two_hour: timedelta(days=2 * 30),
        ChartTimeframe.three_hour: timedelta(days=3 * 30),
        ChartTimeframe.four_hour: timedelta(days=4 * 30),
        ChartTimeframe.six_hour: timedelta(days=6 * 30),
        ChartTimeframe.one_day: timedelta(days=1 * 365),
        ChartTimeframe.one_week: timedelta(days=6 * 365),
        ChartTimeframe.one_month: timedelta(days=12 * 365)
    }

    # Calculate time range to get at least 146 items
    interval = timeframe_mapping[timeframe]
    from_time = now - interval

    # Convert to Unix timestamps in milliseconds
    from_ts = int(from_time.timestamp() * 1000)
    to_ts = int(now.timestamp() * 1000)

    return from_ts, to_ts


@pytest.mark.critical
@pytest.mark.parametrize("timeframe", TIMEFRAMES)
def test(timeframe):

    response_times = []
    result_counts = []
    failed_req = 0
    _trace_log = []

    logger.info("====================================")
    logger.info(f"- EXP response time: {RENDER_TIME} sec")
    logger.info(f"- Number of requests: {NUM_REQS}")

    # Calculate time range based on timeframe
    from_ts, to_ts = calculate_time_range(timeframe)

    # Make multiple API calls and collect response times
    for send_time in range(NUM_REQS):
        try:
            # Send API request
            resp = APIClient().chart.get_candlestick(
                symbol="AUDCAD.ecn",
                timeframe=timeframe,
                from_time=from_ts,
                to=to_ts,
                parse_result=False
            )

            # Check resp time
            response_time = round(resp.elapsed.total_seconds(), 3)
            response_times.append(response_time)

            # Check returned items amount
            resp_json = resp.json()
            result = resp_json.get('result', [])
            result_counts.append(len(result))

            request_format = f"<i>GET - {resp.url}</i>  →  {'<span style=\"color:red;font-weight:bold\">' if response_time > RENDER_TIME else ''}{response_time} sec{'</span>' if response_time > RENDER_TIME else ''}  -  returned {len(result)} items"
            _trace_log.append(f'<div style="color:green;margin-bottom: -15px;">{request_format}</div>')

        except requests.RequestException as e:
            failed_req += 1
            _trace_log.append(f"- Send request time: {send_time} failed with status: {resp.status_code} - {resp.text}")

    # Calculate percentiles
    p90 = calculate_percentile(response_times, 95)

    # check_result_counts = all(count == EXP_DICT[timeframe]['returned_time'] for count in result_counts)
    #
    # if not check_result_counts:
    #     failed_result_counts = [count for count in result_counts if count != EXP_DICT[timeframe]['returned_time']]

    # Create plain text description for allure report
    description = f"""
    <div style="background-color: #f5f5f5; padding: 10px; border-radius: 5px;">
        <h3 style="color: #2e5cb8; margin: 0;">API Performance Results</h3>
        <div style="margin-left: 20px;">
        Test Summary:<br>
        - Total API calls:     {NUM_REQS}<br>
        - Response Time (sec): {response_times}<br>
        - 95th percentile:     <b style="color:{'red' if p90 > RENDER_TIME else 'green'}">{p90:.3f}s</b><br>
        </div>
    </div>
    <br>
    <h3>Trace Log</h3>
    <div style="margin-left: 20px;">
    {f'<div style="color:red">No trace log available</div>' if not _trace_log else '<br>'.join(_trace_log)}
    </div>
    """

    # Log results to allure report
    allure.dynamic.description_html(description)

    # Verify 90th percentile is within expected threshold
    is_within_threshold = p90 <= RENDER_TIME
    assert is_within_threshold, f"90th percentile response time ({p90:.3f}s) exceeds 2.0s threshold for timeframe {timeframe}"

    # Assert the minimum items requirement
    # assert check_result_counts, f"{len(failed_result_counts)} request returned in correct amount of items"
