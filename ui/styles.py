"""
Purpose: Defines custom UI presentation styles and banking operational aesthetic themes.
"""
import streamlit as st

def apply_custom_css() -> None:
    """Injects institutional typography, neutral backgrounds, and status-badge color coding."""
    st.markdown("""
        <style>
            /* Global Application Alignment and Typography */
            [data-testid="stHeader"] { height: 1.5rem !important; min-height: 1.5rem !important; }
            [data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; padding-bottom: 2rem; }
            h1, h2, h3 { color: #0F172A !important; font-family: 'Inter', -apple-system, sans-serif; }

            /* AI System Status panel: multiple check rows + a last-refreshed footer */
            .status-panel {
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                padding: 0.75rem 1rem;
                background-color: #F8FAFC;
                margin-bottom: 1.25rem;
            }
            .status-row { display: flex; align-items: center; gap: 0.55rem; font-size: 0.85rem; color: #166534; padding: 0.2rem 0; }
            .status-row.down { color: #991B1B; }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
            .status-dot.ok { background-color: #22C55E; }
            .status-dot.down { background-color: #EF4444; }
            .status-panel-footer {
                font-size: 0.75rem; color: #94A3B8; margin-top: 0.4rem;
                padding-top: 0.4rem; border-top: 1px solid #E2E8F0;
            }

            /* Metric Cards (Analytics KPIs) */
            .metric-container {
                background-color: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 1.25rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            }
            .metric-value { font-size: 2.25rem; font-weight: 700; color: #1E293B; margin: 0.5rem 0; }
            .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; }

            /* Status / Priority / Risk badges - the one place saturated color is allowed */
            .badge {
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }
            .badge-high   { background-color: #FEE2E2; color: #B91C1C; }
            .badge-medium { background-color: #FEF3C7; color: #92400E; }
            .badge-low    { background-color: #DCFCE7; color: #15803D; }
            .badge-neutral    { background-color: #E2E8F0; color: #334155; }
            .badge-approved   { background-color: #DCFCE7; color: #15803D; }
            .badge-declined   { background-color: #FEE2E2; color: #B91C1C; }
            .badge-escalated  { background-color: #FEF3C7; color: #92400E; }
            .badge-review     { background-color: #DBEAFE; color: #1D4ED8; }

            /* Case Queue rows */
            .queue-row {
                border-bottom: 1px solid #E2E8F0;
                padding: 0.65rem 0.25rem;
            }
            .queue-header {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #64748B;
                border-bottom: 1px solid #CBD5E1;
                padding-bottom: 0.4rem;
            }

            /* Analyst identity block, top-right of every page */
            .identity-header { text-align: right; margin-bottom: 0.5rem; }
            .identity-name { font-weight: 600; color: #0F172A; font-size: 0.95rem; }
            .identity-meta { font-size: 0.82rem; color: #64748B; margin-top: 0.1rem; }

            /* Case lifecycle flow stepper (Investigation view) */
            .flow-stepper { display: flex; align-items: flex-start; margin: 0.25rem 0 1.75rem 0; }
            .flow-step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex-shrink: 0; }
            .flow-dot {
                width: 16px; height: 16px; border-radius: 50%;
                border: 2px solid #CBD5E1; background-color: #FFFFFF; box-sizing: border-box;
            }
            .flow-step.done .flow-dot { background-color: #0F172A; border-color: #0F172A; }
            .flow-step.current .flow-dot { background-color: #FFFFFF; border-color: #0284C7; box-shadow: 0 0 0 3px rgba(2,132,199,0.18); }
            .flow-label { font-size: 0.78rem; color: #94A3B8; white-space: nowrap; }
            .flow-step.done .flow-label { color: #475569; font-weight: 500; }
            .flow-step.current .flow-label { color: #0284C7; font-weight: 700; }
            .flow-connector { flex: 1 1 auto; height: 2px; background-color: #E2E8F0; margin: 7px 0.5rem 0 0.5rem; min-width: 24px; }
            .flow-connector.done { background-color: #0F172A; }

            /* Case header bar (Investigation view) */
            .case-header {
                border-bottom: 1px solid #E2E8F0;
                padding-bottom: 0.75rem;
                margin-bottom: 0.75rem;
            }
            .case-header-id { font-size: 1.4rem; font-weight: 700; color: #0F172A; }
            .case-header-meta { font-size: 0.85rem; color: #64748B; margin-top: 0.15rem; }

            /* AI Assessment strip - compact verdict row, not a marketing banner */
            .assessment-strip {
                border-left: 4px solid #64748B;
                background-color: #F8FAFC;
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                margin-bottom: 1rem;
            }
            .assessment-strip.tier-high   { border-left-color: #B91C1C; }
            .assessment-strip.tier-medium { border-left-color: #D97706; }
            .assessment-strip.tier-low    { border-left-color: #15803D; }
            .assessment-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748B; }
            .assessment-value { font-size: 1.05rem; font-weight: 600; color: #1E293B; margin-top: 0.1rem; }
            .assessment-summary { font-size: 0.92rem; color: #334155; margin-top: 0.6rem; line-height: 1.5; }

            /* Fraud indicator tags */
            .tag-pill {
                display: inline-block;
                background-color: #F1F5F9;
                border: 1px solid #E2E8F0;
                color: #334155;
                border-radius: 4px;
                padding: 0.2rem 0.55rem;
                margin: 0 0.35rem 0.35rem 0;
                font-size: 0.82rem;
            }

            /* Policy citation trail */
            .policy-citation {
                font-size: 0.85rem;
                color: #475569;
                border-left: 2px solid #CBD5E1;
                padding-left: 0.6rem;
                margin-bottom: 0.35rem;
            }

            /* Analyst decision record (locked disposition) */
            .decision-record {
                border: 1px solid #E2E8F0;
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                background-color: #F8FAFC;
            }
            .decision-record-note { font-size: 0.88rem; color: #334155; margin-top: 0.4rem; line-height: 1.5; }
            .decision-record-meta { font-size: 0.78rem; color: #64748B; margin-top: 0.5rem; }
        </style>
    """, unsafe_allow_html=True)
