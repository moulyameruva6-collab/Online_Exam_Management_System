from student_login import student_login

from student_exam import display_exams

from student_questions import conduct_exam

from student_result import (
    calculate_score,
    calculate_percentage,
    save_result,
    view_results as show_results,
    exam_history as show_history
)


class Student:

    def __init__(self, username):

        self.username = username


    # 1. View available exams
    def view_exams(self):

        display_exams()


    # 2. Attend exam
    def attend_exam(self):

        exam_id = input(
            "\nEnter Exam ID: "
        ).upper()

        answers = conduct_exam(exam_id)

        if answers:

            score, total_marks = calculate_score(
                exam_id,
                answers
            )

            percentage = calculate_percentage(
                score,
                total_marks
            )

            print("\n===== RESULT =====")

            print(
                "Score       :",
                score
            )

            print(
                "Total Marks :",
                total_marks
            )

            print(
                "Percentage  :",
                round(percentage, 2),
                "%"
            )

            save_result(
                self.username,
                exam_id,
                score,
                total_marks,
                percentage
            )


    # 3. View latest result
    def view_results(self):

        show_results(self.username)


    # 4. View exam history
    def exam_history(self):

        show_history(self.username)


# ==================================
# STUDENT LOGIN
# ==================================

username = student_login()


# ==================================
# STUDENT MENU
# ==================================

if username:

    student = Student(username)

    while True:

        print("\n===== STUDENT MENU =====")

        print("1. View Exams")
        print("2. Attend Exam")
        print("3. View Results")
        print("4. Exam History")
        print("5. Exit")

        choice = input(
            "Enter your choice: "
        )


        if choice == "1":

            student.view_exams()


        elif choice == "2":

            student.attend_exam()


        elif choice == "3":

            student.view_results()


        elif choice == "4":

            student.exam_history()


        elif choice == "5":

            print(
                "\nThank you for using "
                "Online Exam Management System."
            )

            break


        else:

            print(
                "\nInvalid choice. "
                "Please try again."
            )

else:

    print(
        "\nLogin failed. "
        "Please try again."
    )