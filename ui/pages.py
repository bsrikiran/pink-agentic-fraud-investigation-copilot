"""
Purpose: Assembling main dashboard view configurations, interaction workflows, and charts.
"""
from datetime import datetime
import streamlit as st
from ui.components import (
    load_investigation_cases,
    render_metric_card,
    parse_cases_dataframe,
    badge_html,
    tier_variant,
    case_status_variant,
    resolve_case_id,
)
from rag.retriever import retrieve_policy_matches, format_policy_context, format_policy_citations
from backend.investigator import run_investigation

ANALYST_NAME = "Senior Fraud Risk Analyst"

def _derive_status(case_id: str, fallback: str) -> str:
    """Resolves a case's current display status: a recorded disposition takes precedence
    over an in-progress investigation, which takes precedence over the case's original status."""
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

def render_case_queue_view() -> None:
    """Landing view: today's operational snapshot, followed by the case queue."""
    st.title("Case Queue")
    cases = load_investigation_cases()

    if not cases:
        st.warning("No cases found in the active data source.")
        return

    df = parse_cases_dataframe(cases)
    df["status"] = [_derive_status(cid, cs) for cid, cs in zip(df["case_id"], df["case_status"])]

    case_results = st.session_state.setdefault("case_results", {})
    disposed_statuses = {"Approved", "Declined", "Escalated"}

    active_investigations = int((df["status"] == "Under Review").sum())
    require_review = int((df["status"] == "New").sum())
    open_df = df[~df["status"].isin(disposed_statuses)]
    high_risk_cases = sum(
        _resolved_risk(cid, pr).lower() == "high"
        for cid, pr in zip(open_df["case_id"], open_df["priority"])
    )
    waiting_on_approval = sum(
        1 for cid, status in zip(df["case_id"], df["status"])
        if status == "Under Review" and case_results.get(cid, {}).get("recommendation") == "Approve"
    )

    st.markdown("##### Today")
    op_col1, op_col2, op_col3, op_col4 = st.columns(4)
    with op_col1:
        render_metric_card("Active Investigations", active_investigations)
    with op_col2:
        render_metric_card("Require Analyst Review", require_review)
    with op_col3:
        render_metric_card("High Risk Cases", high_risk_cases)
    with op_col4:
        render_metric_card("Waiting on Approval", waiting_on_approval)

    st.write("")
    st.write("---")

    priority_counts = df["priority"].str.lower().value_counts()
    st.caption(
        f"{len(df)} cases in queue  —  "
        f"{int(priority_counts.get('high', 0))} High · "
        f"{int(priority_counts.get('medium', 0))} Medium · "
        f"{int(priority_counts.get('low', 0))} Low priority"
    )
    st.write("")

    col_widths = [1.2, 1.4, 1.4, 1.0, 0.9, 1.1, 0.8]
    header_cols = st.columns(col_widths)
    for col, label in zip(header_cols, ["Case ID", "Customer", "Merchant", "Amount", "Priority", "Status", ""]):
        col.markdown(f'<div class="queue-header">{label}</div>', unsafe_allow_html=True)

    for _, row in df.iterrows():
        cols = st.columns(col_widths)
        cols[0].markdown(f"**{row['case_id']}**")
        cols[1].write(row["customer"])
        cols[2].write(row["merchant"])
        cols[3].write(f"{row['amount']:,.2f}")
        cols[4].markdown(badge_html(row["priority"], tier_variant(row["priority"])), unsafe_allow_html=True)
        cols[5].markdown(badge_html(row["status"], case_status_variant(row["status"])), unsafe_allow_html=True)
        if cols[6].button("Open", key=f"open_{row['case_id']}", use_container_width=True):
            st.session_state["selected_case_id"] = row["case_id"]
            st.session_state["_pending_nav"] = "Investigation"
            st.rerun()

    with st.expander("About this system"):
        st.markdown(
            "The Agentic Fraud Investigation Copilot assists fraud analysts by reviewing flagged "
            "transactions, retrieving relevant internal policy guidance, and producing an "
            "evidence-based recommendation. All recommendations are advisory — the analyst "
            "makes the final decision."
        )

def render_investigation_view() -> None:
    """Single-case investigation workspace: facts, AI assessment, evidence, and analyst disposition."""
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
    disposition = disposition_records.get(selected_id)
    result = case_results.get(selected_id)
    status_label = _derive_status(selected_id, case_package.get("case_status", "New"))

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

    # 3. Action bar
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
                st.rerun()

    if not result:
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
        st.markdown(f"""
            <div class="decision-record">
                {badge_html(disposition['decision'], case_status_variant(disposition['decision']))}
                <div class="decision-record-note">{disposition['notes']}</div>
                <div class="decision-record-meta">Reviewed by {disposition['analyst']} · {disposition['timestamp']}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
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
                st.rerun()

def render_analytics_view() -> None:
    """Operational reporting view: portfolio-level KPIs and exposure distribution."""
    st.title("Analytics")
    cases = load_investigation_cases()

    if not cases:
        st.warning("No cases found in the active data source.")
        return

    df = parse_cases_dataframe(cases)
    priority_counts = df["priority"].str.lower().value_counts()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Total Cases", len(df))
    with col2:
        render_metric_card("Average Exposure", f"${df['amount'].mean():,.2f}")
    with col3:
        render_metric_card("Prior Fraud Incidents", int(df["past_fraud"].sum()))
    with col4:
        render_metric_card(
            "Priority Mix",
            f"{int(priority_counts.get('high', 0))}H / {int(priority_counts.get('medium', 0))}M / {int(priority_counts.get('low', 0))}L"
        )

    st.write("")
    st.subheader("Exposure by Case")
    st.bar_chart(data=df, x="case_id", y="amount")

    st.write("")
    st.subheader("Portfolio")
    df["status"] = [_derive_status(cid, cs) for cid, cs in zip(df["case_id"], df["case_status"])]
    st.dataframe(
        df[["case_id", "customer", "merchant", "amount", "priority", "status"]],
        use_container_width=True,
        hide_index=True,
    )
