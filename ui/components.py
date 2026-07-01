"""
Purpose: Structuring metrics loaders, rendering widgets, and abstracting data parsing frameworks.
"""
import json
import logging
import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional

logger = logging.getLogger("ui.components")

@st.cache_data
def load_investigation_cases() -> List[Dict[str, Any]]:
    """Loads operational anomalies portfolio logs directly from project data caches."""
    target_path = "sample_data/fraud_investigation_cases.json"
    try:
        with open(target_path, "r", encoding="utf-8") as file_buffer:
            cases_data = json.load(file_buffer)
            logger.info(f"Loaded {len(cases_data)} investigation cases successfully.")
            return cases_data if isinstance(cases_data, list) else []
    except Exception as read_fault:
        logger.error(f"Unable to load investigation cases from context path structure: {str(read_fault)}")
        st.error("Data Infrastructure Error: Failed to ingest active data registers portfolio logs.")
        return []

def render_metric_card(label: str, value: Any, delta_status: Optional[str] = None) -> None:
    """Renders a clean operational dashboard metric block layout."""
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {"<div style='color:#059669; font-size:0.85rem; font-weight:500;'>" + delta_status + "</div>" if delta_status else ""}
        </div>
    """, unsafe_allow_html=True)

def parse_cases_dataframe(cases: List[Dict[str, Any]]) -> pd.DataFrame:
    """Transforms raw record collections directly into standard tracking dataframes."""
    flattened_rows = []
    for c in cases:
        txn = c.get("transaction", {})
        hist = c.get("customer_history", {})
        flattened_rows.append({
            "case_id": txn.get("transaction_id", "N/A"),
            "customer": txn.get("customer_name", "N/A"),
            "amount": txn.get("amount", 0.0),
            "merchant": txn.get("merchant", "N/A"),
            "location": txn.get("location", "N/A"),
            "avg_spending": hist.get("average_transaction", 0.0),
            "past_fraud": hist.get("previous_fraud_cases", 0)
        })
    return pd.DataFrame(flattened_rows)
