import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="online_exam"
    )


def execute_query(query, values=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, values or ())
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def fetch_one(query, values=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, values or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()


def fetch_all(query, values=None):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, values or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()