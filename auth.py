from database import load_data, save_data


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

    for user in users:
        if user["username"].lower() == username.lower():
            print("Username already exists!")
            return

    user = {
        "name": name,
        "username": username,
        "password": password,
        "role": role
    }

    users.append(user)
    save_data("data/users.json", users)

    if role == "student":

        students = load_data("data/students.json")
        students.append(user)
        save_data("data/students.json", students)

    else:

        teachers = load_data("data/teachers.json")

        teacher = {
            "name": name,
            "username": username,
            "password": password,
            "role": role,
            "subject": ""
        }

        teachers.append(teacher)
        save_data("data/teachers.json", teachers)

    print("Registration successful!")


def login():

    print("\n--- Login ---")

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    # Admin login
    if username.lower() == "admin" and password == "admin123":
        print("Admin login successful!")

        return {
            "name": "Admin",
            "username": "admin",
            "role": "admin"
        }

    users = load_data("data/users.json")

    for user in users:

        if (user["username"].lower() == username.lower()
                and user["password"] == password):

            if user["role"] == "teacher":

                teachers = load_data("data/teachers.json")

                for teacher in teachers:

                    if teacher["username"].lower() == username.lower():
                        user["subject"] = teacher.get("subject", "")
                        break

            print("Login successful!")
            return user

    print("Invalid username or password")
    return None