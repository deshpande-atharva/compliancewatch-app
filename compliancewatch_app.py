# compliancewatch_clean.py - Clean Modern Design
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import time
import numpy as np

# Page config
st.set_page_config(
    page_title="ComplianceWatch | Pharmaceutical Monitoring",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Clean, modern CSS with proper contrast
st.markdown("""
<style>
    /* Import clean fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f7f8fa;
        --bg-dark: #1e1e2e;
        --text-primary: #2d3436;
        --text-secondary: #636e72;
        --text-light: #b2bec3;
        --accent-primary: #4834d4;
        --accent-secondary: #6c5ce7;
        --accent-light: #a29bfe;
        --success: #00b894;
        --warning: #fdcb6e;
        --danger: #d63031;
        --info: #74b9ff;
        --border: #dfe6e9;
    }
    
    /* Main app background */
    .stApp {
        background-color: var(--bg-secondary);
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem;
        max-width: 1400px;
    }
    
    /* Headers with proper visibility */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* All text elements */
    p, span, div, label, .stMarkdown {
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-dark);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5 {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Buttons with subtle styling */
    .stButton > button {
        background-color: var(--accent-primary);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.2s;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background-color: var(--accent-secondary);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(72, 52, 212, 0.15);
    }
    
    /* Metrics with clean styling */
    [data-testid="metric-container"] {
        background: var(--bg-primary);
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-size: 0.875rem;
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--text-primary) !important;
        font-size: 1.875rem;
        font-weight: 600;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: var(--success) !important;
        font-size: 0.875rem;
    }
    
    /* Tabs with modern design */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-secondary) !important;
        font-weight: 500;
        padding: 0.75rem 1rem;
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        margin-bottom: -2px;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: var(--text-primary) !important;
        background-color: var(--bg-secondary);
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary);
    }
    
    /* Alert styling */
    .stAlert > div {
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid;
        font-size: 0.95rem;
    }
    
    .stInfo > div {
        background-color: #e3f2fd;
        color: #1565c0;
        border-color: #90caf9;
    }
    
    .stSuccess > div {
        background-color: #e8f5e9;
        color: #2e7d32;
        border-color: #81c784;
    }
    
    .stWarning > div {
        background-color: #fff3e0;
        color: #e65100;
        border-color: #ffb74d;
    }
    
    .stError > div {
        background-color: #ffebee;
        color: #c62828;
        border-color: #ef5350;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 4px;
    }
    
    /* In main area */
    .main .stTextInput > div > div > input,
    .main .stSelectbox > div > div > select {
        background-color: white !important;
        border: 1px solid var(--border) !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 1px var(--accent-primary);
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: var(--accent-primary);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        color: var(--text-primary) !important;
        border: 1px solid var(--border);
        border-radius: 6px;
        font-weight: 500;
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--border);
        border-top: none;
        background-color: white;
    }
    
    /* Columns */
    [data-testid="column"] > div {
        background-color: transparent;
    }
    
    /* Dataframe */
    .dataframe {
        font-size: 0.9rem;
    }
    
    .dataframe thead tr th {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        text-align: left;
    }
    
    .dataframe tbody tr td {
        color: var(--text-primary) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: var(--accent-primary);
    }
    
    /* Custom card styling */
    .info-card {
        background: white;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .info-card h4 {
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .info-card p {
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure text is always visible */
    .element-container {
        color: var(--text-primary) !important;
    }
    
    .stMarkdown div {
        color: inherit !important;
    }
    
    /* Fix for metric delta colors */
    [data-testid="metric-delta"] svg {
        fill: currentColor;
    }
    
    .metric-delta-negative {
        color: var(--danger) !important;
    }
    
    .metric-delta-positive {
        color: var(--success) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💊 ComplianceWatch")
st.markdown("**Real-time Pharmaceutical Adverse Event Monitoring System**")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("# ⚙️ Configuration")
    st.markdown("---")
    
    # Drug input
    drug_name = st.text_input(
        "**Target Drug**",
        placeholder="e.g., Ozempic",
        help="Enter drug name to monitor"
    )
    
    # Data sources
    data_sources = st.multiselect(
        "**Data Sources**",
        ["Reddit", "Twitter/X", "FDA FAERS", "Medical Forums", "Patient Reports"],
        default=["Reddit", "FDA FAERS"]
    )
    
    # Time range
    time_range = st.selectbox(
        "**Time Period**",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
        index=1
    )
    
    # Severity threshold
    severity_threshold = st.slider(
        "**Severity Threshold**",
        min_value=1,
        max_value=10,
        value=5,
        help="Minimum severity level for alerts"
    )
    
    st.markdown("---")
    
    # Monitor button
    if st.button("**Start Monitoring**", use_container_width=True, type="primary"):
        st.session_state.monitoring = True
        st.success("✓ Monitoring Active")
    
    if st.session_state.monitoring:
        st.markdown("---")
        st.markdown("### 📊 Status")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", "Active", "Live")
        with col2:
            st.metric("Health", "100%", "Good")

# Main content
if st.session_state.monitoring and drug_name:
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Events",
            value="1,247",
            delta="+23 today"
        )
    
    with col2:
        st.metric(
            label="Critical Alerts",
            value="3",
            delta="Urgent",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Detection Speed",
            value="48h",
            delta="Faster"
        )
    
    with col4:
        st.metric(
            label="Accuracy",
            value="94.7%",
            delta="+2.1%"
        )
    
    with col5:
        st.metric(
            label="Coverage",
            value="Global",
            delta="100%"
        )
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🔔 Alerts", "🤖 AI Analysis", "🌍 Geographic", "📈 Predictions"])
    
    with tab1:
        st.header("Dashboard Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Severity Distribution")
            
            # Bar chart
            severity_data = pd.DataFrame({
                'Level': ['Critical', 'High', 'Medium', 'Low'],
                'Count': [3, 12, 45, 187],
                'Color': ['#d63031', '#fdcb6e', '#74b9ff', '#00b894']
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=severity_data['Count'],
                    y=severity_data['Level'],
                    orientation='h',
                    marker_color=severity_data['Color'],
                    text=severity_data['Count'],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
                yaxis=dict(showgrid=False),
                margin=dict(l=0, r=50, t=0, b=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Source Distribution")
            
            # Pie chart
            source_data = pd.DataFrame({
                'Source': ['Reddit', 'FDA', 'Twitter', 'Forums'],
                'Count': [89, 67, 54, 37]
            })
            
            fig2 = go.Figure(data=[go.Pie(
                labels=source_data['Source'],
                values=source_data['Count'],
                hole=0.4,
                marker_colors=['#4834d4', '#6c5ce7', '#a29bfe', '#74b9ff']
            )])
            
            fig2.update_layout(
                height=300,
                showlegend=True,
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Trend chart
        st.subheader("30-Day Trend")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Events': np.cumsum(np.random.randn(30) * 10 + 50)
        })
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Events'],
            mode='lines+markers',
            name='Events',
            line=dict(color='#4834d4', width=2),
            marker=dict(size=4)
        ))
        
        fig3.update_layout(
            height=300,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            hovermode='x'
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.header("Active Alerts")
        
        # Alert list
        alerts = [
            {"severity": "Critical", "message": f"Severe reactions to {drug_name}", "time": "2 min ago", "conf": 95},
            {"severity": "High", "message": f"Unusual pattern for {drug_name}", "time": "15 min ago", "conf": 87},
            {"severity": "Medium", "message": f"Increased reports for {drug_name}", "time": "1 hour ago", "conf": 76},
            {"severity": "Low", "message": f"Minor events for {drug_name}", "time": "3 hours ago", "conf": 62}
        ]
        
        for alert in alerts:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                if alert["severity"] == "Critical":
                    st.error(f"🔴 **{alert['severity']}**: {alert['message']}")
                elif alert["severity"] == "High":
                    st.warning(f"🟠 **{alert['severity']}**: {alert['message']}")
                elif alert["severity"] == "Medium":
                    st.info(f"🟡 **{alert['severity']}**: {alert['message']}")
                else:
                    st.success(f"🟢 **{alert['severity']}**: {alert['message']}")
            
            with col2:
                st.markdown(f"**Confidence:** {alert['conf']}%")
            
            with col3:
                st.markdown(f"_{alert['time']}_")
            
            st.markdown("")  # Spacing
    
    with tab3:
        st.header("AI Analysis")
        
        # AI metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pattern Recognition", "96%", "Active")
        with col2:
            st.metric("Anomaly Detection", "92%", "Running")
        with col3:
            st.metric("Confidence Level", "89%", "High")
        with col4:
            st.metric("Processing", "1.2K/s", "Normal")
        
        st.markdown("---")
        
        # Neural activity
        st.subheader("Neural Network Activity")
        
        time_points = np.linspace(0, 10, 200)
        signal = np.sin(2 * np.pi * time_points) + np.random.normal(0, 0.1, 200)
        
        fig_neural = go.Figure()
        fig_neural.add_trace(go.Scatter(
            x=time_points,
            y=signal,
            mode='lines',
            name='Neural Signal',
            line=dict(color='#6c5ce7', width=2)
        ))
        
        fig_neural.update_layout(
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(title='Time (s)', gridcolor='#f0f0f0'),
            yaxis=dict(title='Signal', gridcolor='#f0f0f0'),
            showlegend=False
        )
        
        st.plotly_chart(fig_neural, use_container_width=True)
        
        # Insights
        st.subheader("Key Insights")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("📊 Pattern detected: Increased events in age group 25-35")
        with col2:
            st.warning("⚠️ Anomaly: Unusual clustering in urban areas")
    
    with tab4:
        st.header("Geographic Distribution")
        
        # Map data
        map_data = pd.DataFrame({
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'lat': [40.7, 34.0, 41.9, 29.8, 33.4],
            'lon': [-74.0, -118.2, -87.6, -95.4, -112.1],
            'events': [95, 78, 64, 52, 41]
        })
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            size='events',
            hover_name='City',
            hover_data=['events'],
            color_discrete_sequence=['#4834d4'],
            zoom=3,
            height=400
        )
        
        fig_map.update_layout(
            mapbox_style='carto-positron',
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional stats
        st.subheader("Regional Statistics")
        
        regional_data = pd.DataFrame({
            'Region': ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West'],
            'Events': [342, 298, 276, 234, 197],
            'Trend': ['↑', '↓', '→', '↑', '→']
        })
        
        st.dataframe(regional_data, use_container_width=True, hide_index=True)
    
    with tab5:
        st.header("Predictive Analytics")
        
        # Prediction chart
        future_dates = pd.date_range(start=datetime.now(), periods=30, freq='D')
        prediction = 100 + np.cumsum(np.random.randn(30) * 5)
        upper = prediction + 20
        lower = prediction - 20
        
        fig_pred = go.Figure()
        
        # Confidence band
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=upper,
            fill=None,
            mode='lines',
            line_color='rgba(0,0,0,0)',
            showlegend=False
        ))
        
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=lower,
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,0,0,0)',
            name='95% Confidence',
            fillcolor='rgba(72, 52, 212, 0.1)'
        ))
        
        # Prediction line
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=prediction,
            mode='lines+markers',
            name='Prediction',
            line=dict(color='#4834d4', width=2),
            marker=dict(size=4)
        ))
        
        fig_pred.update_layout(
            title='30-Day Forecast',
            xaxis_title='Date',
            yaxis_title='Predicted Events',
            height=350,
            plot_bgcolor='white',
            paper_bgcolor='white',
            xaxis=dict(gridcolor='#f0f0f0'),
            yaxis=dict(gridcolor='#f0f0f0'),
            hovermode='x'
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Peak Risk", "Day 17", "Monitor")
        with col2:
            st.metric("Trend", "Increasing", "12%")
        with col3:
            st.metric("Confidence", "89%", "High")

else:
    # Welcome screen
    st.header("Welcome to ComplianceWatch")
    
    st.markdown("""
    ComplianceWatch is an AI-powered system for real-time pharmaceutical adverse event monitoring. 
    Detect potential safety signals **48 hours faster** than traditional methods.
    """)
    
    st.markdown("---")
    
    # Features
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        ### 🔍 Real-Time
        24/7 monitoring across multiple data sources
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI-Powered
        Advanced ML with 95% accuracy
        """)
    
    with col3:
        st.markdown("""
        ### ⚡ Fast Detection
        48 hours faster than traditional methods
        """)
    
    with col4:
        st.markdown("""
        ### 📊 Compliance
        FDA-ready automated reports
        """)
    
    st.markdown("---")
    
    # How to use
    with st.expander("📖 How to Use", expanded=True):
        st.markdown("""
        1. **Enter a drug name** in the sidebar (e.g., Ozempic, Keytruda)
        2. **Select data sources** to monitor
        3. **Configure settings** (time range, severity threshold)
        4. **Click "Start Monitoring"** to begin
        5. **View results** in the dashboard tabs
        """)
    
    # Stats
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Drugs Monitored", "2,847")
    with col2:
        st.metric("Events Detected", "1.2M")
    with col3:
        st.metric("Active Alerts", "342")
    with col4:
        st.metric("Uptime", "99.97%")
    
    st.info("👈 **Ready to start?** Enter a drug name in the sidebar and click 'Start Monitoring'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #636e72;'>
    ComplianceWatch © 2025 | Created by Atharva Deshpande
</div>
""", unsafe_allow_html=True)
