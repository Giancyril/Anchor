from langchain_core.documents import Document
from app.chains.citation_parser import parse_citations


def test_parse_single_citation():
    chunks = [
        Document(page_content="Full refunds within 14 days.", metadata={"document_name": "Billing.md", "section": "Refunds", "url": "https://example.com"}),
    ]
    answer = "You are eligible for a refund within 14 days [1]."
    clean_text, sources = parse_citations(answer, chunks)

    assert len(sources) == 1
    assert sources[0].citation_index == 1
    assert sources[0].document_name == "Billing.md"
    assert sources[0].section == "Refunds"
    assert sources[0].url == "https://example.com"


def test_parse_multiple_citations_and_deduplicate():
    chunks = [
        Document(page_content="Doc 1 text", metadata={"document_name": "Doc1.md", "section": "Sec1"}),
        Document(page_content="Doc 2 text", metadata={"document_name": "Doc2.md", "section": "Sec2"}),
    ]
    answer = "First point [1] and second point [2], also repeated [1]."
    clean_text, sources = parse_citations(answer, chunks)

    assert len(sources) == 2
    assert [s.citation_index for s in sources] == [1, 2]


def test_parse_out_of_bounds_citation_gracefully():
    chunks = [
        Document(page_content="Doc 1 text", metadata={"document_name": "Doc1.md", "section": "Sec1"}),
    ]
    answer = "Claim with invalid citation [99]."
    clean_text, sources = parse_citations(answer, chunks)
    assert len(sources) == 0