from pathlib import Path

from src.data.enums import Server
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
IMPLICIT_WAIT = 5
PAGE_LOAD_WAIT = 30
SHORT_WAIT = 2
QUICK_WAIT = 0.5

CHECK_ICON = "✔"
FAILED_ICON = "✘"

SYMBOLS = {
    Server.MT5: [
        "BAKE.USD",
        "DASH.USD",
        "AXS.USD",
    ],
    Server.MT4: [
        "DASHUSD.std",
        "XRPUSD.std",
        "LTCUSD.std"
    ]
}

CRYPTO_SYMBOLS = {
    Server.MT5: ["AVAX.USD", "AXS.USD", "BAKE.USD", "DASH.USD", "DOGE.USD"],
    Server.MT4: ["BTCUSD.std", "DASHUSD.std", "ETHUSD.std", "LTCUSD.std", "XRPUSD.std"]
}