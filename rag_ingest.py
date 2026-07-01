"""
Purpose: One-click extraction workflow script to parse PDF files and fully populate ChromaDB.
Save as: root directory 'rag_ingest.py'
"""
import logging
from rag.loader import PolicyDocumentLoader
from rag.embeddings import PolicyEmbeddingEngine
from rag.vector_store import PolicyVectorStore

logger = logging.getLogger("rag_ingest")

def ingest_policies() -> int:
    """Reads every policy PDF, embeds it, and upserts it into the vector store.
    Record ids are deterministic (see PolicyVectorStore.upsert_policy_records), so this is
    safe to call repeatedly - re-running it just overwrites the same records. Returns the
    number of chunks ingested."""
    loader = PolicyDocumentLoader()
    chunks = loader.read_and_chunk_policies()
    if not chunks:
        logger.warning("No policy PDF documents found inside 'policies/' folder.")
        return 0

    texts_only = [item["text"] for item in chunks]
    engine = PolicyEmbeddingEngine()
    vectors = engine.generate_batch_embeddings(texts_only)

    store = PolicyVectorStore()
    store.upsert_policy_records(chunks, vectors)
    return len(chunks)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    print("=== INITIATING FRAUD CO-PILOT POLICY DATA INDEXING INGESTION ===")

    chunk_count = ingest_policies()

    if not chunk_count:
        print("[-] Verification failed: No policy PDF documents found inside 'policies/' folder.")
        exit(1)

    print(f"\n=== SUCCESS: DATABASE POPULATED WITH {chunk_count} CHUNKS AND READY TO WORK ===")
