import os
from langchain_core.documents import Document
from app.ingestion.chunker import chunk_documents, extract_section_heading
from app.ingestion.loader import load_document


def test_extract_section_heading():
    md = "# Billing Policy\nHere is text."
    assert extract_section_heading(md) == "Billing Policy"

    plain = "No heading here at all."
    assert extract_section_heading(plain) == "General"


def test_chunk_documents_metadata_enrichment():
    raw_doc = Document(page_content="# Terms\nThis is a sample document content. " * 30)
    chunks = chunk_documents(
        documents=[raw_doc],
        document_id="doc_test_1",
        document_name="Terms.md",
        url="https://docs.company.com/terms",
        category="Legal",
    )
    assert len(chunks) > 1
    for idx, c in enumerate(chunks):
        assert c.metadata["source_id"] == "doc_test_1"
        assert c.metadata["document_name"] == "Terms.md"
        assert c.metadata["url"] == "https://docs.company.com/terms"
        assert c.metadata["category"] == "Legal"
        assert c.metadata["chunk_index"] == idx
        assert c.metadata["total_chunks"] == len(chunks)


def test_loader_sample_markdown():
    path = "backend/sample_docs/billing_refund_policy.md"
    if os.path.exists(path):
        docs = load_document(path)
        assert len(docs) > 0
        assert "Refund" in docs[0].page_content