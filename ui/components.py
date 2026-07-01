"""
Purpose: Structuring metrics loaders, rendering widgets, and abstracting data parsing frameworks.
"""
import json
import logging
import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple

logger = logging.getLogger("ui.components")

ANALYST_NAME = "Sr Fraud Investigator"
FRAUD_MANAGER_NAME = "Fraud Manager"
ANALYST_LOCATION = "Wilmington, DE"

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
            {"<div style='color:var(--color-primary-dark); font-size:0.85rem; font-weight:500;'>" + delta_status + "</div>" if delta_status else ""}
        </div>
    """, unsafe_allow_html=True)

def render_kpi_row(items: List[Tuple[str, Any]]) -> None:
    """Renders a row of equal-width metric cards from (label, value) pairs. Reused across
    the Work Queue, Analytics, and Business Impact sections."""
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            render_metric_card(label, value)

def render_system_status_panel(checks: List[Tuple[str, bool]], last_refreshed: str) -> None:
    """Renders a multi-row system health panel (one row per check) with a last-refreshed footer."""
    rows = []
    for label, ok in checks:
        dot_class = "ok" if ok else "down"
        row_class = "status-row" if ok else "status-row down"
        text = label if ok else f"{label} — Unavailable"
        rows.append(f'<div class="{row_class}"><span class="status-dot {dot_class}"></span>{text}</div>')
    st.markdown(f"""
        <div class="status-panel">
            {"".join(rows)}
            <div class="status-panel-footer">Last refreshed {last_refreshed}</div>
        </div>
    """, unsafe_allow_html=True)

def badge_html(label: str, variant: str) -> str:
    """Returns a colored status/priority pill span. Variant must match a .badge-<variant> CSS class
    (high, medium, low, neutral, approved, declined, escalated, review, returned, closed)."""
    return f'<span class="badge badge-{variant}">{label}</span>'

def tier_variant(tier: Optional[str]) -> str:
    """Maps a free-text risk/priority label to its badge color variant."""
    return {"high": "high", "medium": "medium", "low": "low"}.get((tier or "").strip().lower(), "neutral")

def case_status_variant(status_label: str) -> str:
    """Maps a case's derived status label to its badge color variant."""
    return {
        "approved": "approved",
        "declined": "declined",
        "escalated": "escalated",
        "under review": "review",
        "closed": "closed",
        "returned": "returned",
    }.get(status_label.strip().lower(), "neutral")

def render_decision_record(decision: str, notes: str, actor: str, timestamp: str) -> None:
    """Renders a locked decision record: a badge, the rationale notes, and who/when.
    Shared by the analyst's disposition and the Fraud Manager's approval decision."""
    st.markdown(f"""
        <div class="decision-record">
            {badge_html(decision, case_status_variant(decision))}
            <div class="decision-record-note">{notes}</div>
            <div class="decision-record-meta">Reviewed by {actor} · {timestamp}</div>
        </div>
    """, unsafe_allow_html=True)

CASE_FLOW_STAGES = ["Open", "Under Review", "Waiting for Approval", "Closed"]

def _flow_stage_index(status_label: str) -> int:
    """Maps a case's derived status to its position in the lifecycle flow.
    A submitted analyst disposition (Approved/Declined/Escalated) moves the case to
    'Waiting for Approval' rather than 'Closed' - it isn't final until a Fraud Manager
    signs off, which isn't built yet."""
    status = status_label.strip().lower()
    if status == "new":
        return 0
    if status == "under review":
        return 1
    if status in ("approved", "declined", "escalated"):
        return 2
    if status == "closed":
        return 3
    return 0

def render_case_flow(status_label: str) -> None:
    """Renders the case lifecycle stepper: Open -> Under Review -> Waiting for Approval -> Closed,
    highlighting the case's current stage."""
    current_index = _flow_stage_index(status_label)
    parts = ['<div class="flow-stepper">']
    for i, stage in enumerate(CASE_FLOW_STAGES):
        state = "done" if i < current_index else ("current" if i == current_index else "")
        parts.append(f'<div class="flow-step {state}"><div class="flow-dot"></div><div class="flow-label">{stage}</div></div>')
        if i < len(CASE_FLOW_STAGES) - 1:
            connector_state = "done" if i < current_index else ""
            parts.append(f'<div class="flow-connector {connector_state}"></div>')
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)

def resolve_case_id(c: Dict[str, Any], idx: int) -> str:
    """Resolves a stable ID for a case record, regardless of nested vs. flat structure.
    Used everywhere a case is identified (queue rows, selectors, lookups) so different views
    can never disagree on what a given case's ID is."""
    tid = c.get("transaction_id")
    if not tid and isinstance(c.get("transaction"), dict):
        tid = c["transaction"].get("transaction_id")
    if not tid:
        tid = c.get("case_id") or c.get("id") or f"CASE-TICKET-{idx+1:03d}"
    return str(tid)

def parse_cases_dataframe(cases: List[Dict[str, Any]]) -> pd.DataFrame:
    """Transforms raw record collections directly into standard tracking dataframes adaptively."""
    flattened_rows = []
    for idx, c in enumerate(cases):
        # 1. Adaptively isolate the transaction dataset block (handles nested or flat root)
        if "transaction" in c and isinstance(c["transaction"], dict):
            txn = c["transaction"]
            hist = c.get("customer_history", {})
        else:
            txn = c
            hist = c.get("customer_history") or c

        case_id = resolve_case_id(c, idx)
        customer = txn.get("customer_name") or txn.get("customer", "N/A")
        amount = float(txn.get("amount") or 0.0)
        merchant = txn.get("merchant", "N/A")
        location = txn.get("location") or txn.get("transaction_location", "N/A")

        # 3. Extract customer history baselines metrics safely
        avg_spending = float(hist.get("average_transaction") or 0.0)
        past_fraud = int(hist.get("previous_fraud_cases") or 0)

        flattened_rows.append({
            "case_id": case_id,
            "customer": customer,
            "amount": amount,
            "merchant": merchant,
            "location": location,
            "avg_spending": avg_spending,
            "past_fraud": past_fraud,
            "priority": c.get("priority", "N/A"),
            "case_status": c.get("case_status", "New"),
            "created_date": c.get("created_date", "N/A"),
        })

    return pd.DataFrame(flattened_rows)

