import requests

payload = {
    "question": "What is the quadratic formula?",
    "student_id": "student_test",
    "course": "Algebra",
    "subject": "Math",
    "difficulty": "easy",
    "concept": "quadratic_formula"
}

try:
    response = requests.post("http://127.0.0.1:8500/tutor/query", json=payload)
    print("✅ FastAPI status code:", response.status_code)
    print("Response:")
    print(response.json())
except Exception as e:
    print("❌ Error connecting to FastAPI:", e)
