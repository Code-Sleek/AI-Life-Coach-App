# app.py

import io

import speech_recognition as sr
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder

import os
from datetime import datetime

import streamlit as st
import pandas as pd

from emotion_model import EmotionModel
from goal_generator import suggest_goals
from chat_logic import build_coach_response

# ---------- Model loading ----------

@st.cache_resource
def load_emotion_model():
    return EmotionModel()

emotion_model = load_emotion_model()

# ---------- History helpers ----------

HISTORY_PATH = "data/history.csv"
os.makedirs("data", exist_ok=True)

def load_history():
    if os.path.exists(HISTORY_PATH):
        return pd.read_csv(HISTORY_PATH)
    else:
        # One row per goal
        return pd.DataFrame(
            columns=["timestamp", "text", "emotion", "goal", "completed"]
        )

def save_history(df: pd.DataFrame):
    df.to_csv(HISTORY_PATH, index=False)

def append_history(text: str, emotion: str, goals):
    df = load_history()
    ts = datetime.now().isoformat()

    rows = []
    for g in goals:
        rows.append(
            {
                "timestamp": ts,
                "text": text,
                "emotion": emotion,
                "goal": g,
                "completed": False,
            }
        )

    new_rows = pd.DataFrame(rows)
    df = pd.concat([df, new_rows], ignore_index=True)
    save_history(df)

# ---------- Speech & TTS helpers ----------

recognizer = sr.Recognizer()

def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    """Convert raw audio bytes (WAV) to text using SpeechRecognition."""
    if not audio_bytes:
        return ""

    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        # Uses Google Web Speech API (requires internet)
        text = recognizer.recognize_google(audio_data, language="en-US")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"[speech recognition error: {e}]"

def text_to_speech(text: str, filename: str = "coach_response.mp3") -> str:
    """Convert text to speech using gTTS and save as an mp3 file."""
    if not text.strip():
        return ""
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename


# ---------- UI ----------

def main():
    # ---- persistent state for the current input ----
    if "user_text" not in st.session_state:
        st.session_state["user_text"] = ""

    st.title("🧠 AI Life Coach: Emotion-Aware Goal Setter")
    st.write(
        "Choose how you want to check in, then I’ll detect your mood and suggest small, "
        "actionable goals you can try."
    )

    # ---- Input mode selection ----
    input_mode = st.radio("Input mode", ["Text", "Voice"], horizontal=True)

    audio = None  # make sure this always exists

    if input_mode == "Text":
        # Use and update session_state so it survives reruns
        st.session_state["user_text"] = st.text_area(
            "How are you feeling today?",
            height=150,
            value=st.session_state["user_text"],
        )

    else:  # Voice mode
        st.write("Press to record your voice, speak, then press again to stop.")
        audio = mic_recorder(
            start_prompt="🎙️ Start recording",
            stop_prompt="⏹️ Stop",
            key="voice_recorder",
            format="wav",
            just_once=True,
        )

        if audio is not None:
            st.info("Processing your audio...")
            text_from_audio = transcribe_audio_bytes(audio["bytes"])

            if text_from_audio.startswith("[speech recognition error"):
                st.error(text_from_audio)
            elif text_from_audio == "":
                st.warning(
                    "I couldn’t understand that. Please try speaking a bit clearer or closer to the mic."
                )
            else:
                st.success("Transcription:")
                st.write(f"“{text_from_audio}”")
                # Store in session so it stays for the button click
                st.session_state["user_text"] = text_from_audio

    # Show current captured text (helps in voice mode)
    if st.session_state["user_text"]:
        st.markdown("**Current input:**")
        st.write(st.session_state["user_text"])

    # Optional: let user choose if they want audio response
    play_audio = st.checkbox("Play coach response as audio", value=False)

    # Use the persisted text
    user_text = st.session_state["user_text"]

    if st.button("Reflect & Get Goals"):
        if not user_text or not user_text.strip():
            st.warning("Please provide what you feel (text or voice) before continuing.")
        else:
            with st.spinner("Analyzing your emotion..."):
                emotion = emotion_model.predict_emotion(user_text)
                goals = suggest_goals(emotion, num_goals=2)
                response = build_coach_response(user_text, emotion, goals)

            st.markdown("### Coach Response")
            st.markdown(response)

            # If user wants voice output
            if play_audio:
                audio_file = text_to_speech(response)
                if audio_file:
                    st.audio(audio_file, format="audio/mp3")

            # Save interaction + goals
            append_history(user_text, emotion, goals)

    # ---------- History & analytics sections ----------

    history = load_history()

    # ---- Recent check-ins table ----
    st.subheader("📈 Your Recent Check-ins")
    if not history.empty:
        st.dataframe(history.tail(15))
    else:
        st.write("No history yet. Your check-ins will appear here.")

    # ---- Mood overview (last 7 days) ----
    st.subheader("📊 Mood Overview (last 7 days)")
    if not history.empty:
        history["timestamp"] = pd.to_datetime(history["timestamp"], errors="coerce")
        last_week = history[
            history["timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=7)
        ]
        if not last_week.empty:
            mood_counts = last_week["emotion"].value_counts()
            st.bar_chart(mood_counts)
        else:
            st.write("No data for the last 7 days yet.")
    else:
        st.write("No mood data yet.")

    # ---- Goal completion UI ----
    st.subheader("✅ Goal Completion")
    if not history.empty:
        # Safety: older files might not have this column
        if "completed" not in history.columns:
            history["completed"] = False

        pending = history[history["completed"] == False]
        if not pending.empty:
            st.write("Select the goals you’ve completed:")

            # Use row index as ID
            selected_indices = st.multiselect(
                "Pending goals:",
                options=list(pending.index),
                format_func=lambda idx: (
                    f"{pending.loc[idx, 'goal']} "
                    f"(from {str(pending.loc[idx, 'timestamp'])[:16]})"
                ),
            )

            if st.button("Mark selected as completed"):
                history.loc[selected_indices, "completed"] = True
                save_history(history)
                st.success(
                    "Nice work. Goals marked as completed. "
                    "Reload the page to see the updated status."
                )
        else:
            st.write("You have no pending goals. Great job!")
    else:
        st.write("No goals logged yet.")

if __name__ == "__main__":
    main()

