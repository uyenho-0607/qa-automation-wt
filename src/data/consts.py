from pathlib import Path

from src.data.enums import Client, Server
from src.data.project_info import RuntimeConfig

# Framework Paths
ROOTDIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOTDIR / "config"
VIDEO_DIR = ROOTDIR / ".videos"
SRC_DIR = ROOTDIR / "src"
DATA_DIR = SRC_DIR / "data"
GRID_SERVER = "http://aqdev:aq123@selenium-grid.aquariux.dev/wd/hub"
GRID_VIDEO_URL = "https://selenium-grid-videos.aquariux.dev"

# Timeouts (in seconds)
EXPLICIT_WAIT = 10
IMPLICIT_WAIT = 0
PAGE_LOAD_WAIT = 30
SHORT_WAIT = 2
LONG_WAIT = 15
QUICK_WAIT = 0.5

CHECK_ICON = "✔"
FAILED_ICON = "✘"


MULTI_OMS = [Client.LIRUNEX]

SYMBOLS = {
    Client.TRANSACT_CLOUD: {
        Server.MT5: ["BAKE.USD", "AXS.USD", "DASH.USD"]
    },
    Client.LIRUNEX: {
        Server.MT5: ["DASHUSD.std", "XRPUSD.std"],
        Server.MT4: ["DASHUSD.std", "XRPUSD.std"]
    }
}

# supporting methods
def get_symbols():
    symbol_list = SYMBOLS
    if RuntimeConfig.is_prod():
        symbol_list = {
            Client.TRANSACT_CLOUD: {
                Server.MT5: ["BAKEUSD.d", "AXSUSD.d"]
            },
            Client.LIRUNEX: {
                Server.MT5: ["DASHUSD.std", "XRPUSD.std"],
                Server.MT4: ["DASHUSD.std", "XRPUSD.std"]
            }
        }

    # return symbol_list[RuntimeConfig.client][RuntimeConfig.server]
    return symbol_list.get(RuntimeConfig.client, symbol_list.get(Client.TRANSACT_CLOUD))[RuntimeConfig.server]


def get_symbol_details(symbol):
    details = {
        "AXS.USD": dict(point_step=0.01, decimal=2),
        "AXSUSD.d": dict(point_step=0.01, decimal=2),
        "BAKE.USD": dict(point_step=0.0001, decimal=4),
        "BAKEUSD.d": dict(point_step=0.0001, decimal=4),
        "DASH.USD": dict(point_step=0.01, decimal=2),
        "DASHUSD.std": dict(point_step=0.01, decimal=2),
        "XRPUSD.std": dict(point_step=0.0001, decimal=4),
    }
    return details.get(symbol)
