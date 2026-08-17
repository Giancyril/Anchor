import math
import re
from typing import List, Dict, Tuple, Any
from langchain_core.documents import Document

class BM25Indexer:
    """
    In-memory BM25 Okapi sparse indexer for exact keyword, SKU, and code token search.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.documents: List[Document] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_length: float = 0.0
        self.inverted_index: Dict[str, Dict[int, int]] = {}  # term -> {doc_idx: freq}
        self.doc_count: int = 0
        self.idf: Dict[str, float] = {}

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Normalize and tokenize alphanumeric words and code symbols."""
        tokens = re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())
        return [t for t in tokens if len(t) > 1]

    def fit(self, documents: List[Document]):
        """Index a collection of LangChain documents."""
        self.documents = documents
        self.doc_count = len(documents)
        self.doc_lengths = []
        self.inverted_index = {}

        if self.doc_count == 0:
            self.avg_doc_length = 0.0
            return

        total_length = 0
        for idx, doc in enumerate(documents):
            tokens = self.tokenize(doc.page_content)
            length = len(tokens)
            self.doc_lengths.append(length)
            total_length += length

            for term in tokens:
                if term not in self.inverted_index:
                    self.inverted_index[term] = {}
                self.inverted_index[term][idx] = self.inverted_index[term].get(idx, 0) + 1

        self.avg_doc_length = total_length / self.doc_count

        # Compute IDF for all indexed terms
        self.idf = {}
        for term, posting in self.inverted_index.items():
            n_t = len(posting)
            # Standard Lucene/BM25 IDF formula
            self.idf[term] = math.log((self.doc_count - n_t + 0.5) / (n_t + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> List[Tuple[Document, float]]:
        """Score and return top-k documents matching query."""
        if not self.documents or self.doc_count == 0:
            return []

        query_tokens = self.tokenize(query)
        scores: Dict[int, float] = {i: 0.0 for i in range(self.doc_count)}

        for term in query_tokens:
            if term not in self.inverted_index:
                continue
            idf = self.idf.get(term, 0.0)
            posting = self.inverted_index[term]

            for doc_idx, freq in posting.items():
                doc_len = self.doc_lengths[doc_idx]
                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * (doc_len / max(1, self.avg_doc_length)))
                scores[doc_idx] += idf * (numerator / denominator)

        # Sort by BM25 score descending
        sorted_indices = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        results = [(self.documents[idx], score) for idx, score in sorted_indices if score > 0]
        return results[:top_k]

# Global singleton instance for in-memory session index
bm25_indexer = BM25Indexer()