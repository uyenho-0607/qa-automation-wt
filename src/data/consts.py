from pathlib import Path

from src.data.enums import Client

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
    Client.TRANSACT_CLOUD: [
        "BAKE.USD",
        "DASH.USD",
        "AXS.USD",
    ],
    Client.LIRUNEX: [
        "DASHUSD.std",
        "XRPUSD.std",
        "LTCUSD.std"
    ]
}
