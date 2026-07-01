"""
Purpose: Defines custom UI presentation styles and banking operational aesthetic themes.
"""
import streamlit as st

def apply_custom_css() -> None:
    """Injects institutional typography, brand color tokens, and status-badge color coding.
    Brand palette (strict 4-token enterprise system): #EEEEEE primary background (canvas, cards,
    tables, inputs), #DDDDDD secondary surface (sidebar, KPI cards, table headers, containers),
    #CB2957 brand accent used sparingly (buttons, links, active states, medium-severity signal),
    #000000 for text and critical/high-severity signal only. Severity is expressed as an intensity
    ramp - neutral (low) -> accent (medium) -> black (high) - rather than a color per category,
    since the palette has no dedicated red/yellow/green."""
    st.markdown("""
        <style>
            :root {
                /* Primary Background - 65% */
                --color-bg: #EEEEEE;

                /* Secondary Surface - 20% */
                --color-surface: #DDDDDD;
                --color-border: rgba(0, 0, 0, 0.14);

                /* Brand Accent - 10% (sparing: buttons, links, active/selected states,
                   medium-severity signal, progress indicators) */
                --color-accent: #CB2957;
                --color-accent-hover: #A8203F;
                --color-accent-tint: rgba(203, 41, 87, 0.10);
                --color-accent-tint-strong: rgba(203, 41, 87, 0.18);

                /* Text / Critical Contrast - 5% */
                --color-text: #000000;
                --color-text-muted: rgba(0, 0, 0, 0.62);
                --color-text-faint: rgba(0, 0, 0, 0.40);
                --color-critical-tint: rgba(0, 0, 0, 0.07);

                /* Sidebar - secondary surface, light enterprise nav (not a brand-color fill) */
                --color-sidebar-bg: #DDDDDD;
                --color-sidebar-text: #000000;
                --color-sidebar-muted: rgba(0, 0, 0, 0.60);
                --color-sidebar-hr: rgba(0, 0, 0, 0.14);
                --color-sidebar-active-bg: rgba(203, 41, 87, 0.14);
            }

            /* Global Application Alignment and Typography */
            [data-testid="stHeader"] { height: 1.5rem !important; min-height: 1.5rem !important; background-color: var(--color-bg) !important; }
            [data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; padding-bottom: 2rem; }
            [data-testid="stAppViewContainer"] { background-color: var(--color-bg); }
            h1, h2, h3 { color: var(--color-text) !important; font-family: 'Inter', -apple-system, sans-serif; }
            body, p, .stMarkdown, [data-testid="stMarkdownContainer"] { color: var(--color-text); }
            a, a:visited { color: var(--color-accent); }
            a:hover { color: var(--color-accent-hover); }

            /* Input backgrounds - primary background tone, distinct from the secondary-surface
               chrome (sidebar/KPI cards/headers) so form fields read as part of the canvas */
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stNumberInput"] input,
            [data-testid="stDateInput"] input,
            [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                background-color: var(--color-bg) !important;
                border-color: var(--color-border) !important;
            }

            /* Sidebar - light secondary-surface nav (enterprise pattern, not a brand-color anchor) */
            [data-testid="stSidebar"] {
                background-color: var(--color-sidebar-bg) !important;
                border-right: 1px solid var(--color-border);
            }
            [data-testid="stSidebar"] * { color: var(--color-sidebar-text); }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 { color: var(--color-sidebar-text) !important; }
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: var(--color-sidebar-muted) !important; }
            [data-testid="stSidebar"] hr { border-top: 1px solid var(--color-sidebar-hr); }
            /* Native radio: active nav item gets the accent ring + tint, not a full-width fill */
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
                background-color: transparent !important;
                border: 1px solid var(--color-sidebar-muted) !important;
                border-radius: 50%;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child > div {
                background-color: var(--color-accent) !important;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) > div:first-child {
                border-color: var(--color-accent) !important;
                background-color: var(--color-sidebar-active-bg) !important;
            }

            /* Native alert banners (st.info/warning/error/success) - brand-consistent tints.
               Severity ramp: info/success = neutral surface, warning = accent, error = black. */
            [data-testid="stAlertContainer"] { background-color: transparent !important; }
            [data-testid="stAlertContentInfo"] {
                background-color: var(--color-surface) !important;
                color: var(--color-text-muted) !important;
                border-left: 3px solid var(--color-border);
                border-radius: 4px;
            }
            [data-testid="stAlertContentWarning"] {
                background-color: var(--color-accent-tint) !important;
                color: var(--color-accent) !important;
                border-left: 3px solid var(--color-accent);
                border-radius: 4px;
            }
            [data-testid="stAlertContentError"] {
                background-color: var(--color-critical-tint) !important;
                color: var(--color-text) !important;
                border-left: 3px solid var(--color-text);
                border-radius: 4px;
                font-weight: 600;
            }
            [data-testid="stAlertContentSuccess"] {
                background-color: var(--color-surface) !important;
                color: var(--color-text) !important;
                border-left: 3px solid var(--color-border);
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

            /* Buttons: primary = brand accent (native theme), secondary = accent outline */
            [data-testid="stBaseButton-primary"] { background-color: var(--color-accent) !important; border-color: var(--color-accent) !important; color: #FFFFFF !important; }
            [data-testid="stBaseButton-primary"] p { color: #FFFFFF !important; }
            [data-testid="stBaseButton-primary"]:hover { background-color: var(--color-accent-hover) !important; border-color: var(--color-accent-hover) !important; }
            [data-testid="stBaseButton-secondary"] { color: var(--color-accent) !important; border-color: var(--color-accent) !important; background-color: transparent !important; }
            [data-testid="stBaseButton-secondary"]:hover { color: var(--color-accent-hover) !important; border-color: var(--color-accent-hover) !important; background-color: var(--color-accent-tint) !important; }

            /* AI System Status panel: multiple check rows + a last-refreshed footer.
               "OK" is a calm neutral dot; "Down" escalates to full-contrast black. */
            .status-panel {
                border: 1px solid var(--color-border);
                border-radius: 4px;
                padding: 0.75rem 1rem;
                background-color: var(--color-surface);
                margin-bottom: 1.25rem;
            }
            .status-row { display: flex; align-items: center; gap: 0.55rem; font-size: 0.85rem; color: var(--color-text-muted); padding: 0.2rem 0; }
            .status-row.down { color: var(--color-text); font-weight: 600; }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
            .status-dot.ok { background-color: var(--color-text-faint); }
            .status-dot.down { background-color: var(--color-text); }
            .status-panel-footer {
                font-size: 0.75rem; color: var(--color-text-muted); margin-top: 0.4rem;
                padding-top: 0.4rem; border-top: 1px solid var(--color-border);
            }

            /* Metric Cards (Analytics KPIs) - secondary surface with a thin accent top-stripe;
               the accent marks "this is a KPI worth attention" without coloring the number itself */
            .metric-container {
                background-color: var(--color-surface);
                border: 1px solid var(--color-border);
                border-top: 3px solid var(--color-accent);
                border-radius: 6px;
                padding: 1.25rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            }
            .metric-value { font-size: 2.25rem; font-weight: 700; color: var(--color-text); margin: 0.5rem 0; }
            .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-muted); }

            /* Status / Priority / Risk badges - severity intensity ramp:
               low/resolved = neutral surface, medium/needs-review = accent, high/critical = black */
            .badge {
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }
            .badge-high       { background-color: var(--color-critical-tint); color: var(--color-text); border: 1px solid rgba(0,0,0,0.25); }
            .badge-medium     { background-color: var(--color-accent-tint); color: var(--color-accent); }
            .badge-low        { background-color: var(--color-surface); color: var(--color-text-muted); }
            .badge-neutral    { background-color: var(--color-surface); color: var(--color-text-muted); }
            .badge-approved   { background-color: var(--color-surface); color: var(--color-text); }
            .badge-declined   { background-color: var(--color-critical-tint); color: var(--color-text); border: 1px solid rgba(0,0,0,0.25); }
            .badge-escalated  { background-color: var(--color-critical-tint); color: var(--color-text); border: 1px solid rgba(0,0,0,0.25); }
            .badge-review     { background-color: var(--color-accent-tint); color: var(--color-accent); }
            .badge-returned   { background-color: var(--color-accent-tint); color: var(--color-accent); }
            .badge-closed     { background-color: var(--color-text); color: var(--color-bg); }

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
                background-color: var(--color-surface);
                border-bottom: 1px solid var(--color-border);
                padding: 0.4rem 0.25rem;
            }

            /* Role selection gate (first load): centered title + two role cards */
            .role-gate { text-align: center; margin: 4vh 0 2.5rem 0; }
            .role-gate-title { font-size: 2rem; font-weight: 800; color: var(--color-text); }
            .role-gate-subtitle { font-size: 1rem; color: var(--color-text-muted); margin-top: 0.5rem; }
            .role-card {
                background-color: var(--color-surface);
                border: 1px solid var(--color-border);
                border-top: 4px solid var(--color-accent);
                border-radius: 8px;
                padding: 2rem 1.5rem 1.25rem;
                text-align: center;
                margin-bottom: 0.75rem;
                min-height: 130px;
            }
            .role-card-title { font-size: 1.2rem; font-weight: 700; color: var(--color-text); }
            .role-card-desc { font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.5rem; line-height: 1.4; }

            /* Analyst identity block, top-right of every page */
            .identity-header { text-align: right; margin-bottom: 0.5rem; }
            .identity-name { font-weight: 600; color: var(--color-text); font-size: 0.95rem; }
            .identity-meta { font-size: 0.82rem; color: var(--color-text-muted); margin-top: 0.1rem; }

            /* Case lifecycle flow stepper (Investigation view) - progress = accent */
            .flow-stepper { display: flex; align-items: flex-start; margin: 0.25rem 0 1.75rem 0; }
            .flow-step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex-shrink: 0; }
            .flow-dot {
                width: 16px; height: 16px; border-radius: 50%;
                border: 2px solid var(--color-border); background-color: var(--color-bg); box-sizing: border-box;
            }
            .flow-step.done .flow-dot { background-color: var(--color-accent); border-color: var(--color-accent); }
            .flow-step.current .flow-dot { background-color: var(--color-bg); border-color: var(--color-accent); box-shadow: 0 0 0 3px var(--color-accent-tint-strong); }
            .flow-label { font-size: 0.78rem; color: var(--color-text-muted); white-space: nowrap; }
            .flow-step.done .flow-label { color: var(--color-text); font-weight: 500; }
            .flow-step.current .flow-label { color: var(--color-accent); font-weight: 700; }
            .flow-connector { flex: 1 1 auto; height: 2px; background-color: var(--color-border); margin: 7px 0.5rem 0 0.5rem; min-width: 24px; }
            .flow-connector.done { background-color: var(--color-accent); }

            /* Case header bar (Investigation view) */
            .case-header {
                border-bottom: 2px solid var(--color-text);
                padding-bottom: 0.75rem;
                margin-bottom: 0.75rem;
            }
            .case-header-id { font-size: 1.4rem; font-weight: 700; color: var(--color-text); }
            .case-header-meta { font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.15rem; }

            /* AI Assessment strip - compact verdict row. Tier border follows the severity ramp:
               low = neutral border, medium = accent, high = black (a critical-alert signal). */
            .assessment-strip {
                background-color: var(--color-bg);
                border: 1px solid var(--color-border);
                border-left: 4px solid var(--color-border);
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                margin-bottom: 1rem;
            }
            .assessment-strip.tier-high   { border-left-color: var(--color-text); }
            .assessment-strip.tier-medium { border-left-color: var(--color-accent); }
            .assessment-strip.tier-low    { border-left-color: var(--color-border); }
            .assessment-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-muted); }
            .assessment-value { font-size: 1.05rem; font-weight: 600; color: var(--color-text); margin-top: 0.1rem; }
            .assessment-summary { font-size: 0.92rem; color: var(--color-text); margin-top: 0.6rem; line-height: 1.5; }

            /* Fraud indicator tags */
            .tag-pill {
                display: inline-block;
                background-color: var(--color-surface);
                border: 1px solid var(--color-border);
                color: var(--color-text);
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
                background-color: var(--color-surface);
            }
            .decision-record-note { font-size: 0.88rem; color: var(--color-text); margin-top: 0.4rem; line-height: 1.5; }
            .decision-record-meta { font-size: 0.78rem; color: var(--color-text-muted); margin-top: 0.5rem; }
        </style>
    """, unsafe_allow_html=True)
