# goal_generator.py

import random

GOALS_BY_EMOTION = {
    "sadness": [
        "Write down 3 things you’re grateful for.",
        "Send a supportive message to a friend.",
        "Listen to a song that usually lifts your mood."
    ],
    "joy": [
        "Capture this feeling: journal 3 good things that happened today.",
        "Share something positive with someone you care about.",
        "Plan a small reward for yourself later this week."
    ],
    "anger": [
        "Take 10 deep breaths, slowly.",
        "Go for a brisk 15-minute walk.",
        "Write down what’s bothering you, then list what you can control."
    ],
    "fear": [
        "Write down the specific worry and a tiny step to reduce it.",
        "Do a 5-minute grounding exercise (notice 5 things you can see).",
        "Talk to someone you trust about what’s worrying you."
    ],
    "neutral": [
        "Choose one small task you’ve been postponing and complete it.",
        "Review your goals for the week and pick one easy win.",
        "Spend 10 minutes tidying your workspace."
    ]
}

def suggest_goals(emotion: str, num_goals: int = 2):
    emotion = emotion.lower()
    # Use neutral as a fallback
    if emotion not in GOALS_BY_EMOTION:
        emotion = "neutral"

    options = GOALS_BY_EMOTION[emotion]
    if num_goals >= len(options):
        return options
    return random.sample(options, num_goals)
