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


class ProjectConfig:
    client: str = None
    server: str = None
    account: str = None
    platform: str = "web"
    headers: dict = {}

    @classmethod
    def is_non_oms(cls):
        return cls.client == "transactCloud"

    @classmethod
    def is_mt4(cls):
        return cls.client == "mt4"

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
