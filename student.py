from database import fetch_all, fetch_one, execute_query


class Student:

    def __init__(self, username):
        self.username = username

    def get_student_id(self):

        student = fetch_one("""
            SELECT s.student_id
            FROM students s
            JOIN users u
            ON s.user_id = u.user_id
            WHERE LOWER(u.username) = LOWER(%s)
        """, (self.username,))

        if student:
            return student[0]

        return None

    # 1. View Exams
    def view_exams(self):

        exams = fetch_all("""
            SELECT
                e.exam_id,
                e.exam_name,
                s.subject_name
            FROM exams e
            JOIN subjects s
            ON e.subject_id = s.subject_id
            ORDER BY e.exam_id
        """)

        if not exams:
            print("\nNo exams available")
            return

        print("\n===== AVAILABLE EXAMS =====")

        for exam in exams:

            question_count = fetch_one("""
                SELECT COUNT(*)
                FROM questions
                WHERE exam_id = %s
            """, (exam[0],))

            total_questions = question_count[0]

            print("Exam ID       :", exam[0])
            print("Exam Name     :", exam[1])
            print("Subject       :", exam[2])
            print("Questions     :", total_questions)
            print("Total Marks   :", total_questions)
            print("---------------------------")

    # 2. Attend Exam
    def attend_exam(self):

        try:
            exam_id = int(input("\nEnter Exam ID: "))

        except ValueError:
            print("Please enter a valid Exam ID")
            return

        exam = fetch_one("""
            SELECT
                e.exam_id,
                e.exam_name,
                s.subject_name
            FROM exams e
            JOIN subjects s
            ON e.subject_id = s.subject_id
            WHERE e.exam_id = %s
        """, (exam_id,))

        if not exam:
            print("Invalid Exam ID")
            return

        exam_questions = fetch_all("""
            SELECT
                question_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer
            FROM questions
            WHERE exam_id = %s
            ORDER BY question_id
        """, (exam_id,))

        if not exam_questions:
            print("No questions available for this exam")
            return

        print("\n===== EXAM STARTED =====")
        print("Exam ID       :", exam[0])
        print("Exam Name     :", exam[1])
        print("Subject       :", exam[2])
        print("Questions     :", len(exam_questions))
        print("Total Marks   :", len(exam_questions))
        print("---------------------------")

        answers = {}

        for i, q in enumerate(exam_questions, 1):

            print("\nQuestion", i, ":", q[1])

            print("A.", q[2])
            print("B.", q[3])
            print("C.", q[4])
            print("D.", q[5])

            while True:

                answer = input(
                    "Enter your answer (A/B/C/D): "
                ).upper()

                if answer in ["A", "B", "C", "D"]:

                    answers[q[0]] = answer
                    break

                print("Please enter A, B, C or D")

        print("\n===== EXAM COMPLETED =====")

        score = 0
        total_marks = len(exam_questions)

        for q in exam_questions:

            if answers.get(q[0]) == q[6]:
                score += 1

        percentage = 0

        if total_marks > 0:
            percentage = (score / total_marks) * 100

        print("\n===== RESULT =====")
        print("Score       :", score, "/", total_marks)
        print("Percentage  :", round(percentage, 2), "%")

        self.save_result(
            exam_id,
            score
        )

    # 3. View Latest Result
    def view_results(self):

        student_id = self.get_student_id()

        if not student_id:

            print("\nStudent record not found")
            return

        result = fetch_one("""
            SELECT
                r.exam_id,
                e.exam_name,
                r.score,
                r.exam_date
            FROM results r
            JOIN exams e
            ON r.exam_id = e.exam_id
            WHERE r.student_id = %s
            ORDER BY r.result_id DESC
            LIMIT 1
        """, (student_id,))

        if not result:

            print("\nNo results available")
            return

        total_result = fetch_one("""
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
        """, (result[0],))

        total_marks = total_result[0]

        percentage = 0

        if total_marks > 0:
            percentage = (result[2] / total_marks) * 100

        print("\n===== LATEST RESULT =====")

        print("Exam ID      :", result[0])
        print("Exam Name    :", result[1])
        print("Score        :", result[2], "/", total_marks)
        print("Percentage   :", round(percentage, 2), "%")
        print("Exam Date    :", result[3])

        print("------------------------")

    # 4. Exam History
    def exam_history(self):

        student_id = self.get_student_id()

        if not student_id:

            print("\nStudent record not found")
            return

        results = fetch_all("""
            SELECT
                r.result_id,
                r.exam_id,
                e.exam_name,
                r.score,
                r.exam_date
            FROM results r
            JOIN exams e
            ON r.exam_id = e.exam_id
            WHERE r.student_id = %s
            ORDER BY r.result_id
        """, (student_id,))

        if not results:

            print("\nNo exam history available")
            return

        print("\n===== EXAM HISTORY =====")

        for i, result in enumerate(results, 1):

            total_result = fetch_one("""
                SELECT COUNT(*)
                FROM questions
                WHERE exam_id = %s
            """, (result[1],))

            total_marks = total_result[0]

            percentage = 0

            if total_marks > 0:
                percentage = (result[3] / total_marks) * 100

            print("Attempt      :", i)
            print("Exam ID      :", result[1])
            print("Exam Name    :", result[2])
            print("Score        :", result[3], "/", total_marks)
            print("Percentage   :", round(percentage, 2), "%")
            print("Exam Date    :", result[4])

            print("------------------------")

    # Save Result
    def save_result(self, exam_id, score):

        student_id = self.get_student_id()

        if not student_id:

            print("\nStudent record not found")
            return

        execute_query("""
            INSERT INTO results
            (
                student_id,
                exam_id,
                score
            )
            VALUES (%s, %s, %s)
        """, (
            student_id,
            exam_id,
            score
        ))

        print("\nResult saved successfully!")


# ==================================
# STUDENT MENU
# ==================================

def student_menu(user):

    username = user.get(
        "username",
        user.get("name", "Student")
    )

    student = Student(username)

    while True:

        print("\n===== STUDENT MENU =====")
        print("1. View Exams")
        print("2. Attend Exam")
        print("3. View Results")
        print("4. Exam History")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

            student.view_exams()

        elif choice == "2":

            student.attend_exam()

        elif choice == "3":

            student.view_results()

        elif choice == "4":

            student.exam_history()

        elif choice == "5":

            print("\nLogged out successfully!")
            break

        else:

            print("\nInvalid choice")

