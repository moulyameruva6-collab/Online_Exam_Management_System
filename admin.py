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

    if not students:
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

    if not teachers:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for teacher in teachers:
        print("Name:", teacher["name"])
        print("Username:", teacher["username"])
        print("Subject:", teacher.get("subject", ""))
        print()


# ==================================
# VIEW EXAMS
# ==================================

def view_exams():

    exams = load_data("data/exams.json")

    if not exams:
        print("\nNo exams available")
        return

    print("\n--- Exams ---")

    for exam in exams:

        print("Exam:", exam["exam_name"])
        print("Exam ID:", exam["exam_id"])
        print("Subject:", exam.get("subject", ""))
        print("Teacher:", exam.get("teacher", ""))
        print("Duration:", exam.get("duration", 0), "minutes")
        print()


# ==================================
# VIEW RESULTS
# ==================================

def view_results():

    results = load_data("data/results.json")

    if not results:
        print("\nNo results available")
        return

    print("\n--- Results ---")

    for result in results:
        print("Student:", result.get("username", result.get("student", "Unknown")))
        print("Exam ID:", result.get("exam_id", ""))
        print("Score:", result.get("score", 0), "/", result.get("total_marks", 0))
        print("Percentage:", result.get("percentage", 0), "%")
        print()

# ==================================
# ASSIGN SUBJECT
# ==================================

def assign_subject():

    teachers = load_data("data/teachers.json")

    if not teachers:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for i, teacher in enumerate(teachers, 1):
        print(i, teacher["name"], "-", teacher.get("subject", ""))

    try:
        number = int(input("Enter teacher number: "))
        teacher = teachers[number - 1]
    except (ValueError, IndexError):
        print("Invalid teacher number")
        return

    subject = input("Enter subject: ").strip()

    if not subject:
        print("Subject cannot be empty")
        return

    teacher["subject"] = subject

    save_data("data/teachers.json", teachers)

    # Update subject in users.json also
    users = load_data("data/users.json")

    for user in users:

        if user["username"].lower() == teacher["username"].lower():
            user["subject"] = subject
            break

    save_data("data/users.json", users)

    print("Subject assigned successfully!")