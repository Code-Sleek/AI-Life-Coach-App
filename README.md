# 🧠 AI Life Coach: Emotion-Aware Goal Setter  

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-000000.svg?logo=ollama&logoColor=white)](https://ollama.com/)
[![Transformers](https://img.shields.io/badge/Hugging%20Face-Transformers-FFCC4D.svg?logo=huggingface&logoColor=black)](https://huggingface.co/docs/transformers/index)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

An AI-powered **life coach app** that turns how you *feel* into **small, actionable goals** – with:

- Emotion detection from text *or* voice  
- Local LLM coaching responses (no cloud API keys)  
- Optional voice replies from the coach  
- Mood history and goals tracking

---

## 💡 What the App Does

The app acts as a lightweight “AI Life Coach”:

1. You check in by **typing** or **speaking** how you feel.
2. The app:
   - Detects your **emotion** using an NLP model.
   - Suggests **small, realistic goals** tailored to that emotion.
   - Uses a **local LLM (phi3 via Ollama)** to respond in an energetic, encouraging tone.
3. Your check-ins, emotions and goals are logged so you can:
   - See **recent check-ins**  
   - Monitor your **mood over the last 7 days**  
   - Mark goals as **completed**

This is **not** a therapy tool; it’s a productivity- and self-improvement-oriented assistant.

---

## ✨ Features

- **📝 Dual Input Modes**
  - Text input (type how you feel)
  - Voice input using microphone (speech → text)

- **🎯 Emotion-Aware Goal Suggestions**
  - Uses a transformers-based emotion classifier
  - Maps emotions (e.g., sadness, joy, anger, fear, neutral) to **practical mini-goals**

- **🤖 Local LLM Coaching (Ollama + phi3)**
  - Uses a local LLM (e.g. `phi3` via Ollama)
  - Short, energetic, productivity-focused responses
  - No external cloud LLM needed while running locally

- **🔊 Voice Response (Text-to-Speech)**
  - Optional: convert the coach’s reply to audio
  - Hear your coach’s message instead of only reading it

- **📈 Mood & Goal Tracking**
  - Logs each interaction to `data/history.csv`
  - Recent check-ins table
  - Mood distribution chart for the last 7 days
  - Goal completion view with checkboxes

- **🧱 Modular Architecture**
  - `emotion_model.py` – emotion detection
  - `goal_generator.py` – rule-based goal recommender
  - `chat_logic.py` – LLM-powered coach response
  - `app.py` – Streamlit UI + orchestration

---

## 🛠 Tech Stack & Tools

**Language & Core**

- Python 3.9+
- Streamlit (web UI)

**AI / NLP**

- `transformers` (Hugging Face) for emotion classification  
- Local LLM via **Ollama** (e.g. `phi3`, `llama3`, etc.)

**Voice & Audio**

- `SpeechRecognition` – speech → text (Google Web Speech API)
- `streamlit-mic-recorder` – microphone capture in Streamlit
- `gTTS` – text → speech (MP3 audio)

**Data & Visualization**

- `pandas` – interaction history & stats
- `matplotlib` / Streamlit charts – mood overview

**Other**

- `requests` – HTTP calls to Ollama API
- `torch` – backend for transformers model

---

## 📁 Project Structure

```text
ai_life_coach/
├── app.py                 # Main Streamlit app
├── emotion_model.py       # Emotion classifier wrapper
├── goal_generator.py      # Emotion → goals mapping logic
├── chat_logic.py          # LLM-based coach response (Ollama)
├── requirements.txt       # Python dependencies
├── data/
│   └── history.csv        # Runtime history log (auto-created)
└── README.md
```
## 🚀 Quick Start: How to Run the App

### 1️⃣ Prerequisites

You need:

- **Python 3.9+**
- **Git** (optional, for cloning)
- **Ollama** (for running the local LLM)
- A machine running **Windows, macOS, or Linux**

#### Install Ollama

1. Download from: https://ollama.com  
2. Install and open Ollama (it runs as a background service).
3. Pull a model you want to use (example: `phi3`):

   ```bash
   ollama pull phi3

### 2️⃣ Get the Project Code

Option A – Using Git (recommended)
   ```bash

   git clone https://github.com/YOUR_USERNAME/ai-life-coach.git
   cd ai-life-coach
   ```

Option B – Download ZIP

1. Go to your GitHub repository page.

2. Click “Code” → “Download ZIP”.

3. Extract the ZIP and open a terminal/command prompt inside the extracted folder

### 3️⃣ Create and Activate a Virtual Environment

This keeps dependencies isolated.


#### Windows (PowerShell or CMD)
   ```bash

   python -m venv venv
   venv\Scripts\activate
   ```

#### macOS / Linux (bash/zsh)
   ```bash

   python3 -m venv venv
   source venv/bin/activate
   ```

You should see (venv) in your terminal prompt after activation.

### 4️⃣ Install Dependencies

With the virtual environment active, run:

```bash

pip install -r requirements.txt
```

This installs:

- streamlit
- pandas
- transformers
- torch
- requests
- SpeechRecognition
- gTTS
- streamlit-mic-recorder
- pydub

and other needed packages

### 5️⃣ Ensure Ollama is Running

Make sure the Ollama service/app is running in the background and that you pulled a model:
```bash
ollama pull phi3
```

| If you change the model name in chat_logic.py (e.g., to llama3), make sure you also ollama pull llama3.

### 6️⃣ Run the Streamlit App

From the project root:

```bash
streamlit run app.py
```

Streamlit will open a browser window (or give you a local URL such as):
```
http://localhost:8501
```

If it does not open automatically, copy the URL from the terminal into your browser.

### 7️⃣ Using the App

1.  Choose Input Mode

- Text: Type how you feel in the text area.
- Voice: Use the microphone button to record your voice; the app will transcribe it to text.

2. Optional: Audio Response

- Tick “Play coach response as audio” if you want to hear the coach reply using TTS.

3. Click “Reflect & Get Goals”

The app:
- Detects your emotion
- Generates 1–2 small goals
- Uses the local LLM (phi3) to create a short, energetic response

4. Scroll down to:

📈 Recent Check-ins – see your latest entries.

📊 Mood Overview (last 7 days) – bar chart of emotions.

✅ Goal Completion – mark goals as done using checkboxes.

---

### ⚠️ Notes & Limitations

This app is not a substitute for professional mental health support.

Speech recognition relies on the Google Web Speech API, so:
- It requires internet access.
- Accuracy depends on audio quality, accent, background noise, etc.

LLM responses depend on:
- The model you choose in Ollama (phi3, llama3, etc.)
- The prompt defined in chat_logic.py.

---
