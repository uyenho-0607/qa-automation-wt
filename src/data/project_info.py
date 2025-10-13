class StepLogs:
    test_steps = []
    broken_steps = []
    all_failed_logs = []
    failed_logs_dict = {}
    TEST_ID = ""

    @classmethod
    def init_test_logs(cls):
        cls.failed_logs_dict[cls.TEST_ID] = []

    @classmethod
    def add_step(cls, msg_log):
        cls.test_steps.append(msg_log)

    @classmethod
    def add_failed_log(cls, msg_log, failed_detail=""):
        cls.all_failed_logs.append((msg_log, failed_detail))
        cls.failed_logs_dict[cls.TEST_ID].append((msg_log, failed_detail))


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
