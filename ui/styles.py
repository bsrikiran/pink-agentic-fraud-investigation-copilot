"""
Purpose: Defines custom UI presentation styles and banking operational aesthetic themes.
"""
import streamlit as st

def apply_custom_css() -> None:
    """Injects high-contrast typography, minimalist border accents, and neutral background scales."""
    st.markdown("""
        <style>
            /* Global Application Alignment and Typography */
            .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
            h1, h2, h3 { color: #0F172A !important; font-family: 'Inter', -apple-system, sans-serif; }
            
            /* Operations Metric Card Cards Design Layouts */
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
            
            /* High Contrast Recommendation Alerts Banner Matrix */
            .rec-banner {
                padding: 1rem;
                border-left: 5px solid #0284C7;
                background-color: #F0F9FF;
                border-radius: 4px;
                margin-bottom: 1.5rem;
            }
            .rec-text { font-size: 1.15rem; font-weight: 600; color: #0369A1; }
        </style>
    """, unsafe_allow_html=True)
