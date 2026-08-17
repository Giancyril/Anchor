from app.ingestion.hasher import generate_vector_id


def test_deterministic_vector_id_consistency():
    id1 = generate_vector_id("doc_123", "Refund Eligibility", 0)
    id2 = generate_vector_id("doc_123", "Refund Eligibility", 0)
    assert id1 == id2
    assert len(id1) == 32


def test_deterministic_vector_id_uniqueness():
    id1 = generate_vector_id("doc_123", "Refund Eligibility", 0)
    id2 = generate_vector_id("doc_123", "Refund Eligibility", 1)
    id3 = generate_vector_id("doc_456", "Refund Eligibility", 0)
    assert id1 != id2
    assert id1 != id3