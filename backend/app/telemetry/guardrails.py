import re
from typing import Dict, Any, Tuple, List

class SafetyGuardrails:
    """
    Sanitizes user input and output text, redacting sensitive PII and blocking jailbreak attempts.
    """
    # Regex patterns for sensitive PII
    PATTERNS = {
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "API_KEY": r"\b(?:sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16})\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    }

    INJECTION_SIGNALS = [
        "ignore all previous instructions",
        "system prompt",
        "reveal your instructions",
        "disregard previous directives",
        "you are now in developer mode",
        "jailbreak",
        "bypass rules",
    ]

    def sanitize_text(self, text: str) -> Tuple[str, List[str]]:
        """Redacts PII tokens from text and returns list of redacted entity types."""
        sanitized = text
        redacted_types = []

        for p_name, pattern in self.PATTERNS.items():
            if re.search(pattern, sanitized):
                redacted_types.append(p_name)
                sanitized = re.sub(pattern, f"[REDACTED_{p_name}]", sanitized)

        return sanitized, redacted_types

    def check_prompt_injection(self, text: str) -> Dict[str, Any]:
        """Detects adversarial injection attacks."""
        t_low = text.lower()
        flagged = []
        for signal in self.INJECTION_SIGNALS:
            if signal in t_low:
                flagged.append(signal)

        is_safe = len(flagged) == 0
        return {
            "is_safe": is_safe,
            "flagged_signals": flagged,
            "action": "allow" if is_safe else "block",
        }

safety_guardrails = SafetyGuardrails()