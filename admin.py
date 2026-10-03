from database import fetch_all, fetch_one, execute_query


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

    query = """
        SELECT
            s.student_name,
            u.username
        FROM students s
        JOIN users u
        ON s.user_id = u.user_id
    """

    students = fetch_all(query)

    if not students:
        print("\nNo students available")
        return

    print("\n--- Students ---")

    for student in students:
        print("Name:", student[0])
        print("Username:", student[1])
        print()


# ==================================
# VIEW TEACHERS
# ==================================

def view_teachers():

    query = """
        SELECT
            t.teacher_id,
            t.teacher_name,
            u.username
        FROM teachers t
        JOIN users u
        ON t.user_id = u.user_id
    """

    teachers = fetch_all(query)

    if not teachers:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for teacher in teachers:

        teacher_id = teacher[0]
        teacher_name = teacher[1]
        username = teacher[2]

        print("Teacher ID:", teacher_id)
        print("Name:", teacher_name)
        print("Username:", username)

        # Get assigned subjects
        subjects = fetch_all(
            """
            SELECT subject_name
            FROM subjects
            WHERE teacher_id = %s
            """,
            (teacher_id,)
        )

        if subjects:
            print("Subjects:")

            for subject in subjects:
                print(" -", subject[0])
        else:
            print("Subjects: Not assigned")

        print()


# ==================================
# VIEW EXAMS
# ==================================

def view_exams():

    query = """
        SELECT
            e.exam_id,
            e.exam_name,
            s.subject_name,
            t.teacher_name
        FROM exams e
        JOIN subjects s
        ON e.subject_id = s.subject_id
        JOIN teachers t
        ON e.teacher_id = t.teacher_id
    """

    exams = fetch_all(query)

    if not exams:
        print("\nNo exams available")
        return

    print("\n--- Exams ---")

    for exam in exams:

        exam_id = exam[0]
        exam_name = exam[1]
        subject_name = exam[2]
        teacher_name = exam[3]

        # Count questions
        question_count = fetch_one(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
            """,
            (exam_id,)
        )

        total_questions = question_count[0]

        print("Exam ID:", exam_id)
        print("Exam Name:", exam_name)
        print("Subject:", subject_name)
        print("Teacher:", teacher_name)
        print("Questions:", total_questions)
        print("Total Marks:", total_questions)
        print()


# ==================================
# VIEW RESULTS
# ==================================

def view_results():

    query = """
        SELECT
            u.username,
            s.student_name,
            r.exam_id,
            e.exam_name,
            r.score,
            r.exam_date
        FROM results r
        JOIN students s
        ON r.student_id = s.student_id
        JOIN users u
        ON s.user_id = u.user_id
        JOIN exams e
        ON r.exam_id = e.exam_id
        ORDER BY r.exam_date DESC
    """

    results = fetch_all(query)

    if not results:
        print("\nNo results available")
        return

    print("\n--- Results ---")

    for result in results:

        username = result[0]
        student_name = result[1]
        exam_id = result[2]
        exam_name = result[3]
        score = result[4]
        exam_date = result[5]

        # Calculate total marks
        total = fetch_one(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
            """,
            (exam_id,)
        )

        total_marks = total[0]

        # Calculate percentage
        percentage = 0

        if total_marks > 0:
            percentage = (score / total_marks) * 100

        print("Student:", student_name)
        print("Username:", username)
        print("Exam ID:", exam_id)
        print("Exam Name:", exam_name)
        print("Score:", score, "/", total_marks)
        print("Percentage:", round(percentage, 2), "%")
        print("Exam Date:", exam_date)
        print()


# ==================================
# ASSIGN SUBJECT
# ==================================

def assign_subject():

    # Get teachers
    query = """
        SELECT
            t.teacher_id,
            t.teacher_name,
            u.username
        FROM teachers t
        JOIN users u
        ON t.user_id = u.user_id
    """

    teachers = fetch_all(query)

    if not teachers:
        print("\nNo teachers available")
        return

    print("\n--- Teachers ---")

    for i, teacher in enumerate(teachers, 1):

        print(
            i,
            teacher[1],
            "-",
            teacher[2]
        )

    try:
        number = int(input("Enter teacher number: "))

        if number < 1 or number > len(teachers):
            print("Invalid teacher number")
            return

        teacher = teachers[number - 1]

    except ValueError:
        print("Please enter a number")
        return

    teacher_id = teacher[0]

    subject_name = input("Enter subject: ").strip()

    if not subject_name:
        print("Subject cannot be empty")
        return

    # Check if subject already exists
    existing_subject = fetch_one(
        """
        SELECT subject_id
        FROM subjects
        WHERE LOWER(subject_name) = LOWER(%s)
        """,
        (subject_name,)
    )

    if existing_subject:

        subject_id = existing_subject[0]

        # Assign existing subject to teacher
        execute_query(
            """
            UPDATE subjects
            SET teacher_id = %s
            WHERE subject_id = %s
            """,
            (teacher_id, subject_id)
        )

    else:

        # Create new subject
        execute_query(
            """
            INSERT INTO subjects
            (subject_name, teacher_id)
            VALUES (%s, %s)
            """,
            (subject_name, teacher_id)
        )

    print("Subject assigned successfully!")



