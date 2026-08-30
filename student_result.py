from utils.file_handler import load_data, save_data


# Calculate student score
def calculate_score(exam_id, answers):

    questions = load_data("Data/questions.json")

    exam_questions = []

    for question in questions:
        if question["exam_id"] == exam_id:
            exam_questions.append(question)

    score = 0
    total_marks = 0

    for question, student_answer in zip(exam_questions, answers):

        total_marks += question["marks"]

        if student_answer == question["answer"]:
            score += question["marks"]

    return score, total_marks


# Calculate percentage
def calculate_percentage(score, total_marks):

    if total_marks == 0:
        return 0

    percentage = (score / total_marks) * 100

    return percentage


# Save exam result
def save_result(username, exam_id, score, total_marks, percentage):

    results = load_data("Data/results.json")

    result = {
        "username": username,
        "exam_id": exam_id,
        "score": score,
        "total_marks": total_marks,
        "percentage": round(percentage, 2)
    }

    results.append(result)

    save_data("Data/results.json", results)

    print("\nResult saved successfully.")


# View latest result
def view_results(username):

    results = load_data("Data/results.json")

    student_results = []

    for result in results:

        if result["username"] == username:
            student_results.append(result)

    if not student_results:

        print("\nNo results found.")
        return

    # Get latest result
    latest_result = student_results[-1]

    print("\n===== LATEST RESULT =====")

    print("Exam ID      :", latest_result["exam_id"])
    print(
        "Score        :",
        latest_result["score"],
        "/",
        latest_result["total_marks"]
    )
    print(
        "Percentage   :",
        latest_result["percentage"],
        "%"
    )

    print("------------------------")


# View complete exam history
def exam_history(username):

    results = load_data("Data/results.json")

    student_history = []

    for result in results:

        if result["username"] == username:
            student_history.append(result)

    if not student_history:

        print("\nNo exam history found.")
        return

    print("\n===== EXAM HISTORY =====")

    for index, result in enumerate(student_history, start=1):

        print("Attempt      :", index)
        print("Exam ID      :", result["exam_id"])
        print(
            "Score        :",
            result["score"],
            "/",
            result["total_marks"]
        )
        print(
            "Percentage   :",
            result["percentage"],
            "%"
        )

        print("------------------------")
