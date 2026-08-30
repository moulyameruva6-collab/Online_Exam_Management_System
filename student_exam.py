from utils.file_handler import load_data


def get_available_exams():
    exams = load_data("Data/exams.json")
    return exams
def display_exams():
    exams = get_available_exams()
    if not exams:
        print("No exams available.")
        return
    print("\n===== AVAILABLE EXAMS =====")
    for exam in exams:
        print(f"Exam ID     : {exam['exam_id']}")
        print(f"Exam Name   : {exam['exam_name']}")
        print(f"Duration    : {exam['duration']} minutes")
        print(f"Total Marks : {exam['total_marks']}")
        print("---------------------------")