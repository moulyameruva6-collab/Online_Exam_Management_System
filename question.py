from database import load_data, save_data


# ==============================
# ADD QUESTION
# ==============================

def add_question():

    questions = load_data("data/questions.json")
    exams = load_data("data/exams.json")

    if not exams:
        print("No exams available")
        return

    print("\n--- Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, exam["exam_id"], "-", exam["exam_name"])

    try:
        number = int(input("Enter exam number: "))
        exam = exams[number - 1]
    except (ValueError, IndexError):
        print("Invalid exam number")
        return

    question = input("Enter question: ")
    a = input("Enter option A: ")
    b = input("Enter option B: ")
    c = input("Enter option C: ")
    d = input("Enter option D: ")

    while True:

        answer = input(
            "Enter correct answer (A/B/C/D): "
        ).upper()

        if answer in ["A", "B", "C", "D"]:
            break

        print("Enter A, B, C or D")

    question_id = 1

    if questions:
        question_id = max(
            q["question_id"] for q in questions
        ) + 1

    new_question = {
        "exam_id": exam["exam_id"],
        "question_id": question_id,
        "question": question,
        "options": {
            "A": a,
            "B": b,
            "C": c,
            "D": d
        },
        "answer": answer,
        "marks": 1
    }

    questions.append(new_question)

    save_data(
        "data/questions.json",
        questions
    )

    # Update total marks
    total = 0

    for q in questions:
        if q["exam_id"] == exam["exam_id"]:
            total += q["marks"]

    exam["total_marks"] = total

    save_data(
        "data/exams.json",
        exams
    )

    print("Question added successfully!")


# ==============================
# VIEW QUESTIONS
# ==============================

def view_questions():

    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    for i, q in enumerate(questions, 1):

        print("\nQuestion No:", i)
        print("Exam ID:", q["exam_id"])
        print("Question:", q["question"])

        for option, value in q["options"].items():
            print(option + ".", value)

        print("Answer:", q["answer"])


# ==============================
# DELETE QUESTION
# ==============================

def delete_question():

    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    view_questions()

    try:
        number = int(
            input("\nEnter question number to delete: ")
        )
    except ValueError:
        print("Please enter a number")
        return

    if number < 1 or number > len(questions):
        print("Invalid question number")
        return

    exam_id = questions[number - 1]["exam_id"]

    questions.pop(number - 1)

    save_data(
        "data/questions.json",
        questions
    )

    # Update total marks
    exams = load_data("data/exams.json")

    for exam in exams:

        if exam["exam_id"] == exam_id:

            total = 0

            for q in questions:
                if q["exam_id"] == exam_id:
                    total += q["marks"]

            exam["total_marks"] = total

            break

    save_data(
        "data/exams.json",
        exams
    )

    print("Question deleted successfully!")


# ==============================
# UPDATE QUESTION
# ==============================

def update_question():

    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    view_questions()

    try:
        number = int(
            input("\nEnter question number to update: ")
        )
    except ValueError:
        print("Please enter a number")
        return

    if number < 1 or number > len(questions):
        print("Invalid question number")
        return

    q = questions[number - 1]

    print("\nEnter new details")

    q["question"] = input("Enter question: ")
    q["options"]["A"] = input("Enter option A: ")
    q["options"]["B"] = input("Enter option B: ")
    q["options"]["C"] = input("Enter option C: ")
    q["options"]["D"] = input("Enter option D: ")

    while True:

        answer = input(
            "Enter correct answer (A/B/C/D): "
        ).upper()

        if answer in ["A", "B", "C", "D"]:
            q["answer"] = answer
            break

        print("Enter A, B, C or D")

    save_data(
        "data/questions.json",
        questions
    )

    print("Question updated successfully!")


# ==============================
# SEARCH QUESTION
# ==============================

def search_question():

    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    keyword = input(
        "Enter keyword to search: "
    ).lower()

    found = False

    print("\n--- Search Results ---")

    for q in questions:

        if keyword in q["question"].lower():

            print("\nExam ID:", q["exam_id"])
            print("Question:", q["question"])

            for option, value in q["options"].items():
                print(option + ".", value)

            found = True

    if not found:
        print("No questions found")


# ==============================
# QUESTION COUNT
# ==============================

def question_count():

    questions = load_data("data/questions.json")
    exams = load_data("data/exams.json")

    if not exams:
        print("No exams available")
        return

    print("\n--- Question Count ---")

    for exam in exams:

        count = 0

        for q in questions:
            if q["exam_id"] == exam["exam_id"]:
                count += 1

        print(
            exam["exam_name"],
            "->",
            count,
            "questions"
        )