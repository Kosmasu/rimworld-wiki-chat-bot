from src.db import init_db


def main():
    conn = init_db()
    conn.cursor()


if __name__ == "__main__":
    main()
    print("done")
