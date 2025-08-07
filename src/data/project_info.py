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
    allure_dir: str = None
    env: str = None
    client: str = None
    server: str = None
    account: str = None

    platform: str = None
    browser: str = None
    headless: str = None
    argo_cd: str = None

    user: str = None
    password: str = None
    url: str = None

    headers: dict = {}

    @classmethod
    def is_non_oms(cls):
        return cls.client == "transactCloud"

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
