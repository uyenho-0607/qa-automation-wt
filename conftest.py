import os.path
import shutil

import allure
import pytest
from allure_commons.types import Severity

from src.core.config_manager import Config
from src.core.driver.driver_manager import DriverManager
from src.data.consts import ROOTDIR, VIDEO_DIR, MULTI_OMS, WEB_APP_DEVICE
from src.data.enums import Server, Client, AccountType
from src.data.project_info import DriverList, RuntimeConfig, StepLogs
from src.utils.allure_utils import attach_screenshot, log_step_to_allure, custom_allure_report, attach_video
from src.utils.logging_utils import logger


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--env", default="sit", help="Environment to run tests (sit, release_sit, uat)")
    parser.addoption("--client", default="lirunex", help="Client to test (lirunex, transactCloud) - single value only")
    parser.addoption("--server", default="mt4", help="Server type to test (mt4 or mt5)")
    parser.addoption("--account", default="demo", help="Account type to test (demo/ live/ crm)")
    parser.addoption("--platform", default="", help="Platform to run tests (web, ios, android), used for init the driver")
    parser.addoption("--user", help="Custom username")
    parser.addoption("--password", help="Custom raw password")
    parser.addoption("--url", help="Custom tenant url")
    parser.addoption("--browser", default="chrome", help="Browser for web tests (chrome, firefox, safari)")
    parser.addoption("--headless", default=False, action="store_true", help="Run browser in headless mode")
    parser.addoption("--cd", default=False, action="store_true", help="Whether to choose driver to run on argo cd")


def pytest_configure(config):
    allure_dir = config.option.allure_report_dir
    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        shutil.rmtree(allure_dir)
        os.makedirs(ROOTDIR / allure_dir)


def pytest_sessionstart(session: pytest.Session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.debug("============ pytest_sessionstart ============ ")

    # Get initial platform from command line
    platform = session.config.getoption("platform")

    if "tests" in str(session.config.args):
        split_path = session.config.args[0].split("/")
        test_index = split_path.index("tests")

    else:
        split_path = os.getcwd().split("/")
        test_index = split_path.index("tests")

    platform = platform or split_path[test_index + 1]
    logger.info(f">> Platform: {platform.replace('_', ' ').capitalize()!r}")

    ######## System Options ########
    argo_cd = session.config.getoption("cd")
    env = session.config.getoption("env")
    client = session.config.getoption("client")
    server = session.config.getoption("server")
    account = session.config.getoption("account")

    if account == AccountType.LIVE and client == Client.LIRUNEX:
        account = "crm"

    if client not in MULTI_OMS:
        server = Server.MT5

    user = session.config.getoption("user")
    password = session.config.getoption("password")
    url = session.config.getoption("url")

    browser = session.config.getoption("browser")
    headless = session.config.getoption("headless")
    allure_dir = session.config.getoption("allure_report_dir")

    logger.info(f">> Load environment configuration - Client: {client.capitalize()!r}")
    logger.info(f">> Account: {account.capitalize()!r}")
    Config.load_config(env, client)

    # Save options to Runtime Config
    RuntimeConfig.allure_dir = allure_dir
    RuntimeConfig.argo_cd = argo_cd
    RuntimeConfig.env = env
    RuntimeConfig.browser = browser
    RuntimeConfig.user = user
    RuntimeConfig.url = url
    RuntimeConfig.password = password
    RuntimeConfig.headless = headless
    RuntimeConfig.client = client
    RuntimeConfig.server = server
    RuntimeConfig.account = account
    RuntimeConfig.platform = platform


def pytest_collection_modifyitems(config, items):
    for item in items:
        if any(value in item.nodeid for value in ["stop_limit", "stop limit"]):
            item.add_marker("non_oms")


def pytest_runtest_setup(item: pytest.Item):
    """Setup test and configure Allure reporting"""

    server = RuntimeConfig.server
    account = RuntimeConfig.account

    # Set up Allure test structure
    module = item.nodeid.split("::")[0].split("/")[2:-1]  # not count test, web, and test name
    sub_suite = " - ".join(item.capitalize() for item in module)
    sub_suite = sub_suite.replace("_", " ").title()

    # Set allure labels
    parent_suite = RuntimeConfig.client.upper()
    # if RuntimeConfig.is_prod() and RuntimeConfig.url:  # dynamically handle client for prod (todo: still need enhancement)
    #     url = Config.urls()
    #     parent_suite = url.split(".")[-2].upper()

    allure.dynamic.parent_suite(parent_suite)
    allure.dynamic.suite(server.upper())
    allure.dynamic.sub_suite(sub_suite)

    if item.get_closest_marker("critical"):
        allure.dynamic.severity(Severity.CRITICAL)

    if RuntimeConfig.user:
        item.add_marker(f"user: {RuntimeConfig.user}")

    if item.get_closest_marker("non_oms") and not RuntimeConfig.is_non_oms():
        pytest.skip("This test is for Non-OMS server only !")

    if item.get_closest_marker("not_demo") and RuntimeConfig.is_demo():
        pytest.skip("This test is not for demo account !")

    if item.get_closest_marker("not_live") and RuntimeConfig.is_live():
        pytest.skip("This test is not for live account !")

    if item.get_closest_marker("not_crm") and RuntimeConfig.is_crm():
        pytest.skip("This test is not for crm account !")

    print("\x00")  # print a non-printable character to break a new line on console
    logger.info(f"- Running test case: {item.parent.name} - [{server}] - [{account}] ")
    logger.debug(f"- user: {Config.credentials().username!r}")


def pytest_sessionfinish(session: pytest.Session):
    logger.debug("===== pytest_sessionfinish ==== ")

    DriverManager.quit_driver(RuntimeConfig.platform)
    allure_dir = RuntimeConfig.allure_dir

    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        custom_allure_report(allure_dir)  # custom allure report

        # Set allure report properties
        browser = RuntimeConfig.browser
        platform = f"{RuntimeConfig.platform.capitalize()}" + (f" - {browser.capitalize()}" if RuntimeConfig.is_web() else "")
        if platform.lower() == "web_app":
            platform += f" - {WEB_APP_DEVICE}"

        env_data = {
            "Platform": platform.replace("_", " ").title(),
            "Environment": RuntimeConfig.env.capitalize(),
            "Account": "Live/Crm" if RuntimeConfig.account != AccountType.DEMO else AccountType.DEMO.capitalize(),
        }

        with open(f"{allure_dir}/environment.properties", "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")


@pytest.hookimpl(hookwrapper=True, tryfirst=TypeError)
def pytest_runtest_makereport(item, call):
    """Handle test reporting and Allure steps"""
    outcome = yield
    report = outcome.get_result()

    platform = RuntimeConfig.platform
    driver = DriverList.all_drivers.get(platform)
    allure_dir = RuntimeConfig.allure_dir

    # Start recording at the beginning of the test
    if driver and report.when == "setup":
        if platform in ['android', 'ios']:
            if allure_dir and os.path.exists(ROOTDIR / allure_dir):
                try:
                    driver.start_recording_screen(options={"bit_rate": 200000, "video_size": "480x270"})
                    logger.debug(f"Started screen recording for {platform} test")

                except Exception as e:
                    logger.error(f"Failed to start screen recording: {str(e)}")

        if report.failed:
            attach_screenshot(driver, name="setup")
            logger.error(f"Test setup failed: {report.longreprtext}")

    # Handle test completion
    if report.when == "call":
        if allure_dir and os.path.exists(ROOTDIR / allure_dir):
            log_step_to_allure()  # show test steps on allure

            if driver and RuntimeConfig.platform in ["android", "ios"]:
                try:
                    # Attach video for mobile
                    attach_video(driver)
                except Exception as e:
                    logger.error(f"Failed to handle video recording: {str(e)}")

            # if RuntimeConfig.platform.lower() in ["web", "web_app"]:
            #     logger.debug("- Attach session video")
            #     attach_session_video()

        if report.failed and "FAILURE" in report.longreprtext:
            StepLogs.all_failed_logs.append(("end_test", ""))

            # if RuntimeConfig.platform.lower() in ["web", "web_app"]:
            #     logger.debug("- Attach session video")
            #     attach_session_video()

    if report.when == "teardown":
        if allure_dir and os.path.exists(ROOTDIR / allure_dir):
            if report.failed and driver:
                attach_screenshot(driver, name="teardown")
                logger.error(f"Test teardown failed: {report.longreprtext}")


@pytest.fixture(scope="session", autouse=True)
def setup_video_folder():
    if RuntimeConfig.platform in ["android", "ios"] and Config.config.allure_dir:
        if os.path.exists(VIDEO_DIR):
            shutil.rmtree(VIDEO_DIR)

        os.makedirs(VIDEO_DIR)
