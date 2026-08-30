from database import load_data, save_data


def admin_menu():
    while True:

        print("\n====================")
        print("      ADMIN MENU")
        print("====================")
        print("1. View Students")
        print("2. View Teachers")
        print("3. View Exams")
        print("4. View Results")
        print("5. Assign Subject")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_students()

        elif choice == "2":
            view_teachers()

        elif choice == "3":
            view_exams()

        elif choice == "4":
            view_results()

        elif choice == "5":
            assign_subject()

        elif choice == "6":
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice")


# ==================================
# VIEW STUDENTS
# ==================================

def view_students():

    students = load_data("data/students.json")

    if len(students) == 0:
        print("\nNo students available")
        return

    print("\n--- Students ---")

    for student in students:

        print("Name:", student["name"])
        print("Username:", student["username"])
        print()


# ==================================
# VIEW TEACHERS
# ==================================

def view_teachers():

    teachers = load_data("data/teachers.json")

    if len(teachers) == 0:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for teacher in teachers:

        print("Name:", teacher["name"])
        print("Username:", teacher["username"])

        if "subject" in teacher:
            print("Subject:", teacher["subject"])
        else:
            print("Subject: Not Assigned")

        print()


# ==================================
# VIEW EXAMS
# ==================================

def view_exams():

    exams = load_data("data/exams.json")

    if len(exams) == 0:
        print("\nNo exams available")
        return

    print("\n--- Exams ---")

    for exam in exams:

        print("Exam:", exam["exam_name"])
        print("Subject:", exam["subject"])
        print("Teacher:", exam["teacher"])

        if "duration" in exam:
            print("Duration:", exam["duration"], "minutes")

        print()


# ==================================
# VIEW RESULTS
# ==================================

def view_results():

    results = load_data("data/results.json")

    if len(results) == 0:
        print("\nNo results available")
        return

    print("\n--- Results ---")

    for result in results:

        print("Student:", result["student"])
        print("Exam:", result["exam"])
        print("Score:", result["score"], "/", result["total"])
        print("Percentage:", result["percentage"], "%")
        print("Result:", result["result"])
        print()


# ==================================
# ASSIGN SUBJECT
# ==================================

def assign_subject():

    teachers = load_data("data/teachers.json")
    users = load_data("data/users.json")

    if len(teachers) == 0:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for i, teacher in enumerate(teachers):

        subject = teacher.get("subject", "Not Assigned")

        print(
            i + 1,
            teacher["name"],
            "-",
            subject
        )

    # Teacher number validation
    try:
        number = int(input("Enter teacher number: "))

    except ValueError:
        print("Please enter a number")
        return

    if number < 1 or number > len(teachers):
        print("Invalid teacher number")
        return

    subject = input("Enter subject: ").strip()

    if subject == "":
        print("Subject cannot be empty")
        return

    selected_teacher = teachers[number - 1]

    # ==================================
    # UPDATE teachers.json
    # ==================================

    selected_teacher["subject"] = subject

    save_data(
        "data/teachers.json",
        teachers
    )

    # ==================================
    # UPDATE users.json
    # ==================================

    for user in users:

        if user["username"] == selected_teacher["username"]:

            user["subject"] = subject

            break

    save_data(
        "data/users.json",
        users
    )

    print("Subject assigned successfully!")