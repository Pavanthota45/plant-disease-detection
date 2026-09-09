import os

import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",      # ⚠️ DO NOT USE localhost
            user="root",
            password=os.environ["MYSQL_PASSWORD"],
            database="plantdisease",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        print("DATABASE CONNECTED")
        return conn

    except Exception as e:
        print("DATABASE CONNECTION FAILED:", e)
        return None