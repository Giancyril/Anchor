from typing import List, Dict, Any

class CannedResponseSuggester:
    """
    Generates tailored, empathetic canned response drafts for human support agents.
    """
    TEMPLATES = {
        "Billing & Invoicing": [
            "Hi there! I'd be happy to assist with your refund. I see you're within our eligibility window. I've initiated the review with our finance team.",
            "Thanks for reaching out regarding your invoice. Could you confirm the last 4 digits of your payment card so I can verify the charge?",
            "I understand you have billing questions. I have verified your account and our pro-rated refund policy applies here.",
        ],
        "Churn & Cancellation Risk": [
            "I'm truly sorry to hear you're considering canceling. Before you go, could I help resolve the issue you ran into, or offer a complimentary extension?",
            "We value your business and understand your frustration. I'd love the opportunity to make things right directly.",
            "I have paused your upcoming billing renewal while we work through this together.",
        ],
        "Technical & Troubleshooting": [
            "Thanks for reporting this issue! Could you try revoking and re-authenticating your integration in Settings > Integrations?",
            "I've escalated this sync error directly to our on-call engineering team and will follow up within 30 minutes.",
            "Please clear your browser cache or try an incognito window, and let me know if the login prompt appears.",
        ],
    }

    def suggest(self, intent: str, customer_query: str) -> List[str]:
        suggestions = self.TEMPLATES.get(intent)
        if not suggestions:
            suggestions = [
                "Hello! Thank you for contacting our priority support team. I'm reviewing your inquiry now.",
                "I apologize for the inconvenience. Let me take care of this for you right away.",
                "Thanks for your patience. I've reviewed your request and am ready to assist.",
            ]
        return suggestions

canned_suggester = CannedResponseSuggester()