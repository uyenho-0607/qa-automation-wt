from typing import Any

import yaml

from src.data.consts import CONFIG_DIR
from src.data.enums import Client, Server, AccountType
from src.data.project_info import RuntimeConfig
from src.utils import DotDict


class Config:
    _full_config: DotDict[str, Any] = DotDict()
    config: DotDict[str, Any] = DotDict()  # Config of specific client

    @classmethod
    def load_config(cls, env: str = "sit", client=Client.TRANSACT_CLOUD) -> None:
        """Load configuration from YAML file."""
        config_file = CONFIG_DIR / f"{env}.yaml"
        with open(config_file, "r") as f:
            cls._full_config = DotDict(yaml.safe_load(f))
            cls.config = DotDict(cls._full_config.get(client, {}))

    @classmethod
    def credentials(cls):
        if not cls.config:
            cls.load_config()

        server = RuntimeConfig.server or Server.MT5
        account = RuntimeConfig.account or AccountType.LIVE

        credentials = cls.config.credentials[server]
        username = RuntimeConfig.user or credentials[f'user_{account.lower()}']
        password = cls._full_config.get(f"password_{account.lower()}", cls._full_config["password"])
        password = RuntimeConfig.password or password

        return DotDict(username=username, password=password)
