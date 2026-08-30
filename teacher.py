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


# ADD EXAM
def add_exam(user):
    exams = load_data("data/exams.json")
    subject = user.get("subject")

    if not subject:
        print("No subject assigned to this teacher")
        return

    print("Assigned Subject:", subject)

    name = input("Enter exam name: ").strip()
    if not name:
        print("Exam name cannot be empty")
        return

    sub = input("Enter subject: ").strip()

    if sub.lower() != subject.lower():
        print("You can only add exams for your assigned subject.")
        return

    for exam in exams:
        if (exam["exam_name"].lower() == name.lower()
                and exam["teacher"].lower() == user["name"].lower()):
            print("Exam already exists!")
            return

    try:
        duration = int(input("Enter exam duration (minutes): "))
        if duration <= 0:
            print("Duration must be greater than 0")
            return
    except ValueError:
        print("Please enter a valid number")
        return

    exams.append({
        "exam_name": name,
        "subject": sub,
        "teacher": user["name"],
        "duration": duration,
        "passing_percentage": 40,
        "status": "Active"
    })

    save_data("data/exams.json", exams)
    print("Exam added successfully!")


# VIEW EXAMS
def view_exams(user):
    exams = load_data("data/exams.json")
    found = False

    print("\n--- My Exams ---")

    for exam in exams:
        if exam["teacher"].lower() == user["name"].lower():
            print("Exam:", exam["exam_name"])
            print("Subject:", exam["subject"])
            print("Duration:", exam.get("duration", 0), "minutes")
            print("Passing:", exam.get("passing_percentage", 40), "%")
            print("Status:", exam.get("status", "Active"))
            print()
            found = True

    if not found:
        print("No exams available")


# UPDATE QUESTION
def update_question():
    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    view_questions()

    try:
        n = int(input("\nEnter question number to update: "))
    except ValueError:
        print("Please enter a number")
        return

    if n < 1 or n > len(questions):
        print("Invalid question number")
        return

    q = questions[n - 1]

    question = input("Enter new question: ").strip()
    a = input("Enter option A: ").strip()
    b = input("Enter option B: ").strip()
    c = input("Enter option C: ").strip()
    d = input("Enter option D: ").strip()

    while True:
        answer = input("Enter correct answer (A/B/C/D): ").strip().upper()
        if answer in ["A", "B", "C", "D"]:
            break
        print("Please enter A, B, C or D")

    q["question"] = question
    q["A"] = a
    q["B"] = b
    q["C"] = c
    q["D"] = d
    q["answer"] = answer

    save_data("data/questions.json", questions)
    print("Question updated successfully!")


# DELETE EXAM
def delete_exam(user):
    exams = load_data("data/exams.json")

    my_exams = [
        e for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    if not my_exams:
        print("No exams available")
        return

    for i, e in enumerate(my_exams):
        print(i + 1, e["exam_name"], "-", e["subject"])

    try:
        n = int(input("Enter exam number to delete: "))
    except ValueError:
        print("Please enter a number")
        return

    if n < 1 or n > len(my_exams):
        print("Invalid exam number")
        return

    exam = my_exams[n - 1]

    confirm = input("Are you sure? (yes/no): ").lower()

    if confirm != "yes":
        print("Delete cancelled")
        return

    exams.remove(exam)
    save_data("data/exams.json", exams)

    questions = load_data("data/questions.json")
    questions = [
        q for q in questions
        if q["exam_name"].lower() != exam["exam_name"].lower()
    ]
    save_data("data/questions.json", questions)

    print("Exam deleted successfully!")
    print("Related questions also deleted.")


# VIEW RESULTS
def view_results(user):
    exams = load_data("data/exams.json")
    results = load_data("data/results.json")

    my_exams = [
        e["exam_name"].lower()
        for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    found = False

    print("\n--- Exam Results ---")

    for r in results:
        if r["exam"].lower() in my_exams:
            print("Student:", r["student"])
            print("Exam:", r["exam"])
            print("Score:", r["score"], "/", r["total"])
            print("Percentage:", r["percentage"], "%")
            print("Result:", r["result"])
            print()
            found = True

    if not found:
        print("No students have taken your exams yet.")


# UPDATE EXAM
def update_exam(user):
    exams = load_data("data/exams.json")
    questions = load_data("data/questions.json")

    my_exams = [
        e for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    if not my_exams:
        print("No exams available")
        return

    for i, e in enumerate(my_exams):
        print(i + 1, e["exam_name"])

    try:
        n = int(input("Enter exam number to update: "))
    except ValueError:
        print("Please enter a number")
        return

    if n < 1 or n > len(my_exams):
        print("Invalid exam number")
        return

    exam = my_exams[n - 1]
    old_name = exam["exam_name"]

    new_name = input("Enter new exam name: ").strip()

    try:
        duration = int(input("Enter new duration (minutes): "))
    except ValueError:
        print("Please enter a number")
        return

    if not new_name or duration <= 0:
        print("Invalid exam details")
        return

    exam["exam_name"] = new_name
    exam["duration"] = duration

    # Update related questions also
    for q in questions:
        if q["exam_name"].lower() == old_name.lower():
            q["exam_name"] = new_name

    save_data("data/exams.json", exams)
    save_data("data/questions.json", questions)

    print("Exam updated successfully!")


# VIEW EXAM QUESTIONS
def view_exam_questions(user):
    exams = load_data("data/exams.json")
    questions = load_data("data/questions.json")

    my_exams = [
        e["exam_name"] for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    if not my_exams:
        print("No exams available")
        return

    for i, name in enumerate(my_exams):
        print(i + 1, name)

    try:
        n = int(input("Enter exam number: "))
    except ValueError:
        print("Please enter a number")
        return

    if n < 1 or n > len(my_exams):
        print("Invalid exam number")
        return

    name = my_exams[n - 1]
    count = 0

    print("\n--- Exam Questions ---")

    for q in questions:
        if q["exam_name"].lower() == name.lower():
            print("\nQuestion:", q["question"])
            print("A.", q["A"])
            print("B.", q["B"])
            print("C.", q["C"])
            print("D.", q["D"])
            count += 1

    if count == 0:
        print("No questions available")
    else:
        print("\nTotal Questions:", count)


# QUESTION COUNT
def question_count(user):
    exams = load_data("data/exams.json")
    questions = load_data("data/questions.json")

    print("\n--- Question Count ---")

    for exam in exams:
        if exam["teacher"].lower() == user["name"].lower():

            count = sum(
                1 for q in questions
                if q["exam_name"].lower()
                == exam["exam_name"].lower()
            )

            print(exam["exam_name"], "->", count, "questions")


# SEARCH QUESTION
def search_question(user):
    questions = load_data("data/questions.json")
    word = input("Enter keyword to search: ").lower()

    found = False

    for q in questions:
        if word in q["question"].lower():

            print("\nExam:", q["exam_name"])
            print("Question:", q["question"])
            print("A.", q["A"])
            print("B.", q["B"])
            print("C.", q["C"])
            print("D.", q["D"])

            found = True

    if not found:
        print("No matching questions found")


# STUDENT PERFORMANCE
def student_performance(user):
    exams = load_data("data/exams.json")
    results = load_data("data/results.json")

    my_exams = [
        e["exam_name"].lower()
        for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    found = False

    print("\n--- Student Performance ---")

    for r in results:
        if r["exam"].lower() in my_exams:
            print(
                r["student"],
                "-",
                r["exam"],
                "-",
                r["score"],
                "/",
                r["total"],
                "-",
                r["percentage"],
                "%"
            )
            found = True

    if not found:
        print("No student performance available")


# PASSING PERCENTAGE
def passing_percentage(user):
    exams = load_data("data/exams.json")

    my_exams = [
        e for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    if not my_exams:
        print("No exams available")
        return

    for i, e in enumerate(my_exams):
        print(i + 1, e["exam_name"])

    try:
        n = int(input("Enter exam number: "))
        value = float(input("Enter passing percentage: "))
    except ValueError:
        print("Please enter valid numbers")
        return

    if n < 1 or n > len(my_exams) or value < 0 or value > 100:
        print("Invalid input")
        return

    my_exams[n - 1]["passing_percentage"] = value

    save_data("data/exams.json", exams)
    print("Passing percentage updated successfully!")


# EXAM STATUS
def exam_status(user):
    exams = load_data("data/exams.json")

    my_exams = [
        e for e in exams
        if e["teacher"].lower() == user["name"].lower()
    ]

    if not my_exams:
        print("No exams available")
        return

    for i, e in enumerate(my_exams):
        print(i + 1, e["exam_name"], "-", e.get("status", "Active"))

    try:
        n = int(input("Enter exam number: "))
    except ValueError:
        print("Please enter a number")
        return

    if n < 1 or n > len(my_exams):
        print("Invalid exam number")
        return

    status = input(
        "Enter status (active/inactive): "
    ).strip().lower()

    if status not in ["active", "inactive"]:
        print("Please enter active or inactive")
        return

    my_exams[n - 1]["status"] = status.capitalize()

    save_data("data/exams.json", exams)
    print("Exam status updated successfully!")