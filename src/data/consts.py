from pathlib import Path

from src.data.enums import Client, Server
from src.data.project_info import RuntimeConfig

# Framework Paths
ROOTDIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOTDIR / "config"
VIDEO_DIR = ROOTDIR / ".videos"
SRC_DIR = ROOTDIR / "src"
DATA_DIR = SRC_DIR / "data"
CHECK_ICON = "✔"
FAILED_ICON = "✘"

NON_OMS = [Client.TRANSACT_CLOUD]
MULTI_OMS = [Client.LIRUNEX]
