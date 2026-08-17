import difflib
from typing import List, Dict, Tuple, Any
from langchain_core.documents import Document

class ChunkDiffResult:
    def __init__(self, added: List[Document], modified: List[Tuple[Document, Document]], removed: List[Document]):
        self.added = added
        self.modified = modified
        self.removed = removed

    def to_dict(self) -> Dict[str, Any]:
        return {
            "added_count": len(self.added),
            "modified_count": len(self.modified),
            "removed_count": len(self.removed),
            "total_changes": len(self.added) + len(self.modified) + len(self.removed),
        }

class DocumentDiffEngine:
    """
    Computes structural differences between old and new document chunk collections.
    """
    @staticmethod
    def compute_diff(old_chunks: List[Document], new_chunks: List[Document]) -> ChunkDiffResult:
        old_map = {c.metadata.get("section", f"chunk_{i}"): c for i, c in enumerate(old_chunks)}
        new_map = {c.metadata.get("section", f"chunk_{i}"): c for i, c in enumerate(new_chunks)}

        added = []
        modified = []
        removed = []

        # Find new & modified
        for sec, new_doc in new_map.items():
            if sec not in old_map:
                added.append(new_doc)
            else:
                old_doc = old_map[sec]
                if old_doc.page_content.strip() != new_doc.page_content.strip():
                    modified.append((old_doc, new_doc))

        # Find removed
        for sec, old_doc in old_map.items():
            if sec not in new_map:
                removed.append(old_doc)

        return ChunkDiffResult(added=added, modified=modified, removed=removed)

    @staticmethod
    def generate_unified_diff(old_text: str, new_text: str) -> str:
        diff_lines = difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile="v_previous",
            tofile="v_current",
        )
        return "".join(diff_lines)

diff_engine = DocumentDiffEngine()