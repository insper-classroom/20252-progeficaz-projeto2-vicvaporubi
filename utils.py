import os

import pymysql


def get_connection():
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=int(os.environ.get("DB_CONNECT_TIMEOUT", 60)),
        cursorclass=pymysql.cursors.DictCursor,
        db=os.environ.get("DB_NAME"),
        host=os.environ.get("DB_HOST"),
        password=os.environ.get("DB_PASSWORD", ""),
        read_timeout=int(os.environ.get("DB_READ_TIMEOUT", 60)),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        write_timeout=int(os.environ.get("DB_WRITE_TIMEOUT", 60)),
        ssl={"ca": os.environ.get("DB_SSL_CERT_PATH")}
        if os.environ.get("DB_SSL_CERT_PATH")
        else None,
    )
    return connection


def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            with open("imoveis.sql", "r") as f:
                sql_script = f.read().split(";")
                for line in sql_script:
                    cursor.execute(line)
                    print("Executed: ", line)
        conn.commit()
