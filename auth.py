from database import execute_query, fetch_one


def register():

    print("\n--- Registration ---")

    name = input("Enter name: ").strip()
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (student/teacher): ").strip().lower()

    if role not in ["student", "teacher"]:
        print("Invalid role")
        return

    # Check username
    query = """
        SELECT user_id
        FROM users
        WHERE LOWER(username) = LOWER(%s)
    """

    existing_user = fetch_one(query, (username,))

    if existing_user:
        print("Username already exists!")
        return

    # Insert user
    query = """
        INSERT INTO users
        (username, password, role)
        VALUES (%s, %s, %s)
    """

    execute_query(
        query,
        (username, password, role)
    )

    # Get newly created user
    user = fetch_one(
        """
        SELECT user_id
        FROM users
        WHERE LOWER(username) = LOWER(%s)
        """,
        (username,)
    )

    user_id = user[0]

    # Add student
    if role == "student":

        query = """
            INSERT INTO students
            (user_id, student_name)
            VALUES (%s, %s)
        """

        execute_query(
            query,
            (user_id, name)
        )

    # Add teacher
    else:

        query = """
            INSERT INTO teachers
            (user_id, teacher_name)
            VALUES (%s, %s)
        """

        execute_query(
            query,
            (user_id, name)
        )

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

    # Check user
    query = """
        SELECT
            user_id,
            username,
            password,
            role
        FROM users
        WHERE LOWER(username) = LOWER(%s)
    """

    user = fetch_one(query, (username,))

    if not user:
        print("Invalid username or password")
        return None

    if user[2] != password:
        print("Invalid username or password")
        return None

    user_id = user[0]
    username = user[1]
    role = user[3]

    # Student login
    if role == "student":

        student = fetch_one(
            """
            SELECT student_name
            FROM students
            WHERE user_id = %s
            """,
            (user_id,)
        )

        name = student[0] if student else username

        print("Login successful!")

        return {
            "user_id": user_id,
            "name": name,
            "username": username,
            "role": "student"
        }

    # Teacher login
    if role == "teacher":

        teacher = fetch_one(
            """
            SELECT
                teacher_id,
                teacher_name
            FROM teachers
            WHERE user_id = %s
            """,
            (user_id,)
        )

        if not teacher:
            print("Teacher record not found")
            return None

        teacher_id = teacher[0]
        name = teacher[1]

        # Get teacher subject
        subject = fetch_one(
            """
            SELECT subject_name
            FROM subjects
            WHERE teacher_id = %s
            """,
            (teacher_id,)
        )

        subject_name = subject[0] if subject else ""

        print("Login successful!")

        return {
            "user_id": user_id,
            "teacher_id": teacher_id,
            "name": name,
            "username": username,
            "role": "teacher",
            "subject": subject_name
        }

    print("Invalid role")
    return None
