"""
ingest.py — PDF parsing, chunking, embedding, and storing in ChromaDB.
"""

import os
import pdfplumber
import cohere
import chromadb
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "pdf_chunks"
CHUNK_SIZE = 500       # characters
CHUNK_OVERLAP = 50     # characters


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file, page by page."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text


def split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into chunks using recursive character splitting."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Embed a list of text chunks using Cohere embed-english-v3.0."""
    co = cohere.ClientV2(COHERE_API_KEY)
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document",
        embedding_types=["float"],
    )
    return response.embeddings.float_


def store_in_chromadb(chunks: list[str], embeddings: list[list[float]]) -> None:
    """Store chunks and their embeddings in a ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)

    # Delete existing collection if it exists, so each upload is fresh
    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"text": chunk} for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )


def ingest_pdf(pdf_path: str) -> int:
    """
    Full ingest pipeline: parse PDF → chunk → embed → store.
    Returns the number of chunks stored.
    """
    text = extract_text_from_pdf(pdf_path)
    if not text.strip():
        raise ValueError("No text could be extracted from the PDF.")

    chunks = split_text_into_chunks(text)
    embeddings = embed_chunks(chunks)
    store_in_chromadb(chunks, embeddings)

    return len(chunks)
