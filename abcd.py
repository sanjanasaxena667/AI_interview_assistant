import streamlit as st
import pytesseract
import json
import re
from PIL import Image
from pdf2image import convert_from_bytes
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from voice_interviewer import record_audio, speech_to_text, speak, remove_silence


if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

POPPLER_PATH = r"C:\\Users\\Sanjhana\\Downloads\\Release-25.12.0-0\\poppler-25.12.0\\Library\\bin"

# Page Config
st.set_page_config(page_title="AI Interviewer Live", layout="wide")
st.title("Live AI Interview Simulation")

# --- SESSION STATE INITIALIZATION ---
if "audio_to_play" not in st.session_state:
    st.session_state.audio_to_play = None
if "messages" not in st.session_state:
    st.session_state.messages = []

if "scores" not in st.session_state:
    st.session_state.scores = []

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "context_data" not in st.session_state:
    st.session_state.context_data = ""

if "phase" not in st.session_state:
    st.session_state.phase = "intro"

if "tech_question_count" not in st.session_state:
    st.session_state.tech_question_count = 0

if "beh_question_count" not in st.session_state:
    st.session_state.beh_question_count = 0


# --- SIDEBAR & SETUP ---
with st.sidebar:

    st.header("Interview Settings")

    model_id = st.text_input(
        "Ollama Model ID",
        value="deepseek-v3.1:671b-cloud"
    )

    st.markdown("---")

    st.write("### 1. Upload Documents")

    uploaded_resume = st.file_uploader(
        "Upload Resume (PDF/Image)",
        type=["pdf", "png", "jpg"]
    )

    job_description = st.text_area(
        "Paste Job Description",
        height=150
    )

    col1, col2 = st.columns(2)

    with col1:
        start_btn = st.button("Start Interview", type="primary")

    with col2:
        if st.button("End Interview", type="secondary"):
            if st.session_state.interview_active:
                st.session_state.phase = "ended"
                st.rerun()

    if st.button("Reset / Clear Chat"):
        st.session_state.messages = []
        st.session_state.interview_active = False
        st.session_state.phase = "intro"
        st.session_state.tech_question_count = 0
        st.session_state.beh_question_count = 0
        st.rerun()

    if st.session_state.interview_active:
        if st.session_state.audio_to_play:
            speak(st.session_state.audio_to_play)
            st.session_state.audio_to_play = None
        st.info(f"Phase: {st.session_state.phase.capitalize()}")
        st.info(f"Tech Questions: {st.session_state.tech_question_count}/10")
        st.info(f"Behavioral Questions: {st.session_state.beh_question_count}/5")


# --- FUNCTIONS ---

def extract_text_from_file(uploaded_file):

    text = ""

    try:

        if uploaded_file.type == "application/pdf":

            images = convert_from_bytes(
                uploaded_file.read(),
                poppler_path=POPPLER_PATH
            )

            for img in images:
                text += pytesseract.image_to_string(img)

        else:

            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)

    except Exception as e:

        st.error(f"OCR Error: {e}")
        return None

    return text


def get_interviewer_response(history, context, phase):

    llm = OllamaLLM(
        model=model_id,
        stop=["Candidate:", "User:", "Answer:", "\n\n"]
    )

    if phase == "intro":

        instruction = """
        You are an expert Hiring Manager.
        1. Greet the candidate warmly.
        2. Ask them to introduce themselves.
        3. STOP immediately after asking.
        """

    elif phase == "technical":

        instruction = """
        You are conducting the TECHNICAL portion of the interview.

        1. Ask ONE specific technical question based on the candidate's resume and job description.
        2. Do NOT provide the answer.
        3. remember the previous answer.
        4. after intro start asking questions related to data structure and algorithm like:- ask any coding problem.
        5. generate the follow up question based on previous answer.
        6. after that ask question/discuss related to project.
        7. STOP immediately after asking.
        """

    elif phase == "behavioral":

        instruction = """
        You are conducting the BEHAVIORAL portion of the interview.

        1. Ask ONE behavioral question.
        2. STOP immediately after asking.
        """

    elif phase == "ended":

        instruction = """
        The interview is over.

        1. Thank the candidate.
        2. Say goodbye.
        """

    else:

        instruction = "You are an interviewer. Ask one question."

    system_prompt = f"""
    CRITICAL: You are the interviewer. Never answer for the candidate.

    YOUR GOAL:
    {instruction}

    CONTEXT:
    {context}

    CHAT HISTORY:
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    response = chain.invoke(
        {
            "chat_history": history
        }
    )

    return response

def evaluate_answer(question, answer):

    llm = OllamaLLM(model="deepseek-v3.1:671b-cloud") 
    # use same strong model OR at least qwen2.5:3b

    prompt = f"""
You are a STRICT technical interviewer.

STEP 1: Generate a short ideal correct answer.
STEP 2: Compare candidate answer with ideal answer.
STEP 3: Give score from 0-10.

SCORING RULES:

10 = fully correct, clear explanation
8-9 = mostly correct, small mistake
6-7 = partially correct but missing important details
3-5 = weak understanding
1-2 = incorrect
0 = candidate refused, said "I don't know", or irrelevant answer

Be VERY strict.

Question:
{question}

Candidate Answer:
{answer}

Return ONLY valid JSON:

{{
"score": number,
"feedback": "1-2 line improvement suggestion"
}}
"""

    response = llm.invoke(prompt)

    try:
        json_match = re.search(r"\{[^{}]*\}", response)

        if json_match:
            result = json.loads(json_match.group())

            score = float(result["score"])

            score = max(0, min(10, score))

            return score, result["feedback"]

    except:
        pass

    return 0, "Model could not evaluate answer"


# --- MAIN LOGIC ---

# Start Interview
if start_btn:

    if not uploaded_resume or not job_description:

        st.warning("Please upload both Resume and Job Description.")

    else:

        with st.spinner("Analyzing documents..."):

            raw_text = extract_text_from_file(uploaded_resume)

            if raw_text:

                full_context = f"""
                JOB DESCRIPTION:
                {job_description}

                CANDIDATE RESUME:
                {raw_text}
                """

                st.session_state.context_data = full_context
                st.session_state.interview_active = True

                st.session_state.phase = "intro"
                st.session_state.tech_question_count = 0
                st.session_state.beh_question_count = 0

                # Generate Opening Question
                initial_history = []

                opening_response = get_interviewer_response(
                    initial_history,
                    st.session_state.context_data,
                    "intro"
                )

                st.session_state.messages = [
                    AIMessage(content=opening_response)
                ]

                # 🔊 SPEAK FIRST QUESTION
                clean_response = opening_response.strip()
                st.session_state.audio_to_play = clean_response
                # speak(clean_response)

                st.rerun()


# Chat Interface
if st.session_state.interview_active:
    if st.session_state.audio_to_play:
        speak(st.session_state.audio_to_play)
        st.session_state.audio_to_play = None
    for msg in st.session_state.messages:

        if isinstance(msg, AIMessage):

            with st.chat_message("assistant"):
                st.write(msg.content)

        elif isinstance(msg, HumanMessage):

            with st.chat_message("user"):
                st.write(msg.content)

    if st.session_state.phase == "ended":

        st.info("The interview has ended.")

        if not isinstance(st.session_state.messages[-1], AIMessage):

            with st.spinner("Closing interview..."):

                final_response = get_interviewer_response(
                    st.session_state.messages,
                    st.session_state.context_data,
                    "ended"
                )

                st.session_state.messages.append(
                    AIMessage(content=final_response)
                )

                st.rerun()

    else:

        user_input = None
        if "recording" not in st.session_state:
            st.session_state.recording = False

        
        if st.button("Answer with Voice"):
            
            with st.spinner("Recording your answer..."):

                audio_file = record_audio()
            st.success("Recording finished")
                
            user_input = speech_to_text(audio_file)
            st.write("You said:", user_input)

        # TEXT ANSWER OPTION
        st.markdown("### Write your answer (for coding questions)")

        code_input = st.text_area(
            "Write your code here:",
            height=200,
            placeholder="Example:\n\nint add(int a, int b){\n    return a+b;\n}"
        )

        submit_code = st.button("Submit Code")
        
        if user_input:

            st.session_state.messages.append(
                HumanMessage(content=user_input)
            )
            # Get previous interviewer question
            previous_question = None
            for msg in reversed(st.session_state.messages[:-1]):
                if isinstance(msg, AIMessage):
                    previous_question = msg.content
                    break
            # Evaluate answer
            if previous_question:
                score, feedback = evaluate_answer(previous_question, user_input)

                st.session_state.scores.append(score)
                st.session_state.feedbacks.append(feedback)

                st.success(f"Score for this answer: {score}/10")
                st.info(f"Feedback: {feedback}")

            with st.chat_message("user"):
                st.write(user_input)

            if st.session_state.phase == "intro":

                st.session_state.phase = "technical"

            elif st.session_state.phase == "technical":

                st.session_state.tech_question_count += 1

                if st.session_state.tech_question_count >= 10:
                    st.session_state.phase = "behavioral"

            elif st.session_state.phase == "behavioral":

                st.session_state.beh_question_count += 1

                if st.session_state.beh_question_count >= 5:
                    st.session_state.phase = "ended"

                if st.session_state.scores:
                    total_score = sum(st.session_state.scores)
                    max_score = len(st.session_state.scores) * 10
                    percentage = (total_score / max_score) * 100
                    st.subheader("Interview Performance")
                    st.write(f"Total Score: {total_score}/{max_score}")
                    st.write(f"Performance: {percentage:.2f}%")

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    ai_response = get_interviewer_response(
                        st.session_state.messages,
                        st.session_state.context_data,
                        st.session_state.phase
                    )

                    st.write(ai_response)
                    clean_response = ai_response.strip()
                    # print("AI Question:", clean_response)
                    # speak(clean_response)
                    st.session_state.audio_to_play = clean_response

            st.session_state.messages.append(
                AIMessage(content=ai_response)
            )

            st.rerun()

else:

    st.info(
        "Upload your documents in the sidebar and click 'Start Interview' to begin."
    )