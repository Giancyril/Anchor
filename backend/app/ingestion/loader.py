import os
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    BSHTMLLoader,
)
from langchain_core.documents import Document

SUPPORTED_FORMATS = {".md", ".txt", ".pdf", ".html", ".htm"}


def load_document(file_path: str) -> List[Document]:
    """
    Load a document from disk based on its file extension.
    Returns a list of LangChain Document objects.
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format '{ext}'. "
            f"Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    if ext in (".md", ".txt"):
        loader = TextLoader(file_path, autodetect_encoding=True)
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in (".html", ".htm"):
        loader = BSHTMLLoader(file_path, open_encoding="utf-8")
    else:
        loader = TextLoader(file_path, autodetect_encoding=True)

    return loader.load()