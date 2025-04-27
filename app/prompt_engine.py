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
    # 🔹 Base opening prompt
    base_prompt = (
        f"You are a helpful and knowledgeable college-level tutor creating practice problems "
        f"to reinforce student understanding of a concept.\n\n"
        f"Course: {course}\n"
        f"Subject: {subject}\n"
        f"Concept: {concept}\n"
        f"Difficulty: {difficulty.capitalize()}\n\n"
        f"The student previously asked this question:\n"
        f"\"{original_question}\"\n\n"
        f"Now, create a NEW practice problem that targets the same concept but is not identical "
        f"to the student's example. Use different numbers, structures, or contexts.\n\n"
    )

    # 🔹 Random correct answer label
    possible_answers = ["(A)", "(B)", "(C)", "(D)"]
    correct_label = random.choice(possible_answers)

    # 🔹 Subject-specific instructions
    if subject.lower() in ["math", "calculus", "college algebra", "dosage and calculation of medications", "geometry", "intermediate algebra", "pre-algebra", "precalculus", "statistics", "trigonometry"]:
        format_instructions = (
            "🧠 Math Practice Instructions:\n"
            "- Start with: `Practice Question:`\n"
            "- Clearly describe the problem.\n"
            "- For equations, always use separate lines like:\n"
            "  $$ 2x + 3y = 7 $$\n"
            "  $$ x - 4y = 1 $$\n"
            "- Use LaTeX formatting for all math expressions.\n"
            "- Provide four multiple-choice options labeled:\n"
            "  (A) ...\n"
            "  (B) ...\n"
            "  (C) ...\n"
            "  (D) ...\n"
            "- After options, insert a separator:\n"
            "---\n"
            "- Then show:\n"
            f"Answer: {correct_label}\n"
            "- After Answer, include a detailed step-by-step solution:\n"
            "- Use line breaks and LaTeX formatting for solving steps, e.g.,\n"
            "  $$ 2x + 3y = 7 $$\n"
            "  $$ x = 4y + 1 $$\n"
            "- Keep each solving step on its own line.\n"
        )

    elif subject.lower() in ["anatomy", "anatomy & physiology", "biology", "chemistry", "organic chemistry", "physics"]:
        format_instructions = (
            "🔬 Science Practice Instructions:\n"
            "- Start with: `Practice Question:`\n"
            "- Pose a science question based on the concept.\n"
            "- If helpful, mention inserting a diagram like '[Insert diagram of cell]' or '[Insert periodic table segment]'.\n"
            "- Use four multiple-choice options labeled (A), (B), (C), (D).\n"
            "- Only one answer must be correct.\n"
            "- Then write:\n"
            "---\n"
            f"Answer: {correct_label}\n"
            "Explanation: Short and clear explanation referencing key scientific facts.\n"
        )

    elif subject.lower() in ["college reading", "esl", "writing", "english"]:
        format_instructions = (
            "📖 English Practice Instructions:\n"
            "- Start with: `Practice Question:`\n"
            "- Create a reading, grammar, writing revision, or comprehension-based question.\n"
            "- Prefer multiple-choice if possible, but short answer is acceptable.\n"
            "- Provide four options if multiple choice:\n"
            "  (A) ...\n  (B) ...\n  (C) ...\n  (D) ...\n"
            "- Then write:\n"
            "---\n"
            f"Answer: {correct_label if random.random() > 0.4 else 'Corrected sentence: ...'}\n"
            "Explanation: Explain why the correct answer is the best or how the revision improves writing.\n"
        )

    else:
        format_instructions = (
            "📘 General Practice Instructions:\n"
            "- Start with: `Practice Question:`\n"
            "- Create a general problem based on the concept.\n"
            "- Use plain language.\n"
            "- Then write:\n"
            "---\n"
            f"Answer: {correct_label}\n"
            "Explanation: Briefly explain why this is the correct answer.\n"
        )

    return base_prompt + format_instructions
