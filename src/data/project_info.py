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
