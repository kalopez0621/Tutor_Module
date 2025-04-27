import json
import os
from datetime import datetime

history_file = "qa_history.json"
qa_history = []

# Load history from file at startup
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as f:
        try:
            qa_history = json.load(f)
        except json.JSONDecodeError:
            qa_history = []

def save_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(qa_history, f, indent=2)

def log_interaction(student_id: str, course: str, question: str, response: str, concept: str = None):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "student_id": student_id,
        "course": course,
        "question": question,
        "response": response,
        "concept": concept
    }
    qa_history.append(entry)
    save_history()

def get_student_history(student_id: str, course: str = None, after: str = None):
    results = [entry for entry in qa_history if entry["student_id"] == student_id]

    if course:
        results = [entry for entry in results if entry["course"].lower() == course.lower()]

    if after:
        try:
            after_date = datetime.fromisoformat(after)
            results = [entry for entry in results if datetime.fromisoformat(entry["timestamp"]) > after_date]
        except ValueError:
            pass  # Invalid date format — ignore

    return results

