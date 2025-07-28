from typing import Any

import yaml

from src.data.consts import CONFIG_DIR
from src.data.enums import Client, Server, AccountType, URLSites, URLPaths
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

        server = cls.config.get("server", Server.MT5)
        account = cls.config.get("account", AccountType.DEMO)
        cis_username = cls.config.get("user")

        match site:
            case URLSites.ROOT_ADMIN:
                username = cls._full_config.user_root
                password = cls._full_config.password_root

            case URLSites.ADMIN_PORTAL:
                username = cls._full_config.user_admin
                password = cls._full_config.password_admin

            case _:
                credentials = cls.config.credentials[server]
                username = cis_username or credentials[f'user_{account.lower()}']
                encrypted_password = cls._full_config.get(f"password_{account.lower()}", cls._full_config["password"])
                password = decrypt_password(encrypted_password)
                
        return DotDict(username=username, password=password)

    @classmethod
    def urls(cls, site: URLSites = URLSites.MEMBER_SITE):
        if not cls.config:
            cls.load_config()

        match site:
            case URLSites.ROOT_ADMIN:
                return cls._full_config.root_url

            case URLSites.ADMIN_PORTAL:
                return cls.config.bo_url

            case _:
                return cls.config.base_url if cls.config.platform == "web" else cls.config.web_app_url

    @classmethod
    def url_path(cls, path: URLPaths | str):
        """Get full URL including path."""
        base_url = cls.urls()

        if path == URLPaths.TRADE:
            return base_url

        return f"{base_url}/{path}"

    @classmethod
    def mobile(cls, platform=None):
        if not cls.config:
            cls.load_config()

        platform = platform or cls.config.get("platform", "android")

        mobile_config = DotDict(
            android=dict(app_id=cls.config.mobile.app_package, device_udid=cls._full_config.android_udid),
            ios=dict(app_id=cls.config.mobile.app_bundle, device_udid=cls._full_config.ios_udid),

        )

        return mobile_config[platform]
