from dotenv import load_dotenv
import psycopg

from src.settings import DB_CONN_STRING

load_dotenv()

conn = None

def get_conn() -> psycopg.Connection:
    return psycopg.connect(DB_CONN_STRING)


def init_db():
    global conn
    if conn:
        return conn
    
    conn = get_conn()
    assert conn
    
    # migration (dumb version)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                link TEXT NOT NULL,
                scraped_at TIMESTAMP NULL DEFAULT NULL,
                content TEXT
            );
            """)
    conn.commit()
    return conn
