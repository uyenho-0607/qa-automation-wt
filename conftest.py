import os.path
import shutil

import allure
import pytest

from src.core.config_manager import Config
from src.data.consts import ROOTDIR, NON_OMS
from src.data.enums import Server, Client, AccountType
from src.data.project_info import RuntimeConfig, StepLogs
from src.utils.allure_utils import log_step_to_allure, custom_allure_report
from src.utils.logging_utils import logger


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--env", default="sit", help="Environment to run tests (sit, uat, release_sit)")
    parser.addoption("--client", default="lirunex", help="Client to test (lirunex, transactCloud)")
    parser.addoption("--server", default="mt4", help="Server type to test (mt4 or mt5)")
    parser.addoption("--account", default="demo", help="Account type to test (demo, live)")
    parser.addoption("--user", help="Custom username")
    parser.addoption("--password", help="Custom raw password")


def pytest_configure(config):
    allure_dir = config.option.allure_report_dir
    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        shutil.rmtree(allure_dir)
        os.makedirs(ROOTDIR / allure_dir)


def pytest_sessionstart(session: pytest.Session):
    print("\x00")  # print a non-printable character to break a new line on console
    logger.debug("============ pytest_sessionstart ============ ")
    logger.info(">> Platform: Chart Data API Testing")

    ######## System Options ########
    env = session.config.getoption("env")
    client = session.config.getoption("client")
    server = session.config.getoption("server")
    account = session.config.getoption("account")

    if account == AccountType.LIVE and client == Client.LIRUNEX:
        account = "crm"

    if client in NON_OMS:
        server = Server.MT5

    user = session.config.getoption("user")
    password = session.config.getoption("password")
    allure_dir = session.config.getoption("allure_report_dir")

    logger.info(f">> Load environment configuration - Client: {client.capitalize()!r}")
    logger.info(f">> Account: {account.capitalize()!r}")
    logger.info(f">> Server: {server.upper()!r}")
    Config.load_config(env, client)

    # Save options to Runtime Config
    RuntimeConfig.allure_dir = allure_dir
    RuntimeConfig.env = env
    RuntimeConfig.user = user
    RuntimeConfig.password = password
    RuntimeConfig.client = client
    RuntimeConfig.server = server
    RuntimeConfig.account = account
    RuntimeConfig.platform = "api"


def pytest_runtest_setup(item: pytest.Item):
    """Setup test and configure Allure reporting"""

    server = RuntimeConfig.server
    account = RuntimeConfig.account

    # Set allure labels
    allure.dynamic.parent_suite("MetaTrader API Validation")

    print("\x00")  # print a non-printable character to break a new line on console
    logger.info(f"- Running test case: {item.name.replace("test_", "").replace("_", " ").title()} - [{server.upper()}] - [{account.upper()}]")
    logger.debug(f"- user: {Config.credentials().username!r}")


def pytest_sessionfinish(session: pytest.Session):
    logger.debug("===== pytest_sessionfinish ==== ")

    allure_dir = RuntimeConfig.allure_dir

    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        custom_allure_report(allure_dir)  # custom allure report

        # Set allure report properties
        env_data = {
            "Platform": "Chart Data API Testing",
            "Environment": RuntimeConfig.env.upper(),
            "Client": RuntimeConfig.client.upper(),
            "Server": RuntimeConfig.server.upper(),
            "Account": RuntimeConfig.account.upper(),
        }

        with open(f"{allure_dir}/environment.properties", "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")


@pytest.hookimpl(hookwrapper=True, tryfirst=TypeError)
def pytest_runtest_makereport(item, call):
    """Handle test reporting and Allure steps"""
    outcome = yield
    report = outcome.get_result()
    allure_dir = RuntimeConfig.allure_dir

    # Handle test completion
    if report.when == "call":
        if allure_dir and os.path.exists(ROOTDIR / allure_dir):
            log_step_to_allure()  # show test steps on allure

        if report.failed and "FAILURE" in report.longreprtext:
            StepLogs.all_failed_logs.append("end_test")
