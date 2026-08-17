from langchain_core.documents import Document
from app.services.confidence_service import check_confidence


def test_confidence_gate_passes_above_threshold():
    doc = Document(page_content="Relevant content", metadata={})
    passed, score = check_confidence([(doc, 0.85)])
    assert passed is True
    assert score == 0.85


def test_confidence_gate_rejects_below_threshold():
    doc = Document(page_content="Irrelevant text", metadata={})
    passed, score = check_confidence([(doc, 0.62)])
    assert passed is False
    assert score == 0.62


def test_confidence_gate_empty_results():
    passed, score = check_confidence([])
    assert passed is False
    assert score == 0.0