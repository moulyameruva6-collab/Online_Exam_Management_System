from database import fetch_all, fetch_one, execute_query


# ==========================================
# 1. ADD QUESTION
# ==========================================

def add_question():

    exams = fetch_all("""
        SELECT exam_id, exam_name
        FROM exams
        ORDER BY exam_id
    """)

    if not exams:
        print("No exams available")
        return

    print("\n--- Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        number = int(input("Enter exam number: "))
    except ValueError:
        print("Please enter a number")
        return

    if number < 1 or number > len(exams):
        print("Invalid exam number")
        return

    exam_id = exams[number - 1][0]

    question = input("Enter question: ").strip()
    a = input("Enter option A: ").strip()
    b = input("Enter option B: ").strip()
    c = input("Enter option C: ").strip()
    d = input("Enter option D: ").strip()

    if not question:
        print("Question cannot be empty")
        return

    while True:

        answer = input(
            "Enter correct answer (A/B/C/D): "
        ).upper()

        if answer in ["A", "B", "C", "D"]:
            break

        print("Enter A, B, C or D")

    execute_query("""
        INSERT INTO questions
        (
            exam_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        exam_id,
        question,
        a,
        b,
        c,
        d,
        answer
    ))

    print("Question added successfully!")


# ==========================================
# 2. VIEW QUESTIONS
# ==========================================

def view_questions():

    questions = fetch_all("""
        SELECT
            question_id,
            exam_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d,
            correct_answer
        FROM questions
        ORDER BY question_id
    """)

    if not questions:
        print("No questions available")
        return

    for i, q in enumerate(questions, 1):

        print("\nQuestion No:", i)
        print("Question ID:", q[0])
        print("Exam ID:", q[1])
        print("Question:", q[2])
        print("A.", q[3])
        print("B.", q[4])
        print("C.", q[5])
        print("D.", q[6])
        print("Answer:", q[7])


# ==========================================
# 3. DELETE QUESTION
# ==========================================

def delete_question():

    exams = fetch_all("""
        SELECT exam_id, exam_name
        FROM exams
        ORDER BY exam_id
    """)

    if not exams:
        print("No exams available")
        return

    print("\n--- Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        exam_number = int(input("Enter exam number: "))
    except ValueError:
        print("Please enter a number")
        return

    if exam_number < 1 or exam_number > len(exams):
        print("Invalid exam number")
        return

    exam_id = exams[exam_number - 1][0]

    questions = fetch_all("""
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

    if not questions:
        print("No questions available for this exam")
        return

    print("\n--- Exam Questions ---")

    for i, q in enumerate(questions, 1):

        print("\nQuestion No:", i)
        print("Question ID:", q[0])
        print("Question:", q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])
        print("Answer:", q[6])

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

    question_id = questions[number - 1][0]

    execute_query("""
        DELETE FROM questions
        WHERE question_id = %s
    """, (question_id,))

    print("Question deleted successfully!")


# ==========================================
# 4. UPDATE QUESTION
# ==========================================

def update_question():

    exams = fetch_all("""
        SELECT exam_id, exam_name
        FROM exams
        ORDER BY exam_id
    """)

    if not exams:
        print("No exams available")
        return

    print("\n--- Exams ---")

    for i, exam in enumerate(exams, 1):
        print(i, "-", exam[1])

    try:
        exam_number = int(
            input("Enter exam number: ")
        )
    except ValueError:
        print("Please enter a number")
        return

    if exam_number < 1 or exam_number > len(exams):
        print("Invalid exam number")
        return

    exam_id = exams[exam_number - 1][0]

    questions = fetch_all("""
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

    if not questions:
        print("No questions available for this exam")
        return

    print("\n--- Exam Questions ---")

    for i, q in enumerate(questions, 1):

        print("\nQuestion No:", i)
        print("Question ID:", q[0])
        print("Question:", q[1])
        print("A.", q[2])
        print("B.", q[3])
        print("C.", q[4])
        print("D.", q[5])
        print("Answer:", q[6])

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

    question_id = questions[number - 1][0]

    print("\nEnter new details")

    question = input("Enter question: ").strip()
    a = input("Enter option A: ").strip()
    b = input("Enter option B: ").strip()
    c = input("Enter option C: ").strip()
    d = input("Enter option D: ").strip()

    if not question:
        print("Question cannot be empty")
        return

    while True:

        answer = input(
            "Enter correct answer (A/B/C/D): "
        ).upper()

        if answer in ["A", "B", "C", "D"]:
            break

        print("Enter A, B, C or D")

    execute_query("""
        UPDATE questions
        SET
            question_text = %s,
            option_a = %s,
            option_b = %s,
            option_c = %s,
            option_d = %s,
            correct_answer = %s
        WHERE question_id = %s
        AND exam_id = %s
    """, (
        question,
        a,
        b,
        c,
        d,
        answer,
        question_id,
        exam_id
    ))

    print("Question updated successfully!")


# ==========================================
# 5. SEARCH QUESTION
# ==========================================

def search_question():

    questions = fetch_all("""
        SELECT
            question_id,
            exam_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d
        FROM questions
    """)

    if not questions:
        print("No questions available")
        return

    keyword = input(
        "Enter keyword to search: "
    ).lower()

    found = False

    print("\n--- Search Results ---")

    for q in questions:

        if keyword in q[2].lower():

            print("\nQuestion ID:", q[0])
            print("Exam ID:", q[1])
            print("Question:", q[2])
            print("A.", q[3])
            print("B.", q[4])
            print("C.", q[5])
            print("D.", q[6])

            found = True

    if not found:
        print("No questions found")


# ==========================================
# 6. QUESTION COUNT
# ==========================================

def question_count():

    exams = fetch_all("""
        SELECT exam_id, exam_name
        FROM exams
        ORDER BY exam_id
    """)

    if not exams:
        print("No exams available")
        return

    print("\n--- Question Count ---")

    for exam in exams:

        result = fetch_one("""
            SELECT COUNT(*)
            FROM questions
            WHERE exam_id = %s
        """, (exam[0],))

        count = result[0]

        print(
            exam[1],
            "->",
            count,
            "questions"
        )





