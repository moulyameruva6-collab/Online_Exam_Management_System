from database import load_data, save_data


# ==================================
# REGISTER
# ==================================

def register():

    print("\n--- Registration ---")

    name = input("Enter name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (student/teacher): ").strip().lower()

    if role not in ["student", "teacher"]:
        print("Invalid role")
        return

    users = load_data("data/users.json")

    # Check username already exists
    for user in users:

        if user["username"].strip().lower() == username.lower():
            print("Username already exists!")
            return

    # Create user
    user = {
        "name": name,
        "username": username,
        "password": password,
        "role": role
    }

    # Save login details
    users.append(user)

    save_data(
        "data/users.json",
        users
    )

    # ==================================
    # SAVE STUDENT
    # ==================================

    if role == "student":

        students = load_data("data/students.json")

        students.append(user)

        save_data(
            "data/students.json",
            students
        )

    # ==================================
    # SAVE TEACHER
    # ==================================

    elif role == "teacher":

        teachers = load_data("data/teachers.json")

        teacher = {
            "name": name,
            "username": username,
            "password": password,
            "role": role,
            "subject": ""
        }

        teachers.append(teacher)

        save_data(
            "data/teachers.json",
            teachers
        )

    print("Registration successful!")


# ==================================
# LOGIN
# ==================================

def login():

    print("\n--- Login ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    # ==================================
    # ADMIN LOGIN
    # ==================================

    if username.lower() == "admin" and password == "admin123":

        print("Admin login successful!")

        return {
            "name": "Admin",
            "username": "admin",
            "role": "admin"
        }

    # ==================================
    # USER LOGIN
    # ==================================

    users = load_data("data/users.json")

    for user in users:

        if (
            user["username"].strip().lower()
            == username.strip().lower()
            and user["password"] == password
        ):

            # ==================================
            # TEACHER LOGIN
            # ==================================

            if user["role"].strip().lower() == "teacher":

                teachers = load_data(
                    "data/teachers.json"
                )

                user["subject"] = ""

                for teacher in teachers:

                    if (
                        teacher["username"].strip().lower()
                        == user["username"].strip().lower()
                    ):

                        user["subject"] = teacher.get(
                            "subject",
                            ""
                        ).strip()

                        break

            print("Login successful!")

            return user

    print("Invalid username or password")

    return None