"""Project settings, environment variable, and constants manager"""

import os

from dotenv import load_dotenv

load_dotenv()

DB_CONN_STRING = os.getenv("DB_CONN_STRING", "")
MAIN_PAGE_URL = "https://rimworldwiki.com/"
SEARCH_PAGE_URL = "https://rimworldwiki.com/index.php"

DEEP_INFRA_API_KEY=os.getenv("DEEP_INFRA_API_KEY", "")
if DEEP_INFRA_API_KEY == "":
    raise Exception("DEEP_INFRA_API_KEY is not set!")