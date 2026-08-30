from utils.file_handler import load_data


def get_questions(exam_id):

    questions = load_data("Data/questions.json")

    exam_questions = []

    for question in questions:

        if question["exam_id"] == exam_id:
            exam_questions.append(question)

    return exam_questions


def conduct_exam(exam_id):

    questions = get_questions(exam_id)

    if not questions:

        print("\nNo questions available for this exam.")

        return []

    answers = []

    total_marks = sum(
        question["marks"]
        for question in questions
    )

    print("\n===== EXAM STARTED =====")
    print("Exam ID     :", exam_id)
    print("Questions   :", len(questions))
    print("Total Marks :", total_marks)

    for index, question in enumerate(
        questions,
        start=1
    ):

        print(
            f"\nQuestion {index}: "
            f"{question['question']}"
        )

        for option, value in question["options"].items():

            print(f"{option}. {value}")

        while True:

            user_answer = input(
                "Enter your answer (A/B/C/D): "
            ).upper()

            if user_answer in question["options"]:

                answers.append(user_answer)

                break

            else:

                print(
                    "Invalid option. "
                    "Please enter A, B, C or D."
                )

    print("\n===== EXAM COMPLETED =====")

    return answers