from database import load_data, save_data
import time


class Student:

    def __init__(self, username):
        self.username = username

    # 1. View Exams
    def view_exams(self):

        exams = load_data("data/exams.json")

        if not exams:
            print("\nNo exams available")
            return

        print("\n===== AVAILABLE EXAMS =====")

        for exam in exams:
            print("Exam ID     :", exam["exam_id"])
            print("Exam Name   :", exam["exam_name"])
            print("Duration    :", exam["duration"], "minutes")
            print("Total Marks :", exam["total_marks"])
            print("---------------------------")

    # 2. Attend Exam
    def attend_exam(self):

        exams = load_data("data/exams.json")
        questions = load_data("data/questions.json")

        exam_id = input("\nEnter Exam ID: ").upper()

        exam = None

        for e in exams:
            if e["exam_id"] == exam_id:
                exam = e
                break

        if not exam:
            print("Invalid Exam ID")
            return

        exam_questions = []

        for q in questions:
            if q["exam_id"] == exam_id:
                exam_questions.append(q)

        if not exam_questions:
            print("No questions available for this exam")
            return

        print("\n===== EXAM STARTED =====")
        print("Exam ID     :", exam["exam_id"])
        print("Questions   :", len(exam_questions))
        print("Total Marks :", exam["total_marks"])
        print("Duration    :", exam["duration"], "minutes")

        print("---------------------------")

        start_time = time.time()
        duration = exam["duration"] * 60

        answers = {}

        for i, q in enumerate(exam_questions, 1):

            elapsed = time.time() - start_time
            remaining = duration - elapsed

            if remaining <= 0:
                print("\n===== TIME UP =====")
                print("Exam time is over!")
                break

            minutes = int(remaining // 60)
            seconds = int(remaining % 60)

            print("\nTime Remaining:",
                  f"{minutes:02d}:{seconds:02d}")

            print("\nQuestion", i, ":", q["question"])

            for option, value in q["options"].items():
                print(option + ".", value)

            while True:

                answer = input(
                    "Enter your answer (A/B/C/D): "
                ).upper()

                if answer in ["A", "B", "C", "D"]:
                    answers[q["question_id"]] = answer
                    break

                print("Please enter A, B, C or D")

        print("\n===== EXAM COMPLETED =====")

        score = 0
        total_marks = 0

        for q in exam_questions:

            total_marks += q.get("marks", 1)

            if answers.get(q["question_id"]) == q["answer"]:
                score += q.get("marks", 1)

        percentage = 0

        if total_marks > 0:
            percentage = (score / total_marks) * 100

        print("\n===== RESULT =====")
        print("Score       :", score)
        print("Total Marks :", total_marks)
        print("Percentage  :", round(percentage, 2), "%")

        self.save_result(
            exam_id,
            score,
            total_marks,
            percentage
        )

    # 3. View Latest Result
    def view_results(self):

        results = load_data("data/results.json")

        student_results = []

        for result in results:
            if result.get("student") == self.username:
                student_results.append(result)

        if not student_results:
            print("\nNo results available")
            return

        result = student_results[-1]

        print("\n===== LATEST RESULT =====")
        print("Exam ID      :", result.get("exam_id"))
        print(
            "Score        :",
            result.get("score"),
            "/",
            result.get("total_marks")
        )
        print(
            "Percentage   :",
            result.get("percentage"),
            "%"
        )
        print("------------------------")

    # 4. Exam History
    def exam_history(self):

        results = load_data("data/results.json")

        student_results = []

        for result in results:
            if result.get("student") == self.username:
                student_results.append(result)

        if not student_results:
            print("\nNo exam history available")
            return

        print("\n===== EXAM HISTORY =====")

        for i, result in enumerate(student_results, 1):

            print("Attempt      :", i)
            print("Exam ID      :", result.get("exam_id"))
            print(
                "Score        :",
                result.get("score"),
                "/",
                result.get("total_marks")
            )
            print(
                "Percentage   :",
                result.get("percentage"),
                "%"
            )
            print("------------------------")

    # Save Result
    def save_result(
        self,
        exam_id,
        score,
        total_marks,
        percentage
    ):

        results = load_data("data/results.json")

        result = {
            "student": self.username,
            "exam_id": exam_id,
            "score": score,
            "total_marks": total_marks,
            "percentage": round(percentage, 2)
        }

        results.append(result)

        save_data("data/results.json", results)

        print("\nResult saved successfully!")


# ==================================
# STUDENT MENU
# ==================================

def student_menu(user):

    username = user.get(
        "name",
        user.get("username", "Student")
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