# emotion_model.py

from transformers import pipeline

class EmotionModel:
    def __init__(self):
        # Simple text-classification pipeline; you can later swap this
        # for a more specific emotion model (e.g., a fine-tuned RoBERTa)
        self.classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=1
        )

    def predict_emotion(self, text: str) -> str:
        if not text or text.strip() == "":
            return "neutral"

        result = self.classifier(text)[0][0]
        # result is something like {'label': 'joy', 'score': 0.95}
        return result["label"]
