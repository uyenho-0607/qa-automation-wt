import os.path
import shutil

import allure
import pytest
from allure_commons.types import Severity

from src.core.config_manager import Config
from src.core.driver.driver_manager import DriverManager
from src.data.consts import ROOTDIR, VIDEO_DIR
from src.data.enums import Server, Client, AccountType
from src.data.project_info import DriverList, ProjectConfig, StepLogs
from src.utils.allure_utils import attach_screenshot, log_step_to_allure, custom_allure_report, attach_video
from src.utils.logging_utils import logger
from src.utils.allure_utils import attach_session_video


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--env", default="sit", help="Environment to run tests (sit, release_sit, uat)")
    parser.addoption("--client", default="lirunex", help="Client to test (lirunex, transactCloud) - single value only")
    parser.addoption("--server", default="mt4", help="Server type to test (mt4 or mt5)")
    parser.addoption("--account", default="demo", help="Account type to test (demo/ live/ crm)")
    parser.addoption("--platform", default="", help="Platform to run tests (web, ios, android), used for init the driver")
    parser.addoption("--user", help="Custom username")
    parser.addoption("--browser", default="chrome", help="Browser for web tests (chrome, firefox, safari)")
    parser.addoption("--headless", default=False, action="store_true", help="Run browser in headless mode")
    parser.addoption("--cd", default=True, action="store_true", help="Whether to choose driver to run on argo cd")


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

    if client == Client.TRANSACT_CLOUD:
        server = Server.MT5

    user = session.config.getoption("user")
    browser = session.config.getoption("browser")
    headless = session.config.getoption("headless")
    allure_dir = session.config.getoption("allure_report_dir")

    logger.info(f">> Load environment configuration - Client: {client.capitalize()!r}")
    logger.info(f">> Account: {account.capitalize()!r}")
    Config.load_config(env, client)

    # Save options config to Config
    Config.config.argo_cd = argo_cd
    Config.config.env = env
    Config.config.browser = browser
    Config.config.user = user
    Config.config.headless = headless
    Config.config.allure_dir = allure_dir

    Config.config.client = client
    ProjectConfig.client = client

    Config.config.server = server
    ProjectConfig.server = server

    Config.config.account = account
    ProjectConfig.account = account

    Config.config.platform = platform
    ProjectConfig.platform = platform


def pytest_collection_modifyitems(config, items):
    for item in items:
        if any(value in item.nodeid for value in ["stop_limit", "stop limit"]):
            item.add_marker("non_oms")


def pytest_runtest_setup(item: pytest.Item):
    """Setup test and configure Allure reporting"""
    server = Config.config.server
    account = Config.config.account

    # Set up Allure test structure
    module = item.module.__name__.split(".")[2:-1]  # not count test, web, and test name
    sub_suite = " - ".join(item.capitalize() for item in module)
    sub_suite = sub_suite.replace("_", " ").title()

    # Set allure labels
    allure.dynamic.parent_suite(ProjectConfig.client.upper())
    allure.dynamic.suite(server.upper())
    allure.dynamic.sub_suite(sub_suite)

    if item.get_closest_marker("critical"):
        allure.dynamic.severity(Severity.CRITICAL)

    if Config.config.user:
        item.add_marker(f"user: {Config.config.user}")

    if item.get_closest_marker("uat") and Config.config.env != "uat":
        pytest.skip("This test is for UAT environment only !")

    if item.get_closest_marker("non_oms") and not ProjectConfig.is_non_oms():
        pytest.skip("This test is for Non-OMS server only !")

    if item.get_closest_marker("not_demo") and ProjectConfig.is_demo():
        pytest.skip("This test is not for demo account !")

    if item.get_closest_marker("not_live") and ProjectConfig.is_live():
        pytest.skip("This test is not for live account !")

    if item.get_closest_marker("not_crm") and ProjectConfig.is_crm():
        pytest.skip("This test is not for crm account !")

    print("\x00")  # print a non-printable character to break a new line on console
    logger.info(f"- Running test case: {item.parent.name} - [{server}] - [{account}] ")
    logger.debug(f"- user: {Config.credentials().username!r}")


def pytest_sessionfinish(session: pytest.Session):
    logger.debug("===== pytest_sessionfinish ==== ")

    driver = DriverList.all_drivers.get(Config.config.platform)
    if driver:
        DriverManager.quit_driver(Config.config.platform)

    allure_dir = Config.config.allure_dir
    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        custom_allure_report(allure_dir)  # custom allure report

        # Set allure report properties
        browser = Config.config.browser
        platform = f"{ProjectConfig.platform.capitalize()}" + (f" - {browser.capitalize()}" if ProjectConfig.is_web() else "")

        env_data = {
            "Platform": platform,
            "Environment": Config.config.env.capitalize(),
            "Account": "Live/Crm" if ProjectConfig.account != AccountType.DEMO else AccountType.DEMO.capitalize(),
        }

        with open(f"{allure_dir}/environment.properties", "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")


@pytest.hookimpl(hookwrapper=True, tryfirst=TypeError)
def pytest_runtest_makereport(item, call):
    """Handle test reporting and Allure steps"""
    outcome = yield
    report = outcome.get_result()

    platform = Config.config.platform
    driver = DriverList.all_drivers.get(platform)
    allure_dir = Config.config.allure_dir

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

            if driver:
                try:
                    # Attach video for mobile
                    attach_video(driver)
                except Exception as e:
                    logger.error(f"Failed to handle video recording: {str(e)}")

        if report.failed and "FAILURE" in report.longreprtext:
            StepLogs.all_failed_logs.append(("end_test", ""))
            # if ProjectConfig.is_web():
            #     attach_session_video()

    if report.when == "teardown":
        if allure_dir and os.path.exists(ROOTDIR / allure_dir):
            if report.failed and driver:
                attach_screenshot(driver, name="teardown")
                logger.error(f"Test teardown failed: {report.longreprtext}")


@pytest.fixture(scope="session", autouse=True)
def setup_video_folder():
    if not ProjectConfig.is_web() and Config.config.allure_dir:
        if os.path.exists(VIDEO_DIR):
            shutil.rmtree(VIDEO_DIR)

        os.makedirs(VIDEO_DIR)
