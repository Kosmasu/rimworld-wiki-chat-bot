"""Project settings and environment variable manager"""

import os


DB_CONN_STRING = os.getenv("DB_CONN_STRING", "")