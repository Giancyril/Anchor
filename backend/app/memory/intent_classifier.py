from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.config import settings

INTENT_CATEGORIES = [
    "Billing & Invoicing",
    "Technical & Troubleshooting",
    "Security & Privacy",
    "Pricing & Plans",
    "Account & Onboarding",
    "Churn & Cancellation Risk",
    "General Inquiry",
]

class IntentClassifier:
    """
    Classifies incoming customer messages into standard support intent taxonomies.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name

    async def classify(self, text: str) -> str:
        # Rule-based fast heuristics
        t_low = text.lower()
        if any(w in t_low for w in ["cancel", "unsubscribe", "delete my account", "close account"]):
            return "Churn & Cancellation Risk"
        if any(w in t_low for w in ["refund", "invoice", "charge", "receipt", "credit card", "stripe", "billing"]):
            return "Billing & Invoicing"
        if any(w in t_low for w in ["mfa", "saml", "sso", "gdpr", "encrypt", "password", "security"]):
            return "Security & Privacy"
        if any(w in t_low for w in ["pricing", "cost", "pro plan", "starter plan", "enterprise"]):
            return "Pricing & Plans"
        if any(w in t_low for w in ["error", "bug", "sync", "broken", "failed", "login", "not working"]):
            return "Technical & Troubleshooting"

        if not settings.OPENAI_API_KEY:
            return "General Inquiry"

        llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.0,
            openai_api_key=settings.OPENAI_API_KEY,
        )

        categories_str = ", ".join(INTENT_CATEGORIES)
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"You are a customer support triage classifier. Categorize the user message into exactly ONE of these categories: {categories_str}. Output ONLY the category name."),
            ("human", "Message: {text}"),
        ])

        chain = prompt | llm | StrOutputParser()
        try:
            res = await chain.ainvoke({"text": text})
            cleaned = res.strip()
            for cat in INTENT_CATEGORIES:
                if cat.lower() in cleaned.lower():
                    return cat
        except Exception:
            pass

        return "General Inquiry"

intent_classifier = IntentClassifier()