# --- STREAMLIT CLOUD CHROMADB COMPATIBILITY PATCH ---
import sys
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass
# ----------------------------------------------------

# Purpose: Main application entry point for the Agentic Fraud Investigation Copilot UI.
# Orchestrates sidebar routing, layout templates configuration, and global logs.
from datetime import datetime
import logging
import streamlit as st
from ui.styles import apply_custom_css
from ui.pages import (
    render_role_gate,
    render_case_queue_view,
    render_investigation_view,
    render_analytics_view,
    render_manager_queue_view,
)
from ui.components import ANALYST_NAME, FRAUD_MANAGER_NAME, ANALYST_LOCATION

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ui.main_app")

ROLE_NAV_OPTIONS = {
    ANALYST_NAME: ["Home", "Investigation", "Analytics"],
    FRAUD_MANAGER_NAME: ["Manager Queue", "Investigation", "Analytics"],
}

def main() -> None:
    """Configures main workspace layout wrappers, tracking sidebars navigation matrices options."""
    role_chosen = "current_role" in st.session_state
    st.set_page_config(
        page_title="Agentic Fraud Investigation Copilot",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded" if role_chosen else "collapsed"
    )

    apply_custom_css()

    # Gate the app behind a role choice on first load; the sidebar/nav below only renders
    # once a role is picked (render_role_gate stages current_role + nav_radio and reruns).
    if not role_chosen:
        render_role_gate()
        return

    # A widget's session_state value can't be mutated after it's instantiated in the same run,
    # so cross-view navigation (e.g. the queue's "Open" button) stages the target here and this
    # runs before the radio widget below is created.
    if "_pending_nav" in st.session_state:
        st.session_state["nav_radio"] = st.session_state.pop("_pending_nav")

    st.sidebar.markdown(
        '<div class="sidebar-brand">Agentic Fraud Investigation Copilot</div>',
        unsafe_allow_html=True,
    )
    current_role = st.session_state["current_role"]

    nav_options = ROLE_NAV_OPTIONS[current_role]
    if st.session_state.get("nav_radio") not in nav_options:
        st.session_state["nav_radio"] = nav_options[0]

    navigation_route = st.sidebar.radio("Navigate", nav_options, key="nav_radio")

    st.sidebar.write("---")
    if st.sidebar.button("Logout", use_container_width=True):
        # Session-scoped login/nav state only - case data lives in case_store.db and is untouched.
        for key in ("current_role", "nav_radio", "selected_case_id", "_pending_nav"):
            st.session_state.pop(key, None)
        st.rerun()
    st.sidebar.caption("Compliance Protection Enforced")

    _, identity_col = st.columns([4, 1])
    with identity_col:
        st.markdown(f"""
            <div class="identity-header">
                <div class="identity-name">{current_role}</div>
                <div class="identity-meta">{ANALYST_LOCATION} · {datetime.now().strftime('%B %d, %Y')}</div>
            </div>
        """, unsafe_allow_html=True)

    if navigation_route == "Home":
        logger.info("Rendering case queue view.")
        render_case_queue_view()
    elif navigation_route == "Manager Queue":
        logger.info("Rendering Fraud Manager approval queue view.")
        render_manager_queue_view()
    elif navigation_route == "Investigation":
        logger.info(f"Rendering investigation workspace view for role: {current_role}.")
        render_investigation_view(current_role)
    elif navigation_route == "Analytics":
        logger.info("Rendering analytics view.")
        render_analytics_view()

if __name__ == "__main__":
    main()
