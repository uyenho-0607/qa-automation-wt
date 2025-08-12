from typing import Any

import yaml

from src.data.consts import CONFIG_DIR
from src.data.enums import Client, Server, AccountType, URLSites
from src.data.project_info import RuntimeConfig
from src.utils import DotDict
from src.utils.encrypt_utils import decrypt_password


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
    def credentials(cls, site=URLSites.MEMBER_SITE):
        if not cls.config:
            cls.load_config()

        server = RuntimeConfig.server or Server.MT5
        account = RuntimeConfig.account or AccountType.LIVE
        cus_username = RuntimeConfig.user
        cus_password = RuntimeConfig.password

        match site:
            case URLSites.ROOT_ADMIN:
                username = cls._full_config.user_root
                password = cls._full_config.password_root

            case URLSites.ADMIN_PORTAL:
                username = cls._full_config.user_admin
                password = cls._full_config.password_admin

            case _:
                credentials = cls.config.credentials[server]
                username = cus_username or credentials[f'user_{account.lower()}']
                encrypted_password = cls._full_config.get(f"password_{account.lower()}", cls._full_config["password"])
                password = cus_password or decrypt_password(encrypted_password)

        return DotDict(username=username, password=password)

    @classmethod
    def urls(cls, site: URLSites = URLSites.MEMBER_SITE):
        if not cls.config:
            cls.load_config()

        cus_url = RuntimeConfig.url

        match site:
            case URLSites.ROOT_ADMIN:
                return cls._full_config.root_url

            case URLSites.ADMIN_PORTAL:
                return cls.config.bo_url

            case _:
                return cus_url or cls.config.base_url + ("/web" if RuntimeConfig.platform == "web" else "/mobile")
