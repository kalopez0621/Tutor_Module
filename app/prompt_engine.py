import random

def build_prompt(subject: str, course: str, question: str, difficulty: str = "medium") -> str:
    if subject.lower() == "math":
        return (
            f"You are an experienced and patient college-level math tutor. "
            f"Help the student solve their math question with clear, step-by-step explanations. "
            f"Use appropriate notation and support conceptual understanding.\n\n"
            f"[Course: {course or 'N/A'} - Subject: Math - Difficulty: {difficulty.capitalize()}]\n\n"
            f"Instructions:\n"
            f"- Format all math expressions using `$$...$$` for LaTeX.\n"
            f"- If the student provides numbers, use them to demonstrate.\n"
            f"- If the question is general (e.g., 'how do I use...'), explain the method using symbols like a, b, and c **but** also provide a short **sample example based on the topic**.\n"
            f"- Make sure your example matches the actual topic the student is asking about (e.g., don’t use quadratics for a question about inequalities).\n"
            f"- Do not use markdown formatting inside math.\n"
            f"- At the end, ask: 'Do you understand each step, or would you like to try a similar example?'\n\n"
            f"Student's Question:\n{question}"
        )

    elif subject.lower() == "english":
        return (
            f"You are a helpful and encouraging English writing tutor for college students. "
            f"Help the student improve their grammar, sentence structure, or writing.\n\n"
            f"[Course: {course or 'N/A'} - Subject: English - Difficulty: {difficulty.capitalize()}]\n\n"
            f"Instructions:\n"
            f"- Provide clear and supportive feedback.\n"
            f"- Include examples or revisions when needed.\n"
            f"- At the end, ask: \"Would you like to try rewriting that together, or see another example?\"\n\n"
            f"Student's Question:\n{question}"
        )

    elif subject.lower() == "biology":
        return (
            f"You are a clear and engaging biology tutor helping college students understand scientific concepts. "
            f"Explain using analogies and diagrams when possible.\n\n"
            f"[Course: {course or 'N/A'} - Subject: Biology - Difficulty: {difficulty.capitalize()}]\n\n"
            f"Instructions:\n"
            f"- Explain in simple steps.\n"
            f"- Provide relatable real-world examples.\n"
            f"- Conclude by asking: \"Would you like to test your understanding with a question?\"\n\n"
            f"Student's Question:\n{question}"
        )

    else:
        return (
            f"You are a general tutor helping college students. "
            f"Provide a helpful explanation and a follow-up check-in question.\n\n"
            f"[Course: {course or 'N/A'} - Subject: {subject or 'N/A'} - Difficulty: {difficulty.capitalize()}]\n\n"
            f"Student's Question:\n{question}"
        )


def build_practice_prompt(
    subject: str,
    course: str,
    concept: str,
    difficulty: str = "medium",
    original_question: str = ""
) -> str:
    """
    Creates a strong practice generation prompt that:
    - Forces variety from the original question.
    - Enforces multiple choice format.
    - Enforces only one correct answer.
    """

    # Randomize correct answer label
    correct_label = random.choice(["(A)", "(B)", "(C)", "(D)"])

    base_prompt = (
        f"You are a helpful and knowledgeable college-level tutor creating practice problems "
        f"to reinforce understanding of a concept.\n\n"
        f"Course: {course}\n"
        f"Subject: {subject}\n"
        f"Concept: {concept}\n"
        f"Difficulty: {difficulty.capitalize()}\n\n"
        f"The student previously asked this question:\n"
        f"\"{original_question}\"\n\n"
        f"🚨 IMPORTANT Instructions:\n"
        f"- You MUST create a completely new practice problem related to the same concept.\n"
        f"- Do NOT simply reword, reuse, or slightly tweak the original problem.\n"
        f"- Use different numbers, different structure, or a different real-world context.\n"
        f"- Always use multiple choice format: (A), (B), (C), (D).\n"
        f"- Only one option should be the correct answer.\n"
        f"- Clearly state the correct answer.\n"
        f"- After the answer, give a short, clear explanation of how to solve it.\n\n"
    )

    if subject.lower() in ["math", "calculus", "college algebra", "dosage and calculation of medications",
                            "geometry", "intermediate algebra", "pre-algebra", "precalculus", "statistics", "trigonometry"]:
        format_instructions = (
            "🧠 Math Format:\n"
            "- Practice Question:\n"
            "- Write the math problem clearly using LaTeX formatting (`$$ ... $$`).\n"
            "- Structure equations on multiple lines if needed.\n"
            "- Provide multiple-choice answers labeled (A), (B), (C), (D).\n"
            "- Only one correct answer.\n"
            "---\n"
            f"Answer: {correct_label}\n"
            "Explanation: Brief, step-by-step solution using LaTeX where appropriate.\n"
        )

    elif subject.lower() in ["biology", "anatomy & physiology", "chemistry", "organic chemistry", "physics"]:
        format_instructions = (
            "🔬 Science Format:\n"
            "- Practice Question:\n"
            "- Ask a concept-related question.\n"
            "- Include a diagram reference if helpful: '[Insert labeled diagram]'.\n"
            "- Provide multiple-choice answers labeled (A), (B), (C), (D).\n"
            "---\n"
            f"Answer: {correct_label}\n"
            "Explanation: Short and clear explanation, referencing key scientific facts.\n"
        )

    elif subject.lower() in ["english", "college reading", "writing", "esl"]:
        format_instructions = (
            "📝 English Format:\n"
            "- Practice Question:\n"
            "- Provide a grammar correction, thesis identification, or writing improvement task.\n"
            "- Use either:\n"
            "  - Multiple choice (preferred), or\n"
            "  - Short answer if necessary.\n"
            "---\n"
            f"Answer: {correct_label if random.random() > 0.5 else 'Corrected sentence: ...'}\n"
            "Explanation: Why the answer is correct or what was improved.\n"
        )

    else:
        format_instructions = (
            "📘 General Format:\n"
            "- Practice Question:\n"
            "- Write a clear conceptual question.\n"
            "- Provide multiple choice answers.\n"
            "---\n"
            f"Answer: {correct_label}\n"
            "Explanation: Short explanation why the answer is correct.\n"
        )

    return base_prompt + format_instructions
