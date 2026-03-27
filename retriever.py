"""
retriever.py — Query embedding and ChromaDB similarity search.
"""

import os
import cohere
import chromadb
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CHROMA_DB_DIR = "./chroma_db"
COLLECTION_NAME = "pdf_chunks"
TOP_K = 5


def embed_query(query: str) -> list[float]:
    """Embed a user query using Cohere embed-english-v3.0."""
    co = cohere.ClientV2(COHERE_API_KEY)
    response = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query",
        embedding_types=["float"],
    )
    return response.embeddings.float_[0]


def retrieve_relevant_chunks(query: str, top_k: int = TOP_K) -> list[str]:
    """
    Embed the query and retrieve the top-k most similar chunks from ChromaDB.
    Returns a list of chunk texts.
    """
    query_embedding = embed_query(query)

    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    # results["documents"] is a list of lists; we want the first (and only) list
    return results["documents"][0] if results["documents"] else []
