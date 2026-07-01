"""
Purpose: Assembling main dashboard view configurations, interaction workflows, and charts.
"""
from datetime import datetime
import logging
import streamlit as st
from ui.components import (
    load_investigation_cases,
    render_kpi_row,
    render_system_status_panel,
    render_decision_record,
    parse_cases_dataframe,
    badge_html,
    tier_variant,
    case_status_variant,
    resolve_case_id,
    render_case_flow,
    ANALYST_NAME,
    FRAUD_MANAGER_NAME,
)
from rag.retriever import retrieve_policy_matches, format_policy_context, format_policy_citations
from rag.vector_store import PolicyVectorStore
from rag_ingest import ingest_policies
from backend.investigator import run_investigation
from backend.config import validate_config, OPENAI_MODEL

logger = logging.getLogger("ui.pages")

ASSUMED_MANUAL_MINUTES_PER_CASE = 20  # illustrative baseline for the "time saved" estimate below

@st.cache_resource
def _bootstrap_policy_index() -> None:
    """Populates the policy vector store the first time the app runs in a given deployment.
    chroma_db_store/ is gitignored (it's a binary artifact), so a fresh clone - e.g. every
    Streamlit Cloud deploy - starts with an empty index. cache_resource makes this run once
    per process rather than on every rerun."""
    if not validate_config():
        return
    try:
        if PolicyVectorStore().collection.count() == 0:
            ingest_policies()
    except Exception:
        logger.exception("Policy index bootstrap failed.")

@st.cache_data(ttl=30)
def _get_ai_system_status() -> dict:
    """Checks whether the AI investigation engine (LLM credentials + policy knowledge base) is operational.
    Cached for 30s, so 'checked_at' reflects when this check actually last ran, not just 'now'."""
    _bootstrap_policy_index()
    llm_ready = validate_config()
    document_count = 0
    try:
        records = PolicyVectorStore().collection.get(include=["metadatas"])
        document_count = len({m["source_file"] for m in records["metadatas"]})
    except Exception:
        pass
    return {
        "llm_ready": llm_ready,
        "model": OPENAI_MODEL,
        "document_count": document_count,
        "checked_at": datetime.now().strftime("%H:%M:%S"),
    }

def _derive_status(case_id: str, fallback: str) -> str:
    """Resolves a case's current display status: a Fraud Manager's final sign-off takes
    precedence over a recorded disposition, which takes precedence over an in-progress
    investigation, which takes precedence over the case's original status."""
    manager_decision = st.session_state.get("manager_decisions", {}).get(case_id)
    if manager_decision and manager_decision["decision"] == "Closed":
        return "Closed"
    disposition_records = st.session_state.get("disposition_records", {})
    case_results = st.session_state.get("case_results", {})
    disposition = disposition_records.get(case_id)
    if disposition:
        return disposition["decision"]
    if case_id in case_results:
        return "Under Review"
    return fallback

def _resolved_risk(case_id: str, fallback_priority: str) -> str:
    """Resolves a case's current risk tier: the AI's own risk_level once investigated,
    otherwise the case's pre-investigation priority."""
    result = st.session_state.get("case_results", {}).get(case_id)
    return result.get("risk_level", fallback_priority) if result else fallback_priority

def _assigned_to(status_label: str) -> str:
    """A case sits unassigned until someone opens it; there's a single analyst persona for now."""
    return "Unassigned" if status_label.strip().lower() == "new" else ANALYST_NAME

def _last_updated(case_id: str, fallback_date: str) -> str:
    """Resolves the most recent activity timestamp for a case: a manager decision takes
    precedence over a disposition, which takes precedence over an investigation run, which
    takes precedence over the case's original creation date."""
    manager_decision = st.session_state.get("manager_decisions", {}).get(case_id)
    if manager_decision:
        return manager_decision["timestamp"]
    disposition = st.session_state.get("disposition_records", {}).get(case_id)
    if disposition:
        return disposition["timestamp"]
    updated = st.session_state.get("case_last_updated", {}).get(case_id)
    return updated or fallback_date

def render_case_queue_view() -> None:
    """Landing view: the Fraud Operations Work Queue - system health, today's KPIs,
    and the unresolved investigation queue."""
    st.title("Fraud Operations Work Queue")
    st.caption("AI-powered decision support for fraud investigations")
    st.write("")

    cases = load_investigation_cases()
    if not cases:
        st.warning("No cases found in the active data source.")
        return

    df = parse_cases_dataframe(cases)
    df["status"] = [_derive_status(cid, cs) for cid, cs in zip(df["case_id"], df["case_status"])]

    disposed_statuses = {"Approved", "Declined", "Escalated"}  # awaiting Fraud Manager sign-off
    resolved_statuses = disposed_statuses | {"Closed"}  # fully out of the active workload

    active_cases = int((df["status"] == "Under Review").sum())
    pending_review = int((df["status"] == "New").sum())
    open_df = df[~df["status"].isin(resolved_statuses)]
    high_risk_cases = sum(
        _resolved_risk(cid, pr).lower() == "high"
        for cid, pr in zip(open_df["case_id"], open_df["priority"])
    )
    awaiting_approval = int(df["status"].isin(disposed_statuses).sum())

    render_kpi_row([
        ("Active Cases", active_cases),
        ("Pending Analyst Review", pending_review),
        ("High Risk Cases", high_risk_cases),
        ("Awaiting Approval", awaiting_approval),
    ])

    st.write("")
    status = _get_ai_system_status()
    render_system_status_panel(
        [
            ("AI Investigation Engine Online", status["llm_ready"]),
            ("Policy Knowledge Base Connected", status["document_count"] > 0),
            ("Customer Data Available", len(cases) > 0),
        ],
        last_refreshed=status["checked_at"],
    )

    st.write("---")

    st.markdown("##### Investigation Queue")
    unresolved_df = df[df["status"] != "Closed"]
    st.caption(f"{len(unresolved_df)} unresolved investigations")
    st.write("")

    col_widths = [1.0, 1.2, 1.2, 0.7, 0.7, 1.0, 1.1, 1.0, 1.1]
    headers = ["Case ID", "Customer", "Merchant", "Amount", "Priority", "Current Status", "Assigned To", "Last Updated", ""]
    header_cols = st.columns(col_widths)
    for col, label in zip(header_cols, headers):
        col.markdown(f'<div class="queue-header">{label}</div>', unsafe_allow_html=True)

    for _, row in unresolved_df.iterrows():
        cols = st.columns(col_widths)
        cols[0].markdown(f"**{row['case_id']}**")
        cols[1].write(row["customer"])
        cols[2].write(row["merchant"])
        cols[3].write(f"{row['amount']:,.2f}")
        cols[4].markdown(badge_html(row["priority"], tier_variant(row["priority"])), unsafe_allow_html=True)
        cols[5].markdown(badge_html(row["status"], case_status_variant(row["status"])), unsafe_allow_html=True)
        cols[6].write(_assigned_to(row["status"]))
        cols[7].write(_last_updated(row["case_id"], row["created_date"]))
        if cols[8].button("Review →", key=f"open_{row['case_id']}", use_container_width=True):
            st.session_state["selected_case_id"] = row["case_id"]
            st.session_state["_pending_nav"] = "Investigation"
            st.rerun()

def render_investigation_view(current_role: str = ANALYST_NAME) -> None:
    """Single-case investigation workspace: facts, AI assessment, evidence, analyst disposition,
    and (once a disposition exists) the Fraud Manager's final approval. The same view serves both
    roles - what renders in the disposition/approval sections below depends on current_role."""
    st.title("Investigation")
    cases = load_investigation_cases()

    if not cases:
        st.warning("No cases found in the active data source.")
        return

    case_ids = [resolve_case_id(c, idx) for idx, c in enumerate(cases)]
    selected_id = st.selectbox("Case", case_ids, key="selected_case_id")

    case_package = None
    for idx, c in enumerate(cases):
        if resolve_case_id(c, idx) == selected_id:
            case_package = c
            break

    if not case_package:
        st.error("Case not found.")
        return

    if "transaction" in case_package and isinstance(case_package["transaction"], dict):
        txn = case_package["transaction"]
        hist = case_package.get("customer_history", {})
    else:
        txn = case_package
        hist = case_package.get("customer_history") or case_package

    case_results = st.session_state.setdefault("case_results", {})
    disposition_records = st.session_state.setdefault("disposition_records", {})
    manager_decisions = st.session_state.setdefault("manager_decisions", {})
    disposition = disposition_records.get(selected_id)
    manager_decision = manager_decisions.get(selected_id)
    result = case_results.get(selected_id)
    status_label = _derive_status(selected_id, case_package.get("case_status", "New"))

    render_case_flow(status_label)

    # 1. Case header
    case_location = txn.get('location') or txn.get('transaction_location')
    st.markdown(f"""
        <div class="case-header">
            <div class="case-header-id">{selected_id} — {txn.get('customer_name', 'Unknown Customer')}</div>
            <div class="case-header-meta">
                Opened {case_package.get('created_date', 'N/A')} &nbsp;·&nbsp;
                Priority: {case_package.get('priority', 'N/A')} &nbsp;&nbsp;
                {badge_html(status_label, case_status_variant(status_label))}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 2. Case facts
    fact_col1, fact_col2 = st.columns(2)
    with fact_col1:
        st.markdown("##### Transaction")
        st.markdown(
            f"**Amount**   {txn.get('currency', 'USD')} {txn.get('amount', 0):,.2f}  \n"
            f"**Merchant**   {txn.get('merchant', 'N/A')} ({txn.get('merchant_category', 'N/A')})  \n"
            f"**Location**   {case_location or 'N/A'}  \n"
            f"**Device**   {'Known' if txn.get('known_device') else 'Unrecognized'}  \n"
            f"**Travel Notice**   {'On file' if txn.get('travel_notice') else 'None'}"
        )
    with fact_col2:
        st.markdown("##### Customer History")
        st.markdown(
            f"**Average Transaction**   {hist.get('average_transaction', 'N/A')}  \n"
            f"**Highest Transaction**   {hist.get('highest_transaction', 'N/A')}  \n"
            f"**Prior Fraud Cases**   {hist.get('previous_fraud_cases', 0)}"
        )

    st.write("---")

    # 3. Action bar - running investigations is an investigator action, not a manager one
    if current_role == ANALYST_NAME:
        action_label = "Re-run Investigation" if result else "Run Investigation"
        button_type = "secondary" if result else "primary"
        if st.button(action_label, type=button_type):
            with st.spinner("Retrieving policy context and running investigation..."):
                search_query = (
                    f"{txn.get('merchant_category')} purchase of {txn.get('amount')} "
                    f"via {txn.get('device')} location {case_location}"
                )
                policy_matches = retrieve_policy_matches(query=search_query, top_k=2)
                policy_context = format_policy_context(policy_matches)
                policy_citations = format_policy_citations(policy_matches)

                investigation_result = run_investigation(
                    transaction=txn,
                    customer_history=hist,
                    policy_context=policy_context,
                    policy_citations=policy_citations,
                )

                if not investigation_result or investigation_result.get("status") == "error":
                    st.error(f"Investigation failed: {investigation_result.get('message', 'Unknown error')}")
                else:
                    case_results[selected_id] = investigation_result
                    st.session_state.setdefault("case_last_updated", {})[selected_id] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.rerun()

    if not result:
        if current_role == FRAUD_MANAGER_NAME:
            st.info("No investigation has been run for this case yet.")
        else:
            st.info("Run the investigation to view the AI assessment and evidence for this case.")
        return

    # 4. AI Assessment strip
    risk_level = result.get("risk_level", "N/A")
    tier = tier_variant(risk_level)
    st.markdown(f"""
        <div class="assessment-strip tier-{tier}">
            <div style="display:flex; gap:2.5rem; flex-wrap:wrap;">
                <div>
                    <div class="assessment-label">Risk Tier</div>
                    <div class="assessment-value">{badge_html(risk_level, tier)}</div>
                </div>
                <div>
                    <div class="assessment-label">Fraud Score</div>
                    <div class="assessment-value">{result.get('fraud_score', 'N/A')} / 100</div>
                </div>
                <div>
                    <div class="assessment-label">Recommendation</div>
                    <div class="assessment-value">{result.get('recommendation', 'N/A')}</div>
                </div>
                <div>
                    <div class="assessment-label">Confidence</div>
                    <div class="assessment-value">{result.get('confidence', 'N/A')}</div>
                </div>
            </div>
            <div class="assessment-summary">{result.get('investigation_summary', '')}</div>
        </div>
    """, unsafe_allow_html=True)

    # 5. Evidence & Reasoning
    st.markdown("##### Fraud Indicators")
    indicators = result.get("fraud_indicators", [])
    if indicators:
        st.markdown("".join(f'<span class="tag-pill">{i}</span>' for i in indicators), unsafe_allow_html=True)
    else:
        st.caption("No specific fraud indicators identified.")

    st.markdown("##### Reasoning")
    for reason in result.get("reasoning", []):
        st.markdown(f"- {reason}")

    st.markdown("##### Referenced Policies")
    policies = result.get("policy_reference", [])
    if policies:
        for policy in policies:
            st.markdown(f'<div class="policy-citation">{policy}</div>', unsafe_allow_html=True)
    else:
        st.caption("No internal policy directly applicable to this case.")

    st.write("---")

    # 6. Analyst Disposition
    st.markdown("##### Analyst Disposition")
    if disposition:
        render_decision_record(disposition["decision"], disposition["notes"], disposition["analyst"], disposition["timestamp"])
    elif current_role == FRAUD_MANAGER_NAME:
        st.caption("No disposition submitted yet.")
    else:
        if manager_decision and manager_decision["decision"] == "Returned":
            st.warning(f"Returned by {manager_decision['manager']}: {manager_decision['notes']}")
        decision = st.radio(
            "Decision", ["Approved", "Declined", "Escalated"],
            horizontal=True, key=f"decision_{selected_id}"
        )
        notes = st.text_area(
            "Analyst Notes (required)", key=f"notes_{selected_id}",
            placeholder="State the rationale for this decision..."
        )
        if st.button("Submit Disposition", type="primary"):
            if not notes.strip():
                st.error("Analyst notes are required before submitting a disposition.")
            else:
                disposition_records[selected_id] = {
                    "decision": decision,
                    "notes": notes.strip(),
                    "analyst": ANALYST_NAME,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                }
                manager_decisions.pop(selected_id, None)  # start a fresh approval cycle
                st.rerun()

    # 7. Fraud Manager Approval - only relevant once an analyst disposition exists
    if disposition:
        st.write("---")
        st.markdown("##### Fraud Manager Approval")
        if manager_decision and manager_decision["decision"] == "Closed":
            render_decision_record(
                manager_decision["decision"], manager_decision["notes"],
                manager_decision["manager"], manager_decision["timestamp"]
            )
        elif current_role == FRAUD_MANAGER_NAME:
            manager_notes = st.text_area(
                "Manager Notes (required to return a case)", key=f"mgrnotes_{selected_id}",
                placeholder="Optional for approval; required if returning to the investigator..."
            )
            mgr_col1, mgr_col2 = st.columns(2)
            with mgr_col1:
                if st.button("Approve & Close", type="primary", key=f"mgr_close_{selected_id}", use_container_width=True):
                    manager_decisions[selected_id] = {
                        "decision": "Closed",
                        "notes": manager_notes.strip() or "Approved as submitted by the investigator.",
                        "manager": FRAUD_MANAGER_NAME,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    st.rerun()
            with mgr_col2:
                if st.button("Return to Investigator", key=f"mgr_return_{selected_id}", use_container_width=True):
                    if not manager_notes.strip():
                        st.error("Notes are required when returning a case to the investigator.")
                    else:
                        manager_decisions[selected_id] = {
                            "decision": "Returned",
                            "notes": manager_notes.strip(),
                            "manager": FRAUD_MANAGER_NAME,
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }
                        disposition_records.pop(selected_id, None)
                        st.rerun()
        else:
            st.caption("Awaiting Fraud Manager approval.")

def render_manager_queue_view() -> None:
    """Landing view for the Fraud Manager role: cases the analyst has already disposed,
    now awaiting final sign-off before they're closed."""
    st.title("Fraud Manager Approval Queue")
    st.caption("Cases awaiting final sign-off after analyst review")
    st.write("")

    cases = load_investigation_cases()
    if not cases:
        st.warning("No cases found in the active data source.")
        return

    disposition_records = st.session_state.setdefault("disposition_records", {})
    manager_decisions = st.session_state.setdefault("manager_decisions", {})
    case_results = st.session_state.setdefault("case_results", {})

    pending_ids = [cid for cid in disposition_records if manager_decisions.get(cid, {}).get("decision") != "Closed"]
    closed_count = sum(1 for d in manager_decisions.values() if d["decision"] == "Closed")
    returned_count = sum(1 for d in manager_decisions.values() if d["decision"] == "Returned")

    render_kpi_row([
        ("Awaiting Your Approval", len(pending_ids)),
        ("Closed by You", closed_count),
        ("Returned to Investigator", returned_count),
    ])

    st.write("")
    st.write("---")
    st.markdown("##### Approval Queue")

    if not pending_ids:
        st.info("No cases are currently awaiting your approval.")
        return

    col_widths = [1.0, 1.2, 0.9, 0.9, 1.3, 1.2, 1.1, 1.0]
    headers = ["Case ID", "Customer", "Amount", "Priority", "AI Recommendation", "Analyst Decision", "Submitted", ""]
    header_cols = st.columns(col_widths)
    for col, label in zip(header_cols, headers):
        col.markdown(f'<div class="queue-header">{label}</div>', unsafe_allow_html=True)

    for idx, c in enumerate(cases):
        cid = resolve_case_id(c, idx)
        if cid not in pending_ids:
            continue

        txn = c["transaction"] if "transaction" in c and isinstance(c["transaction"], dict) else c
        result = case_results.get(cid, {})
        disposition = disposition_records[cid]

        cols = st.columns(col_widths)
        cols[0].markdown(f"**{cid}**")
        cols[1].write(txn.get("customer_name", "N/A"))
        cols[2].write(f"{txn.get('amount', 0):,.2f}")
        cols[3].markdown(badge_html(c.get("priority", "N/A"), tier_variant(c.get("priority"))), unsafe_allow_html=True)
        cols[4].write(result.get("recommendation", "N/A"))
        cols[5].markdown(badge_html(disposition["decision"], case_status_variant(disposition["decision"])), unsafe_allow_html=True)
        cols[6].write(disposition["timestamp"])
        if cols[7].button("Review →", key=f"mgr_open_{cid}", use_container_width=True):
            st.session_state["selected_case_id"] = cid
            st.session_state["_pending_nav"] = "Investigation"
            st.rerun()

def render_analytics_view() -> None:
    """Operational reporting view: portfolio-level KPIs, exposure distribution, and the
    tool's measured business impact."""
    st.title("Analytics")
    cases = load_investigation_cases()

    if not cases:
        st.warning("No cases found in the active data source.")
        return

    df = parse_cases_dataframe(cases)
    priority_counts = df["priority"].str.lower().value_counts()

    render_kpi_row([
        ("Total Cases", len(df)),
        ("Average Exposure", f"${df['amount'].mean():,.2f}"),
        ("Prior Fraud Incidents", int(df["past_fraud"].sum())),
        ("Priority Mix", f"{int(priority_counts.get('high', 0))}H / {int(priority_counts.get('medium', 0))}M / {int(priority_counts.get('low', 0))}L"),
    ])

    st.write("")
    st.subheader("Exposure by Case")
    st.bar_chart(data=df, x="case_id", y="amount", color="#607456")

    st.write("")
    st.subheader("Portfolio")
    df["status"] = [_derive_status(cid, cs) for cid, cs in zip(df["case_id"], df["case_status"])]
    st.dataframe(
        df[["case_id", "customer", "merchant", "amount", "priority", "status"]],
        use_container_width=True,
        hide_index=True,
    )

    st.write("---")

    st.markdown("##### Business Impact")
    case_results = st.session_state.setdefault("case_results", {})
    investigated_count = len(case_results)
    time_saved_minutes = investigated_count * ASSUMED_MANUAL_MINUTES_PER_CASE
    time_saved_display = f"{time_saved_minutes // 60}h {time_saved_minutes % 60}m" if investigated_count else "0m"
    approve_count = sum(1 for r in case_results.values() if r.get("recommendation") == "Approve")
    reduction_pct = (approve_count / investigated_count * 100) if investigated_count else 0

    render_kpi_row([
        ("Est. Investigation Time Saved", time_saved_display),
        ("Manual Review Reduction", f"{reduction_pct:.0f}%"),
        ("AI Recommendations Generated", investigated_count),
    ])
    st.caption(f"Time saved assumes ~{ASSUMED_MANUAL_MINUTES_PER_CASE} manual minutes per AI-assisted case reviewed today.")

    with st.expander("About this system"):
        st.markdown(
            "The Agentic Fraud Investigation Copilot assists fraud analysts by reviewing flagged "
            "transactions, retrieving relevant internal policy guidance, and producing an "
            "evidence-based recommendation. All recommendations are advisory — the analyst "
            "makes the final decision."
        )
