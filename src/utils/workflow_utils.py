import builtins
import logging
import os
import socket
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from shutil import which
from typing import List, Dict, Optional

import gspread.exceptions
import requests.exceptions
from google.oauth2.service_account import Credentials

from src.data.consts import ROOTDIR
from src.utils.logging_utils import logger

google_sa_creds = os.getenv('GOOGLE_SA_CREDENTIALS')


class GoogleSheetsAPI:
    _sheet_data = None

    def __init__(self, keyfile: Optional[Path] = None):
        self.keyfile = keyfile or (ROOTDIR / google_sa_creds) if google_sa_creds else ROOTDIR / "ggsheet_key.json"
        self.client = self._init_client()

    def _init_client(self):
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(str(self.keyfile), scopes=scopes)
        # client = authorize(creds)
        client = gspread.authorize(creds)
        return client

    @staticmethod
    def _retry(func, *args, **kwargs):
        retries = 5
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except (requests.exceptions.RequestException, socket.gaierror) as e:
                wait = retries ** attempt
                logger.debug(f"- Retry request in {wait}s....")
                time.sleep(wait)

        raise Exception("Max retries exceeded")

    def _load_sheets(self, sheet_url: str):
        """Load all sheets in a spreadsheet by URL."""
        if not self._sheet_data:

            for attempt in range(5):

                logger.debug(f"- Loading sheet data from url (attempt:{attempt + 1})")
                try:
                    self._sheet_data = self.client.open_by_url(sheet_url).worksheets()
                    return self._sheet_data

                except Exception as e:

                    logger.debug(f"- Request exception: {e}, retrying...")
                    wait = 2 ** attempt
                    time.sleep(wait)

            raise Exception("Max retries attempts! Failed to load sheet data")

        return self._sheet_data

    def _get_sheet_data(self, sheet_url: str, clients: List[str]):
        """Get raw sheet data filtered by client names."""
        client_list = [c.strip().lower() for c in clients]
        sheets = self._load_sheets(sheet_url)
        values = {}
        for sheet in sheets:
            if sheet.title.lower() in client_list:
                values[sheet.title.lower()] = sheet.get_all_values()
        return values

    @staticmethod
    def _parse_accounts(sheet_data: Dict, clients: List[str], account_type: str) -> List[Dict]:
        """
        Parse the sheet data and directly return a flattened list of accounts
        filtered by account_type.
        """

        result = []

        for client in clients:
            data = sheet_data.get(client.lower(), None)
            if not data:
                continue

            # Extract client_url from the first row (index 1 if it exists, otherwise empty string)
            client_url = ""
            if len(data) > 0 and len(data[0]) > 1:
                client_url = data[0][1] if data[0][1] else ""

            header_row = data[1]
            rows = data[2:]
            col_defs = []
            i = 0

            while i < len(header_row) - 1:
                label = header_row[i].strip().lower()
                if not label or header_row[i + 1].strip().lower() != "password":
                    i += 1
                    continue

                server_acc = label.split()
                if len(server_acc) == 2:
                    server, acc_type = server_acc
                    if acc_type == account_type:
                        col_defs.append((i, acc_type, server))
                i += 2

            for row in rows:
                for col_idx, acc_type, server in col_defs:
                    userid = row[col_idx] if col_idx < len(row) else ""
                    password = row[col_idx + 1] if col_idx + 1 < len(row) else ""
                    if userid and password:
                        result.append({
                            "client": client,
                            "client_url": client_url,
                            "account_type": acc_type,
                            "server": server,
                            "userid": userid,
                            "password": password,
                        })

        # Sort the result by client, then server, then userid for consistent ordering
        result.sort(key=lambda x: (x["client"], x["server"]))

        return result

    def get_accounts(
            self,
            sheet_url: str,
            clients: str | list,
            account_type: str = None,
            reverse=False
    ) -> List[Dict]:
        """
        One call to get a filtered, flattened list of accounts for clients & account_type.
        """
        clients = clients.split(",") if not isinstance(clients, list) else clients
        sheet_data = self._get_sheet_data(sheet_url, clients)
        accounts = self._parse_accounts(sheet_data, clients, account_type or "live")
        return accounts if not reverse else accounts[::-1]


"""
Handle test directories
"""


def collect_critical_folders(platform="web", module="", test_marker="critical"):
    platform = platform.replace("-", "_")
    test_root = ROOTDIR / "tests" / platform / module
    test_folders = set()

    for test_file in test_root.rglob("test_*.py"):
        test_folders.add(str(test_file.parent))

    pytest_path = which("pytest")
    if not pytest_path:
        raise RuntimeError("pytest not found in PATH")

    for folder in sorted(test_folders.copy()):
        logging.info(f"Running pytest in: {folder}")
        try:
            result = subprocess.run(
                [pytest_path, str(folder), "-m", test_marker, "--co"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )
            if "no tests collected" in result.stdout:
                test_folders.remove(folder)

        except subprocess.TimeoutExpired:
            logging.error(f"Timeout running pytest in {folder}")

        except Exception as e:
            logging.error(f"Error running pytest in {folder}: {e}")

    test_folders = sorted(test_folders)
    res = [{"directory": f"tests{folder.split('tests')[-1]}"} for folder in test_folders]

    return res


def assign_dirs_to_accounts(accounts: List[Dict], dirs: List[Dict]) -> List[Dict]:
    """
    Assign directories to accounts in round-robin fashion.
    Limits the number of accounts per client per server based on the number of directories available.
    """
    if not dirs:
        return accounts

    # Calculate how many accounts we need per client per server
    amount_per_client_server = len(dirs)

    # Track counts per client per server
    counts = defaultdict(lambda: defaultdict(int))
    limited_accounts = []

    for account in accounts:
        client = account["client"]
        server = account["server"]

        # Check limit per client per server
        if counts[client][server] < amount_per_client_server:
            limited_accounts.append(account)
            counts[client][server] += 1

    assigned = []
    for i, account in enumerate(limited_accounts):
        account_copy = account.copy()
        account_copy['directory'] = dirs[i % len(dirs)]['directory']
        assigned.append(account_copy)
    return assigned


def get_session_id():
    driver = getattr(builtins, "web_driver", None)
    if driver:
        session_id = driver.session_id
        with open("/tmp/session_id.txt", "w") as f:
            f.write(session_id)

        logger.debug(f"- session_id: {session_id!r}")
        return session_id
    return None
