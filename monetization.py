import streamlit as st
import config

def check_search_limit():
    """
    Enforces the 'One Search' free trial policy.
    Returns True if user is allowed to proceed, False if they hit the paywall.
    """
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0
        
    if st.session_state.search_count >= config.FREE_SEARCH_LIMIT:
        return False
    
    return True

def increment_search_count():
    if 'search_count' not in st.session_state:
        st.session_state.search_count = 0
    st.session_state.search_count += 1

def show_paywall():
    st.error("🚨 Trial Limit Reached")
    st.markdown("""
    ### Upgrade to AI-Premium
    You have exhausted your **One Search** free trial. 
    
    **Unlock full access to:**
    - Unlimited Fraud Scans
    - Advanced Reasoning Artifacts
    - Real-time Velocity Checks
    
    [Subscribe Now](#) (Simulated Link)
    """)
    st.stop()
