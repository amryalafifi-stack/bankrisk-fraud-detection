import streamlit as st
import pandas as pd
import data_processor
import fraud_engine

# Page Configuration
st.set_page_config(
    page_title="AI Data Analyst | Fraud Detection",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL DARK THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* Subtle Grid Background */
    @keyframes gridMove {
        0% { background-position: 0 0; }
        100% { background-position: 40px 40px; }
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    @keyframes slideUp {
        0% { transform: translateY(10px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background - Professional Dark */
    .stApp {
        background: #0a0a0f !important;
        background-image: 
            linear-gradient(rgba(100, 120, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(100, 120, 255, 0.02) 1px, transparent 1px) !important;
        background-size: 40px 40px;
        animation: gridMove 30s linear infinite;
        color: #FFFFFF !important;
    }
    
    /* Sidebar - Professional Gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            #0f1419 0%, 
            #0a0a0f 50%,
            #12141a 100%) !important;
        border-right: 1px solid rgba(100, 120, 255, 0.15);
        box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label {
        color: #E0E6FF !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
    }

    /* Professional Cards */
    .metric-card {
        background: linear-gradient(135deg, 
            rgba(100, 120, 255, 0.08) 0%, 
            rgba(140, 100, 255, 0.08) 100%),
            #15151f !important;
        padding: 28px;
        border-radius: 16px;
        border: 1px solid rgba(100, 120, 255, 0.2);
        position: relative;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 24px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.03);
        animation: slideUp 0.4s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: rgba(100, 120, 255, 0.4);
        box-shadow: 
            0 8px 32px rgba(100, 120, 255, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6478FF 0%, #8C64FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #A0A8C0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6478FF 0%, #8C64FF 100%);
        color: #FFFFFF;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 
            0 4px 16px rgba(100, 120, 255, 0.3),
            0 2px 8px rgba(0, 0, 0, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 6px 24px rgba(100, 120, 255, 0.4),
            0 4px 12px rgba(0, 0, 0, 0.3);
    }

    /* Expander - Professional Style */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(100, 120, 255, 0.08), rgba(140, 100, 255, 0.08));
        border: 1px solid rgba(100, 120, 255, 0.2);
        border-radius: 10px;
        color: #E0E6FF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    /* Headers - Professional */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        background: linear-gradient(135deg, #6478FF 0%, #8C64FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        font-weight: 700;
    }
    
    /* Hide Default UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

import plotly.express as px
import plotly.graph_objects as go

def display_dashboard_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div style="animation: slideUp 0.5s ease;">
            <h1 style="font-size: 3rem; margin-bottom: 0;">AI DATA ANALYST</h1>
            <p style="color: #A0A8C0; font-size: 1.1rem; font-family: 'Inter', sans-serif; letter-spacing: 1px; font-weight: 500;">
                Fraud Detection Engine <span style="color: #8C64FF;">v2.0</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: right; padding-top: 20px;">
            <span style="font-weight: 600; color: #6478FF; font-family: 'Space Grotesk', sans-serif;">● System Online</span><br>
            <span style="font-size: 0.9rem; color: #A0A8C0;">AI Engine Active</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border: 1px solid rgba(100, 120, 255, 0.15); margin: 20px 0;'>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="font-family: 'Space Grotesk', sans-serif; color: #E0E6FF; font-weight: 700; letter-spacing: 1px; font-size: 1.5rem;">Control Panel</h2>
        <div style="width: 40px; height: 3px; background: linear-gradient(90deg, #6478FF, #8C64FF); margin: 10px auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Data (CSV)", type="csv")
    column_mapping = {}
    
    if uploaded_file:
        try:
            import pandas as pd
            uploaded_file.seek(0)
            preview_df = pd.read_csv(uploaded_file, nrows=1)
            uploaded_file.seek(0)
            
            with st.expander("⚙ Column Mapper"):
                st.caption("Map CSV columns to system fields.")
                cols = list(preview_df.columns)
                
                # Auto-select helpers
                def get_index(options, likely_names):
                    for name in likely_names:
                        for i, opt in enumerate(options):
                            if name.lower() in opt.lower(): return i
                    return 0

                column_mapping['amount'] = st.selectbox("Amount ($)", cols, index=get_index(cols, ['amt', 'amount', 'price', 'value']))
                column_mapping['customer_id'] = st.selectbox("Customer ID", cols, index=get_index(cols, ['cc_num', 'card', 'user', 'id']))
                column_mapping['category'] = st.selectbox("Category", cols, index=get_index(cols, ['category', 'type']))
                
                col_merch = st.selectbox("Merchant", ["None"] + cols, index=get_index(["None"] + cols, ['merchant', 'vendor']) )
                column_mapping['merchant'] = col_merch if col_merch != "None" else None
                
                col_time = st.selectbox("Timestamp", ["None"] + cols, index=get_index(["None"] + cols, ['time', 'date', 'ts']))
                column_mapping['timestamp'] = col_time if col_time != "None" else None

        except Exception as e:
            st.error(f"Error previewing file: {e}")
            
    st.divider()
    
    # System Status
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, rgba(100, 120, 255, 0.08), rgba(140, 100, 255, 0.08)); border-radius: 10px; border: 1px solid rgba(100, 120, 255, 0.2);">
        <p style="color: #6478FF; font-family: 'Space Grotesk', sans-serif; margin: 0; font-size: 0.9rem; font-weight: 600;">● Unlimited Access</p>
        <p style="color: #A0A8C0; font-size: 0.8rem; margin: 5px 0 0 0;">AI Engine Ready</p>
    </div>
    """, unsafe_allow_html=True)

# --- Main App Logic ---
display_dashboard_header()

if st.button("▶ Initiate Analysis", use_container_width=True, type="primary"):
    
    with st.spinner("Processing data and analyzing fraud patterns..."):
        # Load Data
        df = data_processor.load_data(uploaded_file, column_mapping if uploaded_file else None)
        
        # Fraud Analysis
        analyzed_df = fraud_engine.run_fraud_scan(df)
        
        # --- Metrics Row (HTML Cards) ---
        total_tx = len(analyzed_df)
        flagged_df = analyzed_df[analyzed_df['is_flagged']]
        flagged_tx = len(flagged_df)
        fraud_exposure = flagged_df['amount'].sum()
        risk_rate = (flagged_tx / total_tx) * 100 if total_tx > 0 else 0
        
        m1, m2, m3, m4 = st.columns(4)
        
        def metric_html(label, value, delta=None):
            delta_html = ""
            if delta:
                color = "delta-neg" if "-" in delta or "%" in delta else "delta-pos" # Heuristic styling
                delta_html = f'<div class="metric-delta {color}">{delta}</div>'
            return f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                {delta_html}
            </div>
            """
            
        with m1: st.markdown(metric_html("Total Volume", f"{total_tx:,}"), unsafe_allow_html=True)
        with m2: st.markdown(metric_html("Flagged Risks", f"{flagged_tx}", f"{risk_rate:.1f}% Rate"), unsafe_allow_html=True)
        with m3: st.markdown(metric_html("Fraud Exposure", f"${fraud_exposure:,.0f}", "Potential Loss"), unsafe_allow_html=True)
        with m4:
             top_risk_cat = flagged_df['category'].mode()[0] if not flagged_df.empty else "N/A"
             st.markdown(metric_html("Top Risk Cat", top_risk_cat), unsafe_allow_html=True)
             
        st.markdown("---")
        
        # --- Interactive Charts Row ---
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader("Transaction Analysis (Amount vs. Time)")
            # Create Scatter Plot
            # Create a mock time index if timestamp isn't datetime or is missing
            plot_df = analyzed_df.copy()
            if 'timestamp' in plot_df.columns:
                 plot_df['timestamp'] = pd.to_datetime(plot_df['timestamp'], errors='coerce')
                 plot_df = plot_df.sort_values('timestamp')
            else:
                 plot_df['timestamp'] = plot_df.index
            
            # Subsample for plotting performance if too large
            if len(plot_df) > 2000:
                plot_df = plot_df.sample(2000)
            
            fig_scatter = px.scatter(
                plot_df, 
                x="timestamp", 
                y="amount", 
                color="is_flagged",
                color_discrete_map={True: '#F50057', False: '#00E5FF'},
                hover_data=['merchant', 'category', 'risk_score'],
                title="Transaction Timeline"
            )
            fig_scatter.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Poppins", color="#FFFFFF")
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with c2:
            st.subheader("Risk by Category")
            if not flagged_df.empty:
                cat_counts = flagged_df['category'].value_counts().reset_index()
                cat_counts.columns = ['category', 'count']
                fig_bar = px.bar(
                    cat_counts.head(5), 
                    x='count', 
                    y='category', 
                    orientation='h',
                    color='count',
                    color_continuous_scale='RdPu' # Pink/Purple gradient
                )
                fig_bar.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Poppins", color="#FFFFFF")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No flagged transactions to categorize.")

        # --- Detailed Audit List ---
        st.subheader("High-Priority Audit Queue")
        
        # Sort by risk score descending
        audit_queue = flagged_df.sort_values('risk_score', ascending=False).head(50)
        
        if audit_queue.empty:
            st.success("✓ Clean Scan. No high-risk transactions found.")
        else:
            for i, row in audit_queue.iterrows():
                # Custom HTML Expander Summary for better styling
                with st.expander(f"● ${row['amount']:.2f} | {row['merchant']} (Risk Score: {row.get('risk_score', 'N/A')})"):
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.markdown(f"**Reasoning:** *{row['reasoning']}*")
                        st.markdown(f"**Token:** `{row['customer_id_token']}`")
                    with c_b:
                         st.markdown(f"**Category:** {row['category']}")
                         st.markdown(f"**Timestamp:** {row['timestamp']}")
                         if row.get('is_fraud', 0) == 1:
                             st.error("MATCH: Confirmed Fraud Pattern in Database")

else:
    # Empty State / Landing
    st.markdown("""
    <div style="text-align: center; padding: 60px; background: linear-gradient(135deg, rgba(100, 120, 255, 0.05), rgba(140, 100, 255, 0.05)); border-radius: 16px; margin-top: 30px; border: 1px solid rgba(100, 120, 255, 0.2); box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);">
        <h2 style="color: #6478FF; font-weight: 700; font-family: 'Space Grotesk', sans-serif; letter-spacing: -0.5px; font-size: 2rem;">System Ready</h2>
        <p style="color: #E0E6FF; font-size: 1.05rem; margin-top: 15px; font-weight: 400;">Upload your dataset or click <span style="color: #8C64FF; font-weight: 600;">Initiate Analysis</span> to use demo data</p>
        <p style="color: #A0A8C0; font-size: 0.9rem; margin-top: 10px;">AI-Powered Fraud Detection | Unlimited Access</p>
    </div>
    """, unsafe_allow_html=True)

