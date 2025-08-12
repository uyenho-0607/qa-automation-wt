from pathlib import Path

from src.data.enums import Client, Server

# Framework Paths
ROOTDIR = Path(__file__).parent.parent.parent
CONFIG_DIR = ROOTDIR / "config"
SRC_DIR = ROOTDIR / "src"
DATA_DIR = SRC_DIR / "data"

NON_OMS = [Client.TRANSACT_CLOUD]

# MacOS
CSV_DIR = {
    Server.MT5: r"~/Library/Application Support/net.metaquotes.wine.metatrader5/drive_c/Program Files/MetaTrader 5/MQL5/Files/",
    Server.MT4: r"~/Library/Application Support/net.metaquotes.wine.metatrader4/drive_c/Program Files (x86)/MetaTrader 4/MQL4/Files/"
}

# # WINDOWS
# CSV_DIR = {
#     Server.MT5: r"C:\Program Files\MetaTrader 5\MQL5\Files" + "\\",
#     Server.MT4: r"C:\Program Files (x86)\MetaTrader 4\MQL4\Files" + "\\"
# }

TOLERANCE_PERCENT = 0.1