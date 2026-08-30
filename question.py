from database import load_data, save_data


def add_question():
    questions = load_data("data/questions.json")
    exams = load_data("data/exams.json")

    # Exam name
    exam_name = input("Enter exam name: ")

    # Check whether exam exists
    exam_found = False

    for exam in exams:
        if exam["exam_name"].lower() == exam_name.strip().lower():
            exam_found = True
            break

    if not exam_found:
        print("Invalid exam name")
        return

    # Question
    question = input("Enter question: ")

    # Options
    option_a = input("Enter option A: ")
    option_b = input("Enter option B: ")
    option_c = input("Enter option C: ")
    option_d = input("Enter option D: ")

    # Correct answer validation
    while True:
        answer = input("Enter correct answer (A/B/C/D): ").upper()

        if answer in ["A", "B", "C", "D"]:
            break

        print("Please enter A, B, C or D")

    # Create question
    new_question = {
        "exam_name": exam_name.strip(),
        "question": question,
        "A": option_a,
        "B": option_b,
        "C": option_c,
        "D": option_d,
        "answer": answer
    }

    # Save question
    questions.append(new_question)
    save_data("data/questions.json", questions)

    print("Question added successfully!")


def view_questions():
    questions = load_data("data/questions.json")

    if len(questions) == 0:
        print("No questions available")
    else:

        for i, q in enumerate(questions):

            print("\nQuestion No:", i + 1)
            print("Exam:", q["exam_name"])
            print("Question:", q["question"])
            print("A.", q["A"])
            print("B.", q["B"])
            print("C.", q["C"])
            print("D.", q["D"])


def delete_question():
    questions = load_data("data/questions.json")

    if len(questions) == 0:
        print("No questions available")
        return

    view_questions()

    # Question number validation
    try:
        number = int(input("\nEnter question number to delete: "))
    except ValueError:
        print("Please enter a number")
        return

    # Check question number
    if number >= 1 and number <= len(questions):

        questions.pop(number - 1)

        save_data("data/questions.json", questions)

        print("Question deleted successfully!")

    else:
        print("Invalid question number")