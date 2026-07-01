"""
Purpose: Orchestrating the semantic similarity search and exposing the primary public interface.
"""
import logging
from typing import Any, Dict, List
from rag.embeddings import PolicyEmbeddingEngine
from rag.vector_store import PolicyVectorStore

logger = logging.getLogger("rag.retriever")

def retrieve_policy_matches(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Runs the semantic similarity search and returns the raw matched chunk records
    (text + metadata), so callers can build both the LLM prompt context and
    display-ready citations from the same real retrieval results.

    Args:
        query (str): Natural language operational string tracking investigator search context.
        top_k (int): Threshold tracking maximum density count configurations.

    Returns:
        List[Dict[str, Any]]: Matched records, each with "text" and "metadata" keys.
    """
    logger.info("Retrieving policy context")

    if not query or not query.strip():
        return []

    try:
        vector_agent = PolicyEmbeddingEngine()
        query_vector = vector_agent.generate_single_embedding(query.strip())

        storage_engine = PolicyVectorStore()
        matched_records = storage_engine.query_nearest_neighbors(query_vector, top_k=top_k)

        logger.info(f"Retrieved {len(matched_records)} matching policy sections")
        return matched_records

    except Exception as general_retrieval_fault:
        logger.warning(f"Retrieval interface swallowed internal workflow exception tracking error: {str(general_retrieval_fault)}")
        # Safeguard fallback to prevent downstream operational backend crashes
        return []

def format_policy_context(matched_records: List[Dict[str, Any]]) -> str:
    """Compiles matched records into the multi-line text block fed to the LLM prompt."""
    if not matched_records:
        return ""

    string_builder = []
    for record in matched_records:
        meta = record["metadata"]
        header = f"{meta['policy_name']} ({meta['policy_id']})\n{meta['section']}"
        body_content = record["text"].strip()
        string_builder.append(f"{header}\n\n{body_content}\n")

    return "\n".join(string_builder).strip()

def format_policy_citations(matched_records: List[Dict[str, Any]]) -> List[str]:
    """Formats matched records into display citations using the real source file, e.g. 'fraud_policy.pdf - Segment Section 2'."""
    return [
        f"{r['metadata']['source_file']} - {r['metadata']['section']}"
        for r in matched_records
    ]

def retrieve_policy_context(query: str, top_k: int = 3) -> str:
    """
    Backwards-compatible wrapper exposing the primary entry point for callers that
    only need the text context (e.g. the LLM prompt), not the structured citations.
    """
    return format_policy_context(retrieve_policy_matches(query, top_k=top_k))
