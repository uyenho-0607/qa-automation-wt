from src.apis.api_base import BaseAPI
from src.data.enums import AccSummary, AccInfo
from src.data.project_info import RuntimeConfig
from src.utils.logging_utils import logger


class StatisticsAPI(BaseAPI):
    _endpoint = "/statistics/v1/account"

    def __init__(self):
        super().__init__(headers=RuntimeConfig.headers)

    def get_account_statistics(self, get_acc_balance=False, get_asset_acc=False):
        logger.info("[API] GET account statistic")
        resp = self.get(endpoint=self._endpoint)

        if get_acc_balance:
            acc_info = resp["accountBalance"]
            account_overview = {
                AccSummary.BALANCE: acc_info["balance"],
                AccSummary.MARGIN_USED: acc_info["margin"],
                AccSummary.PROFIT_LOSS: acc_info["profitLoss"],
                AccSummary.FREE_MARGIN: acc_info["freeMargin"],
                AccSummary.EQUITY: acc_info["equity"],
                AccSummary.MARGIN_LEVEL: acc_info["marginLevel"],
                AccSummary.STOP_OUT_LEVEL: acc_info["marginStopout"],
                AccSummary.MARGIN_CALL: acc_info["marginCall"]
            }
            return account_overview

        if get_asset_acc:
            account_overview = {
                AccInfo.BALANCE: resp["accountBalance"]["balance"],
                AccInfo.REALISED_PROFIT_LOSS: resp["realisedProfit"],
                AccInfo.WITHDRAWAL: resp["withdrawal"],
                AccInfo.DEPOSIT: resp["deposit"],
                AccInfo.CREDIT: resp["credit"]
            }

            return account_overview

        return resp
