from allure_commons.utils import now


class StepLogs:
    steps_with_time = {}
    test_steps = []
    setup_steps = dict()
    teardown_steps = dict()
    broken_steps = []
    all_failed_logs = []
    failed_logs_dict = {}

    TEST_ID = ""

    @classmethod
    def init_test_logs(cls):
        cls.steps_with_time[cls.TEST_ID] = []
        cls.failed_logs_dict[cls.TEST_ID] = []

    @classmethod
    def add_step(cls, msg_log):
        cls.test_steps.append(msg_log)
        cls.steps_with_time[cls.TEST_ID].append((msg_log, now()))

    @classmethod
    def add_setup_step(cls, msg_log):
        cls.setup_steps |= msg_log

    @classmethod
    def add_teardown_step(cls, msg_log):
        cls.teardown_steps |= msg_log


    @classmethod
    def clean_step(cls):
        cls.test_steps = []

    @classmethod
    def add_failed_log(cls, msg_log, failed_detail=""):
        cls.all_failed_logs.append((msg_log, failed_detail))
        cls.failed_logs_dict[cls.TEST_ID].append((msg_log, failed_detail))

class DriverList:
    web_driver = []
    android_driver = []
    ios_driver = []
    all_drivers = {}


class RuntimeConfig:
    allure_dir: str = ""
    env: str = ""
    client: str = ""
    server: str = ""
    account: str = ""

    platform: str = ""
    browser: str = ""
    headless: str = ""
    argo_cd: str = ""

    user: str = ""
    password: str = ""
    url: str = ""

    headers: dict = {}

    charttime: int = 2

    @classmethod
    def is_non_oms(cls):
        return cls.client.lower() not in ["lirunex"]

    @classmethod
    def is_prod(cls):
        return cls.env == "prod"

    @classmethod
    def is_mt4(cls):
        return cls.server == "mt4"

    @classmethod
    def is_mt5(cls):
        return cls.server == "mt5"

    @classmethod
    def is_web(cls):
        return cls.platform == "web"

    @classmethod
    def is_demo(cls):
        return cls.account == "demo"

    @classmethod
    def is_live(cls):
        return cls.account == "live"

    @classmethod
    def is_crm(cls):
        return cls.account == "crm"
