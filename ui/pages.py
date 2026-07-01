"""
Purpose: Assembling main dashboard view configurations, interaction workflows, and charts.
"""
import streamlit as st
import pandas as pd
from ui.components import load_investigation_cases, render_metric_card, parse_cases_dataframe
from ui.styles import apply_custom_css
from rag.retriever import retrieve_policy_context
from backend.investigator import run_investigation

def render_home_view() -> None:
    """Displays project metadata overview tracking matrices."""
    st.title("🛡️ Agentic Fraud Investigation Copilot")
    st.caption("Enterprise Infrastructure Control Console | Fraud Operations Management Matrix")
    st.write("")
    
    st.markdown("""
    ### System Overview
    This solution acts as an intelligent assistant tailored for fraud risk analyst workflows. 
    It dynamically isolates transaction anomalies, queries compliance rules directly from text repositories using semantic vector retrieval, and outputs explainable structural indicators to maximize evaluation consistency.
    
    ### Architectural Core Stack
    * **Backend Pipeline Layers**: Python 3.12 Engine / Pydantic Verification Contract Constraints / OpenAI Core
    * **Knowledge Indexing Engine (RAG)**: ChromaDB Persistent Vector Tables / Semantic Similarity Search
    * **Presentation Controls Node**: Streamlit Operations Dashboard Suite Layout Framework
    """)
    st.write("")
    st.info("System Ready. Click the navigation options above to initiate active transaction validation runs.")

def render_investigation_pipeline_view() -> None:
    """Orchestrates multi-turn review sessions, execution requests, and charts responses."""
    st.title("🔎 Automated Evaluation Workbench")
    cases = load_investigation_cases()
    
    if not cases:
        st.warning("No operational investigation entities found within active local data clusters.")
        return
        
    # Case Selector Control Node
    case_ids = [c.get("transaction", {}).get("transaction_id", "UNKNOWN-ID") for c in cases]
    selected_id = st.selectbox("Select Active Risk Ticket ID for Evaluation:", case_ids)
    
    # Locate targeted data structures mapping indices records safely
    case_package = next((c for c in cases if c.get("transaction", {}).get("transaction_id") == selected_id), None)
    
    if not case_package:
        st.error("Data routing configuration anomaly: target payload map references not found.")
        return
        
    txn = case_package.get("transaction", {})
    hist = case_package.get("customer_history", {})
    
    # Display Case Properties in crisp dual-column subgrids
    st.subheader("Transaction Metadata Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"Customer Name: {txn.get('customer_name')}")
        st.text(f"Financial Value: {txn.get('currency', 'USD')} {txn.get('amount'):,}")
    with col2:
        st.text(f"Counterparty Merchant: {txn.get('merchant')}")
        st.text(f"Location Zone: {txn.get('location')}")
    with col3:
        st.text(f"Device Known: {'Yes' if txn.get('known_device') else 'No (New Fingerprint)'}")
        st.text(f"Travel Profile Active: {'Yes' if txn.get('travel_notice') else 'No Notification'}")

    st.write("---")
    
    # Core Application Workflow Trigger Execution Button Node
    if st.button("Execute Automated Investigation Sequence", type="primary"):
        with st.spinner("Retrieving compliance parameters and downloading AI evaluation arrays..."):
            
            # Step 1: Query contextual data structures directly out of RAG Vector stores
            search_query = f"{txn.get('merchant_category')} purchase of {txn.get('amount')} via {txn.get('device')} location {txn.get('location')}"
            policy_context = retrieve_policy_context(query=search_query, top_k=2)
            
            # Step 2: Invoke the backend public signature interface contract endpoint mapping parameters
            investigation_result = run_investigation(
                transaction=txn,
                customer_history=hist,
                policy_context=policy_context
            )
            
            # Handle standard functional baseline exception scenarios gracefully
            if not investigation_result or investigation_result.get("status") == "error":
                st.error(f"Investigation execution failed: {investigation_result.get('message', 'Unknown backend exception state')}")
                return
                
            # Stash analytical states safely inside Session Memory blocks for multi-turn tabs viewing access
            st.session_state["active_result"] = investigation_result
            st.session_state["last_evaluated_case_id"] = selected_id
            st.success("Analysis cycle completely finalized. Review output results via the panels below.")

    # Render results dynamically if stashed in session registers
    if "active_result" in st.session_state and st.session_state.get("last_evaluated_case_id") == selected_id:
        res = st.session_state["active_result"]
        
        st.write("")
        st.header("📈 AI Recommendation Profile Output")
        
        # Recommendation Banner Card Design Elements
        st.markdown(f"""
            <div class="rec-banner">
                <div class="rec-label">Operational Recommendation Directive</div>
                <div class="rec-text">{res.get('recommendation', 'Pending Assessment')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            render_metric_card("Calculated Fraud Score", f"{res.get('fraud_score', 0)} / 100")
        with col_m2:
            render_metric_card("Risk Assessment Level", res.get('risk_level', 'N/A'))
        with col_m3:
            render_metric_card("System Assurance Confidence", res.get('confidence', 'N/A'))
            
        st.write("")
        st.subheader("Investigation Executive Summary Wrap-up")
        st.info(res.get("investigation_summary", "No textual abstract returned."))
        
        col_details_1, col_details_2 = st.columns(2)
        with col_details_1:
            st.markdown("#### Observed Risk Indicators")
            for indicator in res.get("fraud_indicators", []):
                st.markdown(f"- ⚠️ {indicator}")
        with col_details_2:
            st.markdown("#### Decision Analytical Reasoning Logic")
            for reason in res.get("reasoning", []):
                st.markdown(f"- {reason}")
                
        st.write("")
        st.markdown("#### Matched Corporate Compliance Policy References Citing")
        for policy in res.get("policy_reference", []):
            st.markdown(f"💼 **{policy}**")
            
        # Human In The Loop Validation Review Screen Section Interactive Buttons Node
        st.write("---")
        st.header("✍️ Human-in-the-Loop Operations Sign-off Panel")
        st.caption("Provide manual structural review authorization confirmation overrides directly below.")
        
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("Confirm Approval Mandate", key="btn_app", use_container_width=True):
                st.session_state["review_signed_id"] = selected_id
                st.session_state["review_signed_status"] = "Approved and Cleared"
        with col_btn2:
            if st.button("Enforce Reject & Void Protocol", key="btn_rej", use_container_width=True):
                st.session_state["review_signed_id"] = selected_id
                st.session_state["review_signed_status"] = "Voided and Blocked"
        with col_btn3:
            if st.button("Escalate to Senior Fraud Desk", key="btn_esc", use_container_width=True):
                st.session_state["review_signed_id"] = selected_id
                st.session_state["review_signed_status"] = "Escalated for Secondary Manual Review Audits"
                
        if st.session_state.get("review_signed_id") == selected_id:
            st.toast(f"Operational update processed completely: {st.session_state['review_signed_status']}", icon="✅")
            st.success(f"Audit log synchronized: Case entry marked as **{st.session_state['review_signed_status']}**.")

def render_metrics_dashboard_view() -> None:
    """Compiles statistics summaries using native high-speed tracking dataframe charts tools."""
    st.title("📊 Global Operations Metrics Analytics")
    cases = load_investigation_cases()
    
    if not cases:
        st.warning("No metrics registries files mounted into visualization engines paths.")
        return
        
    df = parse_cases_dataframe(cases)
    
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        render_metric_card("Total Logs Under Management", len(df))
    with col_stat2:
        render_metric_card("Mean Exposure Limit Profile", f"${df['amount'].mean():,.2f}")
    with col_stat3:
        render_metric_card("Historical Prior Fraud Incidents Count", int(df["past_fraud"].sum()))
        
    st.write("")
    st.subheader("Financial Exposure Value Distribution Across Active Portfolio Tickets")
    # Native lightweight chart display rendering
    st.bar_chart(data=df, x="case_id", y="amount")
