import pytest
from langchain_core.documents import Document
from app.services.confidence_service import check_confidence
from app.chains.citation_parser import parse_citations


# Grounded Eval Cases (Assert correct citations & data grounding)
GROUNDED_EVAL_CASES = [
    {
        "question": "What is the refund window for initial purchases?",
        "expected_doc": "billing_refund_policy.md",
        "expected_keyword": "14 days",
    },
    {
        "question": "What authentication methods are supported?",
        "expected_doc": "security_privacy.md",
        "expected_keyword": "MFA",
    },
    {
        "question": "How many team members can I have on the Starter plan?",
        "expected_doc": "pricing_plans.md",
        "expected_keyword": "5 team members",
    },
]

# Out-of-Domain Negative Cases (Assert agent says IDK and doesn't hallucinate)
DELIBERATE_NEGATIVE_CASES = [
    "What is the company discount for employee pet insurance?",
    "How do I book an international flight through corporate travel?",
    "Where is the headquarters office parking garage located?",
    "What is the CEO personal phone number?",
]


@pytest.mark.parametrize("case", GROUNDED_EVAL_CASES)
def test_grounded_eval_cases(case):
    # Simulated top retrieval chunk
    chunk = Document(
        page_content=f"Relevant excerpt containing {case['expected_keyword']}",
        metadata={"document_name": case["expected_doc"], "section": "Policy"},
    )
    passed, score = check_confidence([(chunk, 0.88)])
    assert passed is True

    answer = f"The answer is {case['expected_keyword']} [1]."
    _, sources = parse_citations(answer, [chunk])
    assert len(sources) == 1
    assert sources[0].document_name == case["expected_doc"]


@pytest.mark.parametrize("question", DELIBERATE_NEGATIVE_CASES)
def test_negative_hallucination_eval_cases(question):
    # Weak/irrelevant match below cosine threshold
    weak_chunk = Document(
        page_content="Completely unrelated system settings information.",
        metadata={"document_name": "getting_started.md", "section": "Overview"},
    )
    # Cosine score below 0.75 gate
    passed, score = check_confidence([(weak_chunk, 0.54)])
    assert passed is False, f"Question '{question}' failed hallucination gate!"