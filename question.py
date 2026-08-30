from database import load_data, save_data


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
        answer = input("Enter correct answer (A/B/C/D): ").upper()
        if answer in ["A", "B", "C", "D"]:
            break
        print("Enter A, B, C or D")

    question_id = 1
    if questions:
        question_id = max(q["question_id"] for q in questions) + 1

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
    save_data("data/questions.json", questions)

    print("Question added successfully!")


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


def delete_question():
    questions = load_data("data/questions.json")

    if not questions:
        print("No questions available")
        return

    view_questions()

    try:
        number = int(input("\nEnter question number to delete: "))
    except ValueError:
        print("Please enter a number")
        return

    if 1 <= number <= len(questions):
        questions.pop(number - 1)
        save_data("data/questions.json", questions)
        print("Question deleted successfully!")
    else:
        print("Invalid question number")