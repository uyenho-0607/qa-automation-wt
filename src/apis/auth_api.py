from src.apis.api_base import BaseAPI
from src.core.config_manager import Config
from src.data.enums import Client, AccountType
from src.data.project_info import RuntimeConfig


class AuthAPI(BaseAPI):
    __headers = {"content-type": "application/json", "user-agent": "automation-team-client"}

    endpoints = {
        Client.LIRUNEX: {
            AccountType.CRM: "/auth/v1/company/login",
            AccountType.DEMO: "/auth/v2/company/demo/login"
        },
        Client.TRANSACT_CLOUD: {
            AccountType.LIVE: "/auth/v2/metatrader5/live/login",
            AccountType.DEMO: "/auth/v2/metatrader5/demo/login",
        }
    }

    def __init__(self, userid: str = None, password: str = None):
        super().__init__(self.__headers)
        self.userid = userid
        self.password = password
        self.client = RuntimeConfig.client
        self.account_type = RuntimeConfig.account or AccountType.LIVE
        self.get_token()

    def get_token(self):
        if "Authorization" not in RuntimeConfig.headers:
            credentials = Config.credentials()
            payload = {
                "source": "WEB",
                "password": self.password or credentials.password,
                "userId": self.userid or credentials.username
            }

            resp = self.post(
                # endpoint=self.endpoints[self.client][self.account_type],
                endpoint=self.endpoints.get(self.client, self.endpoints.get(Client.TRANSACT_CLOUD))[self.account_type],
                payload=payload
            )

            self.__headers["Authorization"] = f"Bearer {resp['token']}"
            RuntimeConfig.headers = self.__headers
            return self.__headers

        return self.__headers
