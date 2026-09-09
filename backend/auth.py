import bcrypt
from backend.db import get_connection


# ---------------- REGISTER ----------------
def register_user(username, email, password):
    try:
        conn = get_connection()
        if conn is None:
            print("NO DB CONNECTION")
            return

        cursor = conn.cursor()

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO users(username,email,password) VALUES(%s,%s,%s)",
            (username, email, hashed.decode('utf-8'))
        )

        conn.commit()
        print("USER STORED IN DATABASE")

        cursor.close()
        conn.close()

    except Exception as e:
        print("REGISTER ERROR:", e)


# ---------------- LOGIN ----------------
def login_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM users WHERE username=%s",
            (username,)
        )

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            stored_password = result[0]
            return bcrypt.checkpw(password.encode('utf-8'),
                                  stored_password.encode('utf-8'))
        return False

    except Exception as e:
        print("LOGIN ERROR:", e)
        return False


# ---------------- RESET PASSWORD ----------------
def reset_password(username, new_password):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "UPDATE users SET password=%s WHERE username=%s",
            (hashed.decode('utf-8'), username)
        )

        conn.commit()

        cursor.close()
        conn.close()

        print("PASSWORD UPDATED")

    except Exception as e:
        print("RESET ERROR:", e)