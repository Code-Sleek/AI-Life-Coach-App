# chat_logic.py

from typing import List
import textwrap
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi3"  # or "llama3", etc.

def _call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[LLM error: {e}]"

def _shorten(text: str, max_words: int = 90) -> str:
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + "..."

def build_coach_response(user_text: str, emotion: str, goals: List[str]) -> str:
    """
    Build a coaching message using a local LLM via Ollama.
    Tone: energetic, productive, concise.
    """
    goals_text = "\n".join([f"- {g}" for g in goals])

    prompt = textwrap.dedent(f"""
    You are an upbeat, energetic, productivity-focused life coach (not a therapist).

    Context:
    - Detected emotion: {emotion}
    - Suggested small, realistic goals:
    {goals_text}

    User's message:
    \"\"\"{user_text}\"\"\"

    Write a very short response with this exact structure:
    1) One short sentence acknowledging how they feel (no more than 20 words).
    2) Then two bullet points, each a specific, practical action using or adapting the suggested goals.
    3) One final short motivational sentence encouraging them to take action now.

    Style rules:
    - Max 80 words total.
    - Sound energetic and optimistic.
    - Focus on action and productivity, not therapy or deep emotions.
    - No long explanations, no disclaimers, no emojis.
    """)

    llm_response = _call_ollama(prompt)

    if llm_response.startswith("[LLM error:"):
        # Fallback template if LLM fails
        fallback = (
            f"I hear you. It sounds like you’re feeling **{emotion}** right now.\n\n"
            f"Here are two quick actions you can try:\n"
            f"{goals_text}\n\n"
            "Pick one and start now—small steps create momentum."
        )
        return fallback + f"\n\n*(Local LLM is currently unavailable: {llm_response})*"

    return _shorten(llm_response, max_words=90)
