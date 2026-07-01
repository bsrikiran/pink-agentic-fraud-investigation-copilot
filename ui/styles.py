"""
Purpose: Defines custom UI presentation styles and banking operational aesthetic themes.
"""
import streamlit as st

def apply_custom_css() -> None:
    """Injects institutional typography, brand color tokens, and status-badge color coding.
    Brand palette: primary sage green (structure/navigation/primary actions), secondary cream
    (surfaces/backgrounds), accent terracotta (secondary actions/highlights, used sparingly),
    and critical red (reserved for fraud/risk states only)."""
    st.markdown("""
        <style>
            :root {
                --color-primary: #607456;
                --color-primary-dark: #4A5A42;
                --color-primary-light: #E3E9DE;
                --color-primary-light-text: #3F4D39;

                --color-secondary: #EEE0CC;
                --color-secondary-soft: #FAF6EF;
                --color-border: #E3DACB;

                --color-accent: #BA6A4C;
                --color-accent-dark: #A15A3E;
                --color-accent-light: #F6E4DA;
                --color-accent-light-text: #8A4A32;

                --color-critical: #7B2525;
                --color-critical-light: #F3DEDE;

                --color-neutral-bg: #E7E2D6;
                --color-neutral-text: #5B5648;

                --color-text-heading: #4A5A42;
                --color-text-body: #33362F;
                --color-text-muted: #7A7364;

                --color-sidebar-bg: #607456;
                --color-sidebar-text: #F5F1E8;
                --color-sidebar-muted: rgba(245, 241, 232, 0.72);
                --color-sidebar-hr: rgba(245, 241, 232, 0.25);
                --color-sidebar-active-bg: rgba(255, 255, 255, 0.14);
            }

            /* Global Application Alignment and Typography */
            [data-testid="stHeader"] { height: 1.5rem !important; min-height: 1.5rem !important; background-color: var(--color-secondary-soft) !important; }
            [data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; padding-bottom: 2rem; }
            [data-testid="stAppViewContainer"] { background-color: var(--color-secondary-soft); }
            h1, h2, h3 { color: var(--color-text-heading) !important; font-family: 'Inter', -apple-system, sans-serif; }
            body, p, .stMarkdown, [data-testid="stMarkdownContainer"] { color: var(--color-text-body); }
            a, a:visited { color: var(--color-accent); }
            a:hover { color: var(--color-accent-dark); }

            /* Sidebar - primary brand color anchors the whole app */
            [data-testid="stSidebar"] {
                background-color: var(--color-sidebar-bg) !important;
                border-right: 1px solid var(--color-primary-dark);
            }
            [data-testid="stSidebar"] * { color: var(--color-sidebar-text); }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 { color: var(--color-sidebar-text) !important; }
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: var(--color-sidebar-muted) !important; }
            [data-testid="stSidebar"] hr { border-top: 1px solid var(--color-sidebar-hr); }
            /* Native radio: force ring/dot to sidebar-text regardless of the app-wide primaryColor,
            since the theme's primaryColor (green) would otherwise render invisible on this green bg */
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
                background-color: transparent !important;
                border: 1px solid var(--color-sidebar-muted) !important;
                border-radius: 50%;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child > div {
                background-color: var(--color-sidebar-text) !important;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) > div:first-child {
                border-color: var(--color-sidebar-text) !important;
                background-color: var(--color-sidebar-active-bg) !important;
            }

            /* Native alert banners (st.info/warning/error/success) - replace Streamlit's default
            blue/yellow/red/green with brand-consistent tints */
            [data-testid="stAlertContainer"] { background-color: transparent !important; }
            [data-testid="stAlertContentInfo"] {
                background-color: var(--color-secondary) !important;
                color: var(--color-text-muted) !important;
                border-left: 3px solid var(--color-border);
                border-radius: 4px;
            }
            [data-testid="stAlertContentWarning"] {
                background-color: var(--color-accent-light) !important;
                color: var(--color-accent-light-text) !important;
                border-left: 3px solid var(--color-accent);
                border-radius: 4px;
            }
            [data-testid="stAlertContentError"] {
                background-color: var(--color-critical-light) !important;
                color: var(--color-critical) !important;
                border-left: 3px solid var(--color-critical);
                border-radius: 4px;
            }
            [data-testid="stAlertContentSuccess"] {
                background-color: var(--color-primary-light) !important;
                color: var(--color-primary-light-text) !important;
                border-left: 3px solid var(--color-primary);
                border-radius: 4px;
            }
            [data-testid="stAlertContentInfo"] p,
            [data-testid="stAlertContentWarning"] p,
            [data-testid="stAlertContentError"] p,
            [data-testid="stAlertContentSuccess"] p { color: inherit !important; }
            [data-testid="stAlertContentInfo"] [data-testid="stIconMaterial"],
            [data-testid="stAlertContentWarning"] [data-testid="stIconMaterial"],
            [data-testid="stAlertContentError"] [data-testid="stIconMaterial"],
            [data-testid="stAlertContentSuccess"] [data-testid="stIconMaterial"] { color: inherit !important; }

            /* Buttons: primary = brand green (native theme), secondary = accent terracotta */
            [data-testid="stBaseButton-primary"] { background-color: var(--color-primary) !important; border-color: var(--color-primary) !important; }
            [data-testid="stBaseButton-primary"]:hover { background-color: var(--color-primary-dark) !important; border-color: var(--color-primary-dark) !important; }
            [data-testid="stBaseButton-secondary"] { color: var(--color-accent) !important; border-color: var(--color-accent) !important; background-color: transparent !important; }
            [data-testid="stBaseButton-secondary"]:hover { color: var(--color-accent-dark) !important; border-color: var(--color-accent-dark) !important; background-color: var(--color-accent-light) !important; }

            /* AI System Status panel: multiple check rows + a last-refreshed footer */
            .status-panel {
                border: 1px solid var(--color-border);
                border-radius: 4px;
                padding: 0.75rem 1rem;
                background-color: var(--color-secondary);
                margin-bottom: 1.25rem;
            }
            .status-row { display: flex; align-items: center; gap: 0.55rem; font-size: 0.85rem; color: var(--color-primary-dark); padding: 0.2rem 0; }
            .status-row.down { color: var(--color-critical); }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
            .status-dot.ok { background-color: var(--color-primary); }
            .status-dot.down { background-color: var(--color-critical); }
            .status-panel-footer {
                font-size: 0.75rem; color: var(--color-text-muted); margin-top: 0.4rem;
                padding-top: 0.4rem; border-top: 1px solid var(--color-border);
            }

            /* Metric Cards (Analytics KPIs) */
            .metric-container {
                background-color: var(--color-secondary);
                border: 1px solid var(--color-border);
                border-top: 3px solid var(--color-accent);
                border-radius: 6px;
                padding: 1.25rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            }
            .metric-value { font-size: 2.25rem; font-weight: 700; color: var(--color-text-heading); margin: 0.5rem 0; }
            .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-muted); }

            /* Status / Priority / Risk badges - the primary place accent/critical color is allowed */
            .badge {
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }
            .badge-high       { background-color: var(--color-critical-light); color: var(--color-critical); }
            .badge-medium     { background-color: var(--color-accent-light); color: var(--color-accent-light-text); }
            .badge-low        { background-color: var(--color-primary-light); color: var(--color-primary-light-text); }
            .badge-neutral    { background-color: var(--color-neutral-bg); color: var(--color-neutral-text); }
            .badge-approved   { background-color: var(--color-primary-light); color: var(--color-primary-light-text); }
            .badge-declined   { background-color: var(--color-critical-light); color: var(--color-critical); }
            .badge-escalated  { background-color: var(--color-critical-light); color: var(--color-critical); }
            .badge-review     { background-color: var(--color-accent-light); color: var(--color-accent-light-text); }
            .badge-returned   { background-color: var(--color-accent-light); color: var(--color-accent-light-text); }
            .badge-closed     { background-color: var(--color-primary-dark); color: var(--color-sidebar-text); }

            /* Case Queue rows */
            .queue-row {
                border-bottom: 1px solid var(--color-border);
                padding: 0.65rem 0.25rem;
            }
            .queue-header {
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: var(--color-text-muted);
                border-bottom: 1px solid var(--color-border);
                padding-bottom: 0.4rem;
            }

            /* Analyst identity block, top-right of every page */
            .identity-header { text-align: right; margin-bottom: 0.5rem; }
            .identity-name { font-weight: 600; color: var(--color-text-heading); font-size: 0.95rem; }
            .identity-meta { font-size: 0.82rem; color: var(--color-text-muted); margin-top: 0.1rem; }

            /* Case lifecycle flow stepper (Investigation view) */
            .flow-stepper { display: flex; align-items: flex-start; margin: 0.25rem 0 1.75rem 0; }
            .flow-step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex-shrink: 0; }
            .flow-dot {
                width: 16px; height: 16px; border-radius: 50%;
                border: 2px solid var(--color-border); background-color: var(--color-secondary-soft); box-sizing: border-box;
            }
            .flow-step.done .flow-dot { background-color: var(--color-primary); border-color: var(--color-primary); }
            .flow-step.current .flow-dot { background-color: var(--color-secondary-soft); border-color: var(--color-accent); box-shadow: 0 0 0 3px rgba(186,106,76,0.18); }
            .flow-label { font-size: 0.78rem; color: var(--color-text-muted); white-space: nowrap; }
            .flow-step.done .flow-label { color: var(--color-primary-dark); font-weight: 500; }
            .flow-step.current .flow-label { color: var(--color-accent); font-weight: 700; }
            .flow-connector { flex: 1 1 auto; height: 2px; background-color: var(--color-border); margin: 7px 0.5rem 0 0.5rem; min-width: 24px; }
            .flow-connector.done { background-color: var(--color-primary); }

            /* Case header bar (Investigation view) */
            .case-header {
                border-bottom: 1px solid var(--color-border);
                padding-bottom: 0.75rem;
                margin-bottom: 0.75rem;
            }
            .case-header-id { font-size: 1.4rem; font-weight: 700; color: var(--color-text-heading); }
            .case-header-meta { font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.15rem; }

            /* AI Assessment strip - compact verdict row, not a marketing banner */
            .assessment-strip {
                border-left: 4px solid var(--color-primary);
                background-color: var(--color-secondary);
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                margin-bottom: 1rem;
            }
            .assessment-strip.tier-high   { border-left-color: var(--color-critical); }
            .assessment-strip.tier-medium { border-left-color: var(--color-accent); }
            .assessment-strip.tier-low    { border-left-color: var(--color-primary); }
            .assessment-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-muted); }
            .assessment-value { font-size: 1.05rem; font-weight: 600; color: var(--color-text-heading); margin-top: 0.1rem; }
            .assessment-summary { font-size: 0.92rem; color: var(--color-text-body); margin-top: 0.6rem; line-height: 1.5; }

            /* Fraud indicator tags */
            .tag-pill {
                display: inline-block;
                background-color: var(--color-secondary);
                border: 1px solid var(--color-border);
                color: var(--color-text-body);
                border-radius: 4px;
                padding: 0.2rem 0.55rem;
                margin: 0 0.35rem 0.35rem 0;
                font-size: 0.82rem;
            }

            /* Policy citation trail */
            .policy-citation {
                font-size: 0.85rem;
                color: var(--color-text-muted);
                border-left: 2px solid var(--color-border);
                padding-left: 0.6rem;
                margin-bottom: 0.35rem;
            }

            /* Analyst decision record (locked disposition) */
            .decision-record {
                border: 1px solid var(--color-border);
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                background-color: var(--color-secondary);
            }
            .decision-record-note { font-size: 0.88rem; color: var(--color-text-body); margin-top: 0.4rem; line-height: 1.5; }
            .decision-record-meta { font-size: 0.78rem; color: var(--color-text-muted); margin-top: 0.5rem; }
        </style>
    """, unsafe_allow_html=True)
