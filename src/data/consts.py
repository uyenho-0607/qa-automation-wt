from pathlib import Path

from src.data.enums import Client, Server
from src.data.project_info import ProjectConfig

# Framework Paths
ROOTDIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOTDIR / "config"
VIDEO_DIR = ROOTDIR / ".videos"
SRC_DIR = ROOTDIR / "src"
DATA_DIR = SRC_DIR / "data"
GRID_SERVER = "http://aqdev:aq123@selenium-grid.aquariux.dev/wd/hub"

# Timeouts (in seconds)
EXPLICIT_WAIT = 10
IMPLICIT_WAIT = 0
PAGE_LOAD_WAIT = 30
SHORT_WAIT = 2
LONG_WAIT = 15
QUICK_WAIT = 0.5

CHECK_ICON = "✔"
FAILED_ICON = "✘"

SYMBOLS = {
    Client.TRANSACT_CLOUD: {
        # Server.MT5: ["BAKE.USD", "AXS.USD", "ICP.USD", "DOGE.USD"]
        Server.MT5: ["BAKE.USD", "AXS.USD", "DASH.USD"]
    },
    Client.LIRUNEX: {
        Server.MT5: ["DASHUSD.std", "XRPUSD.std"],
        Server.MT4: ["DASHUSD.std", "XRPUSD.std"]
    }
}

# supporting methods
def get_symbols():
    return SYMBOLS[ProjectConfig.client][ProjectConfig.server]