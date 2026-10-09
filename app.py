import streamlit as st
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
from core.agent import generate_response

load_dotenv()

st.set_page_config(
    page_title="HomeCredit Voice AI",
    page_icon="📞",
    layout="centered"
)

st.title("📞 HomeCredit Voice AI")
st.caption("Loan Against Property — Preliminary Qualification")


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "started" not in st.session_state:
    st.session_state.started = False


def start_call():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I'm calling from Home Credit. "
                "May I speak with the intended customer, please?"
            )
        }
    ]
    st.session_state.started = True


# Sidebar controls
with st.sidebar:
    st.header("Call Controls")
    st.info("Demo mode — use fictional customer details.")

    if st.button("Start New Call", use_container_width=True):
        start_call()
        st.rerun()

    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.started = False
        st.rerun()


# Start screen
if not st.session_state.started:
    st.write("Start a demo call to test the AI qualification flow.")

    if st.button("Start Demo Call", type="primary"):
        start_call()
        st.rerun()


# Display conversation
for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            if st.button("🔊 Generate Audio", key=f"audio_{index}"):
                try:
                    audio_buffer = BytesIO()
                    gTTS(
                        text=message["content"],
                        lang="en"
                    ).write_to_fp(audio_buffer)

                    st.audio(
                        audio_buffer.getvalue(),
                        format="audio/mp3"
                    )
                except Exception as error:
                    st.error(f"Audio generation failed: {error}")


# Chat input and AI response
if st.session_state.started:
    user_input = st.chat_input(
        "Type the customer's response..."
    )

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            with st.spinner("AI is responding..."):
                answer = generate_response(
                    st.session_state.messages
                )

            if not answer or not answer.strip():
                answer = (
                    "I'm sorry, I couldn't generate a response. "
                    "Could you please repeat that?"
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as error:
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    f"AI response failed: {error}"
                )
            })

        st.rerun()


st.divider()

st.caption(
    "Prototype only. Eligibility is preliminary and requires "
    "review by a qualified Home Credit loan expert."
)