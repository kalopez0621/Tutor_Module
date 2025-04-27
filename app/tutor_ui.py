import streamlit as st
import requests
import re

st.set_page_config(page_title="Tutor Module – Guest Mode", layout="centered")
st.title("🎓 AI Tutor (Guest Access)")

# 🔁 Initialize session state variables
for key in [
    "response", "question", "clarify_mode", "visuals", "resources",
    "show_practice", "practice_question", "practice_answer",
    "practice_revealed", "course", "concept", "subject"
]:
    if key not in st.session_state:
        st.session_state[key] = "" if key in ["response", "question", "practice_question", "course", "concept", "subject"] else False

# 📝 Ask initial question
with st.form("guest_form"):
    question = st.text_area("Ask your question:", value=st.session_state.question)
    course = st.text_input("Optional: What course is this related to?", value=st.session_state.course or " ")
    submitted = st.form_submit_button("Submit")

# 🔍 Submit main question to FastAPI
if submitted and question:
    st.session_state.question = question
    st.session_state.course = course
    st.session_state.practice_question = ""
    st.session_state.practice_revealed = False
    st.session_state.practice_answer = ""

    payload = {
        "question": question,
        "student_id": "guest_user",
        "course": course,
        "subject": "",
        "difficulty": "medium",
        "concept": ""
    }

    with st.spinner("Thinking..."):
        try:
            res = requests.post("http://127.0.0.1:8500/tutor/query", json=payload)
            data = res.json()
            st.session_state.response = data.get("response", "")
            st.session_state.resources = data.get("resources", [])
            st.session_state.visuals = data.get("visuals", [])
            st.session_state.clarify_mode = False
            st.session_state.show_practice = False
            st.session_state.concept = data.get("concept", "")  # optional if returned
            st.session_state.subject = data.get("subject", "")  # optional if returned
        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# 🧠 Render AI response
def render_response(response_text):
    for line in response_text.split("\n"):
        line = line.strip()
        if line.startswith("```latex") or line.startswith("$$$"):  # ✅ Skip raw LaTeX block indicators
            continue
        if "$$" in line:
            for block in re.findall(r"\$\$(.*?)\$\$", line):
                st.latex(block.strip())
            extra = re.sub(r"\$\$(.*?)\$\$", "", line).strip()
            if extra:
                st.markdown(extra)
        elif re.search(r"\\frac|\\sqrt|\\pm|\\begin|\\end|\\[a-zA-Z]+", line):
            st.latex(line)
        elif line:
            st.markdown(line)

# 📘 Display explanation + visuals + resources
if st.session_state.response:
    st.subheader("🧠 Tutor Response:")
    render_response(st.session_state.response)

    if st.session_state.resources:
        st.subheader("📎 Resources:")
        for link in st.session_state.resources:
            if link.startswith("http"):
                st.markdown(f"- [Watch here]({link})")
            else:
                st.write(f"- {link}")

    if st.session_state.visuals:
        st.subheader("🖼️ Visual Aids:")
        for visual in st.session_state.visuals:
            if visual.endswith((".jpg", ".jpeg", ".png", ".gif")):
                st.image(visual, use_container_width=True)
            elif "youtube.com" in visual:
                st.markdown(f"▶️ [Watch Video]({visual})")
            elif "desmos.com" in visual or "cellsalive.com" in visual:
                st.markdown(f"🧪 [Interactive Tool]({visual})")
            elif visual.startswith("http"):
                st.markdown(f"- [View Resource]({visual})")

    # 🧠 Understanding check
    st.subheader("❓ Did you understand the explanation?")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("✅ Yes, give me a practice question!"):
            st.session_state.show_practice = True
            st.session_state.clarify_mode = False
    with col2:
        if st.button("🤔 Not sure"):
            st.session_state.clarify_mode = True
    with col3:
        if st.button("❌ No, explain again"):
            st.session_state.clarify_mode = True

# 💬 Clarification flow
if st.session_state.clarify_mode:
    st.subheader("💬 What part should I clarify?")
    clarification_input = st.text_area("Type your confusion or question here:")
    if st.button("📨 Send Clarification Request"):
        if clarification_input:
            follow_up = {
                "question": f"The student asked for clarification: {clarification_input}",
                "student_id": "guest_user",
                "course": st.session_state.course,
                "subject": st.session_state.subject or " ",
                "difficulty": "medium",
                "concept": st.session_state.concept or ""
            }
            with st.spinner("Getting a clearer explanation..."):
                try:
                    res = requests.post("http://127.0.0.1:8500/tutor/query", json=follow_up)
                    data = res.json()
                    st.session_state.response = data.get("response", "")
                    st.session_state.resources = data.get("resources", [])
                    st.session_state.visuals = data.get("visuals", [])
                    st.session_state.clarify_mode = False
                    st.session_state.show_practice = True
                except Exception as e:
                    st.error(f"❌ Clarification failed: {e}")

# 🧪 Practice request 
if st.session_state.show_practice and not st.session_state.practice_question:
    with st.spinner("Creating a practice problem..."):
        try:
            practice_payload = {
                "subject": st.session_state.subject or "Math",
                "course": st.session_state.course,
                "concept": st.session_state.concept or st.session_state.question,
                "difficulty": "medium",
                "question": st.session_state.question
            }
            res = requests.post("http://127.0.0.1:8500/tutor/practice", json=practice_payload)
            data = res.json()
            st.session_state.practice_question = data.get("practice_question", "")
        except Exception as e:
            st.error(f"⚠️ Could not generate practice question: {e}")

# 🧠 Show practice and answer flow
if st.session_state.practice_question:
    st.subheader("📝 Practice Time!")
    question_only = st.session_state.practice_question.split("Answer:")[0].strip()
    st.markdown(f"**{question_only}**")

    if not st.session_state.practice_revealed:
        st.session_state.practice_answer = st.text_input("Your answer:")
        if st.button("📩 Submit Answer"):
            st.session_state.practice_revealed = True

    if st.session_state.practice_revealed:
        try:
            full = st.session_state.practice_question
            answer_part = full.split("Answer:")[-1].strip()
            st.success("✅ Here's the correct answer and explanation:")
            st.markdown(f"**Answer:** {answer_part}")

                    # 🔁 Follow-up options after practice
            st.subheader("🚀 What would you like to do next?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Another Practice Question"):
                    st.session_state.practice_question = ""
                    st.session_state.practice_revealed = False
                    st.session_state.show_practice = True
            with col2:
                if st.button("❓ Clarify Explanation Again"):
                    st.session_state.clarify_mode = True
                    st.session_state.practice_question = ""
                    st.session_state.practice_revealed = False
            with col3:
                if st.button("✅ I'm Good, Start New Question"):
                    st.experimental_rerun()

        except:
            st.error("⚠️ Could not display the answer.")

