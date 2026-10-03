from database import fetch_all, fetch_one, execute_query
from question import (
    add_question,
    view_questions,
    delete_question,
    update_question,
    search_question,
    question_count
)


def teacher_menu(user):

    while True:

        print("\n====================")
        print("    TEACHER MENU")
        print("====================")
        print("1. Add Exam")
        print("2. View Exams")
        print("3. Add Question")
        print("4. View Questions")
        print("5. Delete Question")
        print("6. Update Question")
        print("7. Delete Exam")
        print("8. View Exam Results")
        print("9. Update Exam")
        print("10. View Exam Questions")
        print("11. Question Count")
        print("12. Search Question")
        print("13. Student Performance")
        print("14. Set Passing Percentage")
        print("15. Exam Status")
        print("16. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_exam(user)

        elif choice == "2":
            view_exams(user)

        elif choice == "3":
            add_question()

        elif choice == "4":
            view_questions()

        elif choice == "5":
            delete_question()

        elif choice == "6":
            update_question()

        elif choice == "7":
            delete_exam(user)

        elif choice == "8":
            view_results(user)

        elif choice == "9":
            update_exam(user)

        elif choice == "10":
            view_exam_questions(user)

        elif choice == "11":
            question_count()

        elif choice == "12":
            search_question()

        elif choice == "13":
            student_performance(user)

        elif choice == "14":
            passing_percentage()

        elif choice == "15":
            exam_status()

        elif choice == "16":
            print("Logged out successfully!")
            break

        else:
            print("Invalid choice")


# ==================================
# GET TEACHER ID
# ==================================

def get_teacher_id(user):

    if "teacher_id" in user:
        return user["teacher_id"]

    query = """
        SELECT teacher_id
        FROM teachers
        WHERE user_id = %s
    """

    teacher = fetch_one(
        query,
        (user["user_id"],)
    )

    if teacher:
        return teacher[0]

    return None


# ==================================
# MY EXAMS
# ==================================

def my_exams(user):

    teacher_id = get_teacher_id(user)

    if not teacher_id:
        return []

    query = """
        SELECT
            e.exam_id,
            e.exam_name,
            s.subject_name
        FROM exams e
        JOIN subjects s
        ON e.subject_id = s.subject_id
        WHERE e.teacher_id = %s
        ORDER BY e.exam_id
    """

    return fetch_all(
        query,
        (teacher_id,)
    )


# ==================================
# ADD EXAM
# ==================================

def add_exam(user):

    teacher_id = get_teacher_id(user)

    if not teacher_id:
        print("Teacher not found")
        return

    # Get assigned subjects
    subjects = fetch_all(
        """
        SELECT
            subject_id,
            subject_name
        FROM subjects
        WHERE teacher_id = %s
        """,
        (teacher_id,)
    )

    if not subjects:
        print("No subject assigned")
        return

    print("\n--- Assigned Subjects ---")

    for i, subject in enumerate(subjects, 1):
        print(i, "-", subject[1])

    try:
        number = int(
            input("Enter subject number: ")
        )

        if number < 1 or number > len(subjects):
            print("Invalid subject number")
            return

        subject_id = subjects[number - 1][0]
        subject_name = subjects[number - 1][1]

    except ValueError:
        print("Please enter a number")
        return

    exam_name = input(
        "Enter exam name: "
    ).strip()

    if not exam_name:
        print("Exam name cannot be empty")
        return

    # Check duplicate exam
    existing_exam = fetch_one(
        """
        SELECT exam_id
        FROM exams
        WHERE LOWER(exam_name) = LOWER(%s)
        AND teacher_id = %s
        """,
        (exam_name, teacher_id)
    )

    if existing_exam:
        print("Exam already exists!")
        return

    # Insert exam
    query = """
        INSERT INTO exams
        (
            exam_name,
            subject_id,
            teacher_id
        )
        VALUES (%s, %s, %s)
    """

    execute_query(
        query,
        (
            exam_name,
            subject_id,
            teacher_id
        )
    )

    print("Exam added successfully!")
    print("Subject:", subject_name)


# ==================================
# VIEW EXAMS
# ==================================

def view_exams(user):

    exams = my_exams(user)

    print("\n--- My Exams ---")

    if not exams:
        print("No exams available")
        return

    for exam in exams:

        question_result = fetch_one(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
            """,
            (exam[0],)
        )

        total_questions = question_result[0]

        print("\nExam:", exam[1])
        print("ID:", exam[0])
        print("Subject:", exam[2])
        print("Questions:", total_questions)
        print("Total Marks:", total_questions)


# ==================================
# DELETE EXAM
# ==================================

def delete_exam(user):

    exams = my_exams(user)

    if not exams:
        print("No exams available")
        return

    print("\n--- My Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        number = int(
            input("Enter exam number to delete: ")
        )

        if number < 1 or number > len(exams):
            print("Invalid exam number")
            return

        exam = exams[number - 1]

    except ValueError:
        print("Please enter a number")
        return

    confirm = input(
        "Are you sure? (yes/no): "
    ).lower()

    if confirm != "yes":
        print("Delete cancelled")
        return

    exam_id = exam[0]

    # Delete results
    execute_query(
        """
        DELETE FROM results
        WHERE exam_id = %s
        """,
        (exam_id,)
    )

    # Delete questions
    execute_query(
        """
        DELETE FROM questions
        WHERE exam_id = %s
        """,
        (exam_id,)
    )

    # Delete exam
    execute_query(
        """
        DELETE FROM exams
        WHERE exam_id = %s
        """,
        (exam_id,)
    )

    print("Exam deleted successfully!")


# ==================================
# VIEW RESULTS
# ==================================

def view_results(user):

    exams = my_exams(user)

    if not exams:
        print("No exams available")
        return

    print("\n--- Exam Results ---")

    found = False

    for exam in exams:

        results = fetch_all(
            """
            SELECT
                u.username,
                s.student_name,
                r.score,
                r.exam_date
            FROM results r
            JOIN students s
            ON r.student_id = s.student_id
            JOIN users u
            ON s.user_id = u.user_id
            WHERE r.exam_id = %s
            ORDER BY r.exam_date DESC
            """,
            (exam[0],)
        )

        total_result = fetch_one(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
            """,
            (exam[0],)
        )

        total_marks = total_result[0]

        for result in results:

            username = result[0]
            student_name = result[1]
            score = result[2]
            exam_date = result[3]

            percentage = 0

            if total_marks > 0:
                percentage = (
                    score / total_marks
                ) * 100

            print("\nStudent:", student_name)
            print("Username:", username)
            print("Exam:", exam[1])
            print(
                "Score:",
                score,
                "/",
                total_marks
            )
            print(
                "Percentage:",
                round(percentage, 2),
                "%"
            )
            print("Date:", exam_date)

            found = True

    if not found:
        print(
            "No students have taken "
            "your exams yet."
        )


# ==================================
# UPDATE EXAM
# ==================================

def update_exam(user):

    exams = my_exams(user)

    if not exams:
        print("No exams available")
        return

    print("\n--- My Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        number = int(
            input("Enter exam number: ")
        )

        if number < 1 or number > len(exams):
            print("Invalid exam number")
            return

        exam = exams[number - 1]

    except ValueError:
        print("Please enter a number")
        return

    new_name = input(
        "Enter new exam name: "
    ).strip()

    if not new_name:
        print("Exam name cannot be empty")
        return

    query = """
        UPDATE exams
        SET exam_name = %s
        WHERE exam_id = %s
        AND teacher_id = %s
    """

    execute_query(
        query,
        (
            new_name,
            exam[0],
            get_teacher_id(user)
        )
    )

    print("Exam updated successfully!")


# ==================================
# VIEW EXAM QUESTIONS
# ==================================

def view_exam_questions(user):

    exams = my_exams(user)

    if not exams:
        print("No exams available")
        return

    print("\n--- My Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        number = int(
            input("Enter exam number: ")
        )

        if number < 1 or number > len(exams):
            print("Invalid exam number")
            return

        exam_id = exams[number - 1][0]

    except ValueError:
        print("Please enter a number")
        return

    questions = fetch_all(
        """
        SELECT
            question_text,
            option_a,
            option_b,
            option_c,
            option_d
        FROM questions
        WHERE exam_id = %s
        ORDER BY question_id
        """,
        (exam_id,)
    )

    print("\n--- Exam Questions ---")

    if not questions:
        print("No questions available")
        return

    for i, question in enumerate(
        questions, 1
    ):

        print(
            "\nQuestion",
            i,
            ":",
            question[0]
        )
        print("A.", question[1])
        print("B.", question[2])
        print("C.", question[3])
        print("D.", question[4])


# ==================================
# STUDENT PERFORMANCE
# ==================================

def student_performance(user):

    exams = my_exams(user)

    if not exams:
        print("No exams available")
        return

    print("\n--- Student Performance ---")

    found = False

    for exam in exams:

        total_result = fetch_one(
            """
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
            """,
            (exam[0],)
        )

        total_marks = total_result[0]

        results = fetch_all(
            """
            SELECT
                s.student_name,
                u.username,
                r.score,
                r.exam_date
            FROM results r
            JOIN students s
            ON r.student_id = s.student_id
            JOIN users u
            ON s.user_id = u.user_id
            WHERE r.exam_id = %s
            """,
            (exam[0],)
        )

        for result in results:

            student_name = result[0]
            username = result[1]
            score = result[2]

            percentage = 0

            if total_marks > 0:
                percentage = (
                    score / total_marks
                ) * 100

            print("\nStudent:", student_name)
            print("Username:", username)
            print("Exam:", exam[1])
            print(
                "Score:",
                score,
                "/",
                total_marks
            )
            print(
                "Percentage:",
                round(percentage, 2),
                "%"
            )

            found = True

    if not found:
        print(
            "No student performance available"
        )


# ==================================
# PASSING PERCENTAGE
# ==================================

def passing_percentage():

    print(
        "\nPassing percentage cannot be stored."
    )

    print(
        "The current exams table does not "
        "contain a passing_percentage column."
    )

    print(
        "Percentage is calculated from "
        "score and question count."
    )


# ==================================
# EXAM STATUS
# ==================================

def exam_status():

    print(
        "\nExam status cannot be stored."
    )

    print(
        "The current exams table does not "
        "contain a status column."
    )

    print(
        "All created exams are available "
        "to students."
    )

