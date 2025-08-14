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

WEB_APP_DEVICE = "iPhone 14 Pro Max"

MULTI_OMS = [Client.LIRUNEX]
