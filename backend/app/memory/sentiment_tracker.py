from typing import List, Dict, Any

class SentimentTracker:
    """
    Performs per-turn sentiment scoring and tracks frustration dips across conversation turns.
    """
    NEGATIVE_KEYWORDS = [
        "angry", "frustrated", "ridiculous", "terrible", "worst", "unacceptable",
        "broken", "waste of time", "scam", "lawyer", "refund immediately", "disaster"
    ]
    POSITIVE_KEYWORDS = [
        "thank", "thanks", "great", "helpful", "perfect", "awesome", "appreciate", "good"
    ]

    def analyze(self, text: str) -> Dict[str, Any]:
        t_low = text.lower()
        neg_count = sum(1 for w in self.NEGATIVE_KEYWORDS if w in t_low)
        pos_count = sum(1 for w in self.POSITIVE_KEYWORDS if w in t_low)

        if "!" in text and neg_count > 0:
            sentiment = "Urgent / Frustrated"
            score = -0.8
        elif neg_count > 0:
            sentiment = "Frustrated"
            score = -0.5
        elif pos_count > 0:
            sentiment = "Satisfied"
            score = 0.8
        else:
            sentiment = "Neutral"
            score = 0.0

        return {
            "sentiment": sentiment,
            "score": score,
            "requires_human_attention": score < -0.4,
        }

sentiment_tracker = SentimentTracker()