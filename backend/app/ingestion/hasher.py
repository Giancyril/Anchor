import hashlib


def generate_vector_id(document_id: str, section: str, chunk_index: int) -> str:
    """
    Generate a deterministic, collision-resistant vector ID.
    Format: SHA256(document_id + '::' + section + '::' + str(chunk_index))[:32]

    This ensures re-ingesting the same document always produces the same IDs,
    enabling safe upserts (overwrite) in Pinecone without creating duplicates.
    """
    raw = f"{document_id}::{section}::{chunk_index}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]
