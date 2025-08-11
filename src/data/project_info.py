class DriverList:
    web_driver = []
    android_driver = []
    ios_driver = []
    all_drivers = {}


class StepLogs:
    test_steps = []
    broken_steps = []
    all_failed_logs = []
    failed_logs_dict = {}


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
