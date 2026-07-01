"""
Purpose: Main application entry point for the Agentic Fraud Investigation Copilot UI.
Orchestrates sidebar routing, layout templates configuration, and global logs.
"""
import logging
import streamlit as st
from ui.styles import apply_custom_css
from ui.pages import render_home_view, render_investigation_pipeline_view, render_metrics_dashboard_view

# Configure unified localized basic interface tracking streams logging routines safely
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ui.main_app")

def main() -> None:
    """Configures main workspace layout wrappers, tracking sidebars navigation matrices options."""
    st.set_page_config(
        page_title="Fraud Operations Copilot Dashboard",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Injects corporate theme styling metrics
    apply_custom_css()
    
    # Sidebar Operations Module Navigation Panel Control Row Matrix
    st.sidebar.markdown("### 🎛️ Operations Control Panel")
    navigation_route = st.sidebar.radio(
        "Navigate Workspace Paths:",
        ["Home Console Overview", "Interactive Evaluation Workbench", "Global Analytics Metrics"]
    )
    
    st.sidebar.write("---")
    st.sidebar.caption("🔒 Compliance Protection Enforced")
    st.sidebar.caption("Role Profile: Senior Fraud Risk Analyst")
    
    # Structural Page Views Content Execution Tree Routing Mapping Contexts
    if navigation_route == "Home Console Overview":
        logger.info("Rendering Home Overview Console page state view layout matrices.")
        render_home_view()
    elif navigation_route == "Interactive Evaluation Workbench":
        logger.info("Launching Interactive Evaluation Workbench workflow execution engines.")
        render_investigation_pipeline_view()
    elif navigation_route == "Global Analytics Metrics":
        logger.info("Extracting portfolio registers tables to generate visualizations dashboards data columns.")
        render_metrics_dashboard_view()

if __name__ == "__main__":
    main()
