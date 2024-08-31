"""Project settings, environment variable, and constants manager"""

import os


DB_CONN_STRING = os.getenv("DB_CONN_STRING", "")
MAIN_PAGE_URL = "https://rimworldwiki.com/"
SEARCH_PAGE_URL = "https://rimworldwiki.com/index.php"