from fastapi import APIRouter, Query
from datetime import datetime
from app.models import QueryRequest, QueryResponse, RecommendRequest, RecommendResponse, PracticeRequest, PracticeResponse
from app.gemma_engine import get_gemma_response
from app.recommender import get_recommendations, get_resources, get_visual_resources
from app.history import log_interaction, get_student_history
from app.prompt_engine import build_prompt, build_practice_prompt
import re

router = APIRouter()

# 🔍 Auto-detect subject for Guest Mode
def detect_subject_from_question(question: str) -> str:
    question = question.lower()
    if any(word in question for word in ["equation", "solve", "graph", "factor", "quadratic", "variable", "x", "y", "number", "algebra", "expression"]):
        return "Math"
    elif any(word in question for word in ["thesis", "sentence", "grammar", "paragraph", "essay", "writing", "revise", "citation", "punctuation"]):
        return "English"
    elif any(word in question for word in ["photosynthesis", "cell", "organism", "ecosystem", "respiration", "biology", "genetics", "mitosis"]):
        return "Biology"
    else:
        return "General"

# 🔎 Auto-detect concept keyword
def extract_concept_from_question(question: str) -> str:
    question = question.lower()
    keyword_map = {
        "photosynthesis": "photosynthesis",
        "quadratic": "quadratic_equations",
        "linear": "linear_equations",
        "graph": "graphing",
        "inequality": "inequalities",
        "thesis": "thesis_statement",
        "sentence": "sentence_structure",
        "grammar": "grammar",
        "cell": "cell_structure",
        "genetics": "genetics"
    }
    for keyword, concept in keyword_map.items():
        if keyword in question:
            return concept
    # fallback if no keywords matched
    words = re.findall(r"\b[a-z]{4,}\b", question)
    return words[0] if words else "general"

# 🌐 Root health check
@router.get("/", tags=["Root"])
def root():
    return {"message": "Tutor Module API is running!"}

# 🧠 Tutor response with AI + resources + visuals
@router.post("/tutor/query", response_model=QueryResponse)
def get_tutor_response(payload: QueryRequest):
    subject = (payload.subject or detect_subject_from_question(payload.question)).lower()
    concept = (payload.concept or extract_concept_from_question(payload.question)).lower()

    full_prompt = build_prompt(
        subject=subject,
        course=payload.course,
        question=payload.question,
        difficulty=payload.difficulty or "medium"
    )
    ai_response = get_gemma_response(full_prompt)

    log_interaction(
        student_id=payload.student_id or "unknown",
        course=payload.course or "unknown",
        question=payload.question,
        response=ai_response,
        concept=concept
    )

    # 📘 Resource links
    resources = get_resources(subject, concept)

    # 📊 Visual assets (image/interactive/video)
    visuals = get_visual_resources(subject, payload.course, concept)
    print("Visuals:", visuals)  # 🔍 DEBUG CHECK

    return {
        "response": ai_response,
        "resources": resources,
        "visuals": visuals,
        "subject": subject,
        "concept": concept
    }

# 🎯 Recommendation endpoint
@router.post("/tutor/recommend", response_model=RecommendResponse, tags=["Tutor"])
def get_recommendations_route(payload: RecommendRequest):
    recommendations = get_recommendations(payload.course, payload.struggled_topic)
    return {"recommendations": recommendations}

# 🕓 Get Q&A interaction logs
@router.get("/history", response_model=list[dict], tags=["Tutor"])
def get_student_history_route(
    student_id: str,
    course: str = None,
    after: str = Query(None, description="Filter logs after this date (YYYY-MM-DD)")
):
    return get_student_history(student_id, course=course, after=after)

@router.post("/tutor/practice", response_model=PracticeResponse, tags=["Tutor"])
def get_practice_question_route(payload: PracticeRequest):
    practice_prompt = build_practice_prompt(
        subject=payload.subject,
        course=payload.course,
        concept=payload.concept,
        difficulty=payload.difficulty,
        original_question=payload.question or ""  # Passes student's original question
        # question=payload.question # Optional, not used in practice prompt
    )
    response = get_gemma_response(practice_prompt)
    return {"practice_question": response}
