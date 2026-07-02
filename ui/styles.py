"""
Purpose: Defines custom UI presentation styles and banking operational aesthetic themes.
"""
import streamlit as st

def apply_custom_css() -> None:
    """Injects institutional typography, brand color tokens, and status-badge color coding.
    Semantic palette: #FFFCFB background (canvas), #F5F7FA surface (cards, tables, inputs,
    headers), #D7DCE5 border, #2F2FE4 primary (buttons, links, active states), #233044 secondary
    - a dark slate used for the sidebar/nav chrome, #080616 text, #6E7785 muted text, plus
    dedicated #16A34A success, #F59E0B warning, and #DC2626 danger colors for severity/status
    signal (high/declined/escalated = danger, medium/review/returned = warning, low/approved/
    resolved = success)."""
    st.markdown("""
        <style>
            :root {
                --color-bg: #FFFCFB;
                --color-surface: #F5F7FA;
                --color-border: #D7DCE5;

                /* Primary - buttons, links, active/selected states, progress indicators */
                --color-primary: #2F2FE4;
                --color-primary-hover: #2626B6;
                --color-primary-tint: rgba(47, 47, 228, 0.10);
                --color-primary-tint-strong: rgba(47, 47, 228, 0.18);

                /* Secondary - dark slate sidebar/nav chrome, pairs with light secondary-text */
                --color-secondary: #233044;
                --color-secondary-text: #FFFCFB;
                --color-secondary-muted: rgba(255, 252, 251, 0.65);
                --color-secondary-border: rgba(255, 252, 251, 0.18);
                --color-secondary-active-bg: rgba(47, 47, 228, 0.35);

                --color-text: #080616;
                --color-text-muted: #6E7785;

                /* Semantic status colors */
                --color-success: #16A34A;
                --color-success-tint: rgba(22, 163, 74, 0.12);
                --color-warning: #F59E0B;
                --color-warning-tint: rgba(245, 158, 11, 0.14);
                --color-danger: #DC2626;
                --color-danger-tint: rgba(220, 38, 38, 0.10);
            }

            /* Global Application Alignment and Typography */
            [data-testid="stHeader"] { height: 1.5rem !important; min-height: 1.5rem !important; background-color: var(--color-bg) !important; }
            [data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; padding-bottom: 2rem; }
            [data-testid="stAppViewContainer"] { background-color: var(--color-bg); }
            h1, h2, h3 { color: var(--color-text) !important; font-family: 'Inter', -apple-system, sans-serif; }
            body, p, .stMarkdown, [data-testid="stMarkdownContainer"] { color: var(--color-text); }
            a, a:visited { color: var(--color-primary); }
            a:hover { color: var(--color-primary-hover); }

            /* Input backgrounds - primary background tone, distinct from the surface chrome
               (sidebar/KPI cards/headers) so form fields read as part of the canvas */
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stNumberInput"] input,
            [data-testid="stDateInput"] input,
            [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                background-color: var(--color-bg) !important;
                border-color: var(--color-border) !important;
            }

            /* Sidebar - dark secondary (slate) nav chrome */
            [data-testid="stSidebar"] {
                background-color: var(--color-secondary) !important;
                border-right: 1px solid var(--color-secondary-border);
            }
            [data-testid="stSidebar"] * { color: var(--color-secondary-text); }
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 { color: var(--color-secondary-text) !important; }
            [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color: var(--color-secondary-muted) !important; }
            [data-testid="stSidebar"] hr { border-top: 1px solid var(--color-secondary-border); }
            /* Native radio: active nav item gets the primary ring + tint, not a full-width fill */
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
                background-color: transparent !important;
                border: 1px solid var(--color-secondary-muted) !important;
                border-radius: 50%;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label > div:first-child > div {
                background-color: var(--color-primary) !important;
            }
            [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) > div:first-child {
                border-color: var(--color-primary) !important;
                background-color: var(--color-secondary-active-bg) !important;
            }

            /* Native alert banners (st.info/warning/error/success) - dedicated semantic colors */
            [data-testid="stAlertContainer"] { background-color: transparent !important; }
            [data-testid="stAlertContentInfo"] {
                background-color: var(--color-surface) !important;
                color: var(--color-text-muted) !important;
                border-left: 3px solid var(--color-border);
                border-radius: 4px;
            }
            [data-testid="stAlertContentWarning"] {
                background-color: var(--color-warning-tint) !important;
                color: var(--color-warning) !important;
                border-left: 3px solid var(--color-warning);
                border-radius: 4px;
            }
            [data-testid="stAlertContentError"] {
                background-color: var(--color-danger-tint) !important;
                color: var(--color-danger) !important;
                border-left: 3px solid var(--color-danger);
                border-radius: 4px;
                font-weight: 600;
            }
            [data-testid="stAlertContentSuccess"] {
                background-color: var(--color-success-tint) !important;
                color: var(--color-success) !important;
                border-left: 3px solid var(--color-success);
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

            /* Buttons: primary = brand primary (native theme), secondary = primary outline */
            [data-testid="stBaseButton-primary"] { background-color: var(--color-primary) !important; border-color: var(--color-primary) !important; color: #FFFFFF !important; }
            [data-testid="stBaseButton-primary"] p { color: #FFFFFF !important; }
            [data-testid="stBaseButton-primary"]:hover { background-color: var(--color-primary-hover) !important; border-color: var(--color-primary-hover) !important; }
            [data-testid="stBaseButton-secondary"] { color: var(--color-primary) !important; border-color: var(--color-primary) !important; background-color: transparent !important; }
            [data-testid="stBaseButton-secondary"]:hover { color: var(--color-primary-hover) !important; border-color: var(--color-primary-hover) !important; background-color: var(--color-primary-tint) !important; }

            /* AI System Status panel: multiple check rows + a last-refreshed footer.
               "OK" reads success (green), "Down" escalates to danger (red). */
            .status-panel {
                border: 1px solid var(--color-border);
                border-radius: 4px;
                padding: 0.75rem 1rem;
                background-color: var(--color-surface);
                margin-bottom: 1.25rem;
            }
            .status-row { display: flex; align-items: center; gap: 0.55rem; font-size: 0.85rem; color: var(--color-text-muted); padding: 0.2rem 0; }
            .status-row.down { color: var(--color-danger); font-weight: 600; }
            .status-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
            .status-dot.ok { background-color: var(--color-success); }
            .status-dot.down { background-color: var(--color-danger); }
            .status-panel-footer {
                font-size: 0.75rem; color: var(--color-text-muted); margin-top: 0.4rem;
                padding-top: 0.4rem; border-top: 1px solid var(--color-border);
            }

            /* Metric Cards (Analytics KPIs) - surface with a thin primary top-stripe;
               the stripe marks "this is a KPI worth attention" without coloring the number itself */
            .metric-container {
                background-color: var(--color-surface);
                border: 1px solid var(--color-border);
                border-top: 3px solid var(--color-primary);
                border-radius: 6px;
                padding: 1.25rem;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0,0,0,0.04);
            }
            .metric-value { font-size: 2.25rem; font-weight: 700; color: var(--color-text); margin: 0.5rem 0; }
            .metric-label { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--color-text-muted); }

            /* Status / Priority / Risk badges - dedicated semantic colors:
               high/declined = danger, medium/needs-review/returned = warning,
               low/approved = success, neutral/new = muted surface, closed = solid secondary. */
            .badge {
                display: inline-block;
                padding: 0.15rem 0.6rem;
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 600;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }
            .badge-high       { background-color: var(--color-danger-tint); color: var(--color-danger); border: 1px solid rgba(220, 38, 38, 0.30); }
            .badge-medium     { background-color: var(--color-warning-tint); color: var(--color-warning); }
            .badge-low        { background-color: var(--color-success-tint); color: var(--color-success); }
            .badge-neutral    { background-color: var(--color-surface); color: var(--color-text-muted); border: 1px solid var(--color-border); }
            .badge-approved   { background-color: var(--color-success-tint); color: var(--color-success); }
            .badge-declined   { background-color: var(--color-danger-tint); color: var(--color-danger); border: 1px solid rgba(220, 38, 38, 0.30); }
            .badge-escalated  { background-color: var(--color-danger); color: var(--color-bg); font-weight: 700; }
            .badge-review     { background-color: var(--color-warning-tint); color: var(--color-warning); }
            .badge-returned   { background-color: var(--color-warning-tint); color: var(--color-warning); }
            .badge-closed     { background-color: var(--color-secondary); color: var(--color-secondary-text); }

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
                border-top: 4px solid var(--color-primary);
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

            /* Case lifecycle flow stepper (Investigation view) - progress = primary */
            .flow-stepper { display: flex; align-items: flex-start; margin: 0.25rem 0 1.75rem 0; }
            .flow-step { display: flex; flex-direction: column; align-items: center; gap: 0.5rem; flex-shrink: 0; }
            .flow-dot {
                width: 16px; height: 16px; border-radius: 50%;
                border: 2px solid var(--color-border); background-color: var(--color-bg); box-sizing: border-box;
            }
            .flow-step.done .flow-dot { background-color: var(--color-primary); border-color: var(--color-primary); }
            .flow-step.current .flow-dot { background-color: var(--color-bg); border-color: var(--color-primary); box-shadow: 0 0 0 3px var(--color-primary-tint-strong); }
            .flow-label { font-size: 0.78rem; color: var(--color-text-muted); white-space: nowrap; }
            .flow-step.done .flow-label { color: var(--color-text); font-weight: 500; }
            .flow-step.current .flow-label { color: var(--color-primary); font-weight: 700; }
            .flow-connector { flex: 1 1 auto; height: 2px; background-color: var(--color-border); margin: 7px 0.5rem 0 0.5rem; min-width: 24px; }
            .flow-connector.done { background-color: var(--color-primary); }

            /* Case header bar (Investigation view) */
            .case-header {
                border-bottom: 2px solid var(--color-text);
                padding-bottom: 0.75rem;
                margin-bottom: 0.75rem;
            }
            .case-header-id { font-size: 1.4rem; font-weight: 700; color: var(--color-text); }
            .case-header-meta { font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.15rem; }

            /* AI Assessment strip - compact verdict row. Tier border follows the semantic ramp:
               low = success, medium = warning, high = danger. */
            .assessment-strip {
                background-color: var(--color-bg);
                border: 1px solid var(--color-border);
                border-left: 4px solid var(--color-border);
                border-radius: 4px;
                padding: 0.9rem 1.1rem;
                margin-bottom: 1rem;
            }
            .assessment-strip.tier-high   { border-left-color: var(--color-danger); }
            .assessment-strip.tier-medium { border-left-color: var(--color-warning); }
            .assessment-strip.tier-low    { border-left-color: var(--color-success); }
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

            /* Queue tables (Work Queue / Approval Queue / Portfolio) are wide, many-column
               layouts that would otherwise squeeze illegibly on a phone. Keep their natural
               column widths and let the row scroll horizontally instead. */
            .st-key-case-queue-table [data-testid="stHorizontalBlock"],
            .st-key-manager-queue-table [data-testid="stHorizontalBlock"],
            .st-key-portfolio-table [data-testid="stHorizontalBlock"] {
                flex-wrap: nowrap;
            }
            .st-key-case-queue-table [data-testid="stColumn"],
            .st-key-manager-queue-table [data-testid="stColumn"],
            .st-key-portfolio-table [data-testid="stColumn"] {
                min-width: 110px;
            }

            /* Mobile phones */
            @media (max-width: 768px) {
                [data-testid="stMainBlockContainer"] { padding-left: 1rem !important; padding-right: 1rem !important; }

                .st-key-case-queue-table,
                .st-key-manager-queue-table,
                .st-key-portfolio-table {
                    overflow-x: auto;
                }
                .st-key-case-queue-table [data-testid="stHorizontalBlock"],
                .st-key-manager-queue-table [data-testid="stHorizontalBlock"],
                .st-key-portfolio-table [data-testid="stHorizontalBlock"] {
                    min-width: 780px;
                }

                .role-gate-title { font-size: 1.4rem; }
                .role-gate { margin: 2vh 0 1.5rem 0; }
                .role-card { padding: 1.25rem 1rem 1rem; min-height: unset; }

                .metric-value { font-size: 1.6rem; }
                .metric-container { padding: 0.85rem; }

                .case-header-id { font-size: 1.1rem; }

                /* Lifecycle stepper: scroll instead of compressing the stage labels */
                .flow-stepper { overflow-x: auto; padding-bottom: 0.25rem; }
                .flow-label { font-size: 0.7rem; }

                .identity-header { text-align: left; margin-top: 0.5rem; }
            }
        </style>
    """, unsafe_allow_html=True)
