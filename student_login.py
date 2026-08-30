from utils.file_handler import load_data


def student_login():

    users = load_data("Data/users.json")

    print("\n===== STUDENT LOGIN =====")

    username = input("Enter Username: ")
    password = input("Enter Password: ")

    for user in users:

        if (
            user["username"] == username
            and user["password"] == password
            and user["role"] == "student"
        ):

            print("\nLogin Successful!")

            return username

    print("\nInvalid Username or Password.")

    return None