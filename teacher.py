from database import load_data, save_data
from question import add_question, view_questions, delete_question


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
            question_count(user)
        elif choice == "12":
            search_question(user)
        elif choice == "13":
            student_performance(user)
        elif choice == "14":
            passing_percentage(user)
        elif choice == "15":
            exam_status(user)
        elif choice == "16":
            print("Logged out successfully!")
            break
        else:
            print("Invalid choice")


def my_exams(user):
    exams = load_data("data/exams.json")

    return [
        exam for exam in exams
        if exam.get("teacher", "").lower() == user["name"].lower()
    ]


def add_exam(user):
    exams = load_data("data/exams.json")

    subject = user.get("subject")

    if not subject:
        print("No subject assigned")
        return

    name = input("Enter exam name: ").strip()
    exam_subject = input("Enter subject: ").strip()

    if exam_subject.lower() != subject.lower():
        print("Wrong subject")
        return

    for exam in exams:
        if exam["exam_name"].lower() == name.lower():
            print("Exam already exists!")
            return

    try:
        duration = int(input("Enter duration (minutes): "))
    except ValueError:
        print("Enter a valid number")
        return

    exam_id = "EX" + str(101 + len(exams))

    exams.append({
        "exam_id": exam_id,
        "exam_name": name,
        "subject": exam_subject,
        "teacher": user["name"],
        "duration": duration,
        "total_marks": 0,
        "passing_percentage": 40,
        "status": "Active"
    })

    save_data("data/exams.json", exams)
    print("Exam added successfully!")


def view_exams(user):
    exams = my_exams(user)

    print("\n--- My Exams ---")

    if not exams:
        print("No exams available")
        return

    for exam in exams:
        print("\nExam:", exam["exam_name"])
        print("ID:", exam["exam_id"])
        print("Subject:", exam.get("subject", ""))
        print("Duration:", exam.get("duration", 0), "minutes")
        print("Passing:", exam.get("passing_percentage", 40), "%")
        print("Status:", exam.get("status", "Active"))


def update_question():
    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    view_questions()

    try:
        number = int(input("\nEnter question number to update: "))
        question = questions[number - 1]
    except (ValueError, IndexError):
        print("Invalid question number")
        return

    question["question"] = input("Enter new question: ")
    question["options"]["A"] = input("Enter option A: ")
    question["options"]["B"] = input("Enter option B: ")
    question["options"]["C"] = input("Enter option C: ")
    question["options"]["D"] = input("Enter option D: ")

    while True:
        answer = input("Enter correct answer (A/B/C/D): ").upper()

        if answer in ["A", "B", "C", "D"]:
            question["answer"] = answer
            break

        print("Enter A, B, C or D")

    save_data("data/questions.json", questions)
    print("Question updated successfully!")


def delete_exam(user):
    exams = load_data("data/exams.json")
    mine = my_exams(user)

    if not mine:
        print("No exams available")
        return

    for i, exam in enumerate(mine, 1):
        print(i, exam["exam_name"])

    try:
        number = int(input("Enter exam number to delete: "))
        exam = mine[number - 1]
    except (ValueError, IndexError):
        print("Invalid exam number")
        return

    confirm = input("Are you sure? (yes/no): ").lower()

    if confirm != "yes":
        print("Delete cancelled")
        return

    exams.remove(exam)
    save_data("data/exams.json", exams)

    questions = load_data("data/questions.json")
    questions = [
        q for q in questions
        if q["exam_id"] != exam["exam_id"]
    ]

    save_data("data/questions.json", questions)

    print("Exam deleted successfully!")


def view_results(user):
    results = load_data("data/results.json")
    exam_ids = [exam["exam_id"] for exam in my_exams(user)]

    print("\n--- Exam Results ---")

    found = False

    for result in results:
        if result.get("exam_id") in exam_ids:
            print("Student:", result.get("student"))
            print(
                "Score:",
                result.get("score"),
                "/",
                result.get("total_marks")
            )
            print("Percentage:", result.get("percentage"), "%")
            print()

            found = True

    if not found:
        print("No students have taken your exams yet.")


def update_exam(user):
    exams = load_data("data/exams.json")
    mine = my_exams(user)

    if not mine:
        print("No exams available")
        return

    for i, exam in enumerate(mine, 1):
        print(i, exam["exam_name"])

    try:
        number = int(input("Enter exam number: "))
        exam = mine[number - 1]
    except (ValueError, IndexError):
        print("Invalid exam number")
        return

    exam["exam_name"] = input("Enter new exam name: ").strip()

    try:
        exam["duration"] = int(
            input("Enter new duration: ")
        )
    except ValueError:
        print("Invalid duration")
        return

    save_data("data/exams.json", exams)
    print("Exam updated successfully!")


def view_exam_questions(user):
    exams = my_exams(user)
    questions = load_data("data/questions.json")

    if not exams:
        print("No exams available")
        return

    for i, exam in enumerate(exams, 1):
        print(i, exam["exam_name"])

    try:
        number = int(input("Enter exam number: "))
        exam_id = exams[number - 1]["exam_id"]
    except (ValueError, IndexError):
        print("Invalid exam number")
        return

    found = False

    print("\n--- Exam Questions ---")

    for question in questions:
        if question["exam_id"] == exam_id:
            print("\nQuestion:", question["question"])

            for key, value in question["options"].items():
                print(key + ".", value)

            found = True

    if not found:
        print("No questions available")


def question_count(user):
    questions = load_data("data/questions.json")

    print("\n--- Question Count ---")

    for exam in my_exams(user):
        count = sum(
            q["exam_id"] == exam["exam_id"]
            for q in questions
        )

        print(exam["exam_name"], "->", count, "questions")


def search_question(user):
    questions = load_data("data/questions.json")
    exams = {
        exam["exam_id"]: exam["exam_name"]
        for exam in my_exams(user)
    }

    word = input("Enter keyword to search: ").lower()

    found = False

    print("\n--- Search Results ---")

    for question in questions:
        if question["exam_id"] in exams:
            if word in question["question"].lower():

                print("\nExam:", exams[question["exam_id"]])
                print("Question:", question["question"])

                for key, value in question["options"].items():
                    print(key + ".", value)

                found = True

    if not found:
        print("No matching questions found")


def student_performance(user):
    results = load_data("data/results.json")
    exam_ids = [exam["exam_id"] for exam in my_exams(user)]

    print("\n--- Student Performance ---")

    found = False

    for result in results:
        if result.get("exam_id") in exam_ids:
            print(
                result.get("student"),
                "-",
                result.get("score"),
                "/",
                result.get("total_marks"),
                "-",
                result.get("percentage"),
                "%"
            )

            found = True

    if not found:
        print("No student performance available")


def passing_percentage(user):
    exams = load_data("data/exams.json")
    mine = my_exams(user)

    if not mine:
        print("No exams available")
        return

    for i, exam in enumerate(mine, 1):
        print(i, exam["exam_name"])

    try:
        number = int(input("Enter exam number: "))
        value = float(input("Enter passing percentage: "))
    except ValueError:
        print("Invalid input")
        return

    if not 1 <= number <= len(mine):
        print("Invalid exam number")
        return

    if not 0 <= value <= 100:
        print("Percentage must be between 0 and 100")
        return

    exam_id = mine[number - 1]["exam_id"]

    for exam in exams:
        if exam["exam_id"] == exam_id:
            exam["passing_percentage"] = value
            break

    save_data("data/exams.json", exams)

    print("Passing percentage updated successfully!")


def exam_status(user):
    exams = load_data("data/exams.json")
    mine = my_exams(user)

    if not mine:
        print("No exams available")
        return

    for i, exam in enumerate(mine, 1):
        print(
            i,
            exam["exam_name"],
            "-",
            exam.get("status", "Active")
        )

    try:
        number = int(input("Enter exam number: "))
    except ValueError:
        print("Invalid number")
        return

    if not 1 <= number <= len(mine):
        print("Invalid exam number")
        return

    status = input(
        "Enter status (active/inactive): "
    ).lower()

    if status not in ["active", "inactive"]:
        print("Enter active or inactive")
        return

    exam_id = mine[number - 1]["exam_id"]

    for exam in exams:
        if exam["exam_id"] == exam_id:
            exam["status"] = status.capitalize()
            break

    save_data("data/exams.json", exams)

    print("Exam status updated successfully!")