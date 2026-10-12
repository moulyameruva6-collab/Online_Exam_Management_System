
from database import get_connection

try:
    connection = get_connection()

    if connection.is_connected():
        print("Python connected to MySQL successfully!")
        print("Database:", connection.database)

    connection.close()

except Exception as e:
    print("Connection failed!")
    print("Error:", e)
