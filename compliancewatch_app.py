# compliancewatch_wcag_compliant.py - WCAG 2.1 Compliant Professional Version
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
    page_title="ComplianceWatch | AI Pharmaceutical Monitoring",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Professional WCAG 2.1 Compliant CSS
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');
    
    /* WCAG Compliant Color Scheme */
    :root {
        --primary-dark: #1a237e;      /* Deep Blue - High contrast */
        --primary: #3949ab;            /* Primary Blue */
        --primary-light: #5e72e4;     /* Light Blue */
        --secondary: #00897b;          /* Teal */
        --accent: #ff6b35;             /* Orange - for important elements */
        --success: #2e7d32;            /* Green */
        --warning: #f57c00;            /* Orange */
        --danger: #c62828;             /* Red */
        --info: #0277bd;               /* Light Blue */
        --background: #f8f9fa;         /* Light Gray */
        --surface: #ffffff;            /* White */
        --text-primary: #212529;       /* Almost Black */
        --text-secondary: #495057;     /* Dark Gray */
        --border: #dee2e6;             /* Light Border */
    }
    
    /* Global styles with proper contrast */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Font hierarchy for readability */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-weight: 600;
        color: var(--primary-dark);
    }
    
    p, span, div, label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: var(--text-primary);
    }
    
    /* Main container with subtle depth */
    .main .block-container {
        background: var(--surface);
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Sidebar with professional styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Accessible button styling */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: 2px solid transparent;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button:focus {
        outline: 3px solid var(--primary-light);
        outline-offset: 2px;
    }
    
    /* Metric cards with proper contrast */
    [data-testid="metric-container"] {
        background: var(--surface);
        padding: 1.25rem;
        border-radius: 8px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    [data-testid="metric-container"] label {
        color: var(--text-secondary) !important;
        font-size: 0.875rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] > div div[data-testid="metric-value"] {
        color: var(--primary-dark) !important;
        font-weight: 700;
        font-size: 2rem;
    }
    
    /* Tab styling for accessibility */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--surface);
        border-radius: 8px;
        border: 1px solid var(--border);
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--text-primary);
        font-weight: 500;
        background: transparent;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--background);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
    }
    
    /* Alert boxes with semantic colors */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    .stInfo {
        background: #e3f2fd !important;
        color: var(--info) !important;
        border-left-color: var(--info) !important;
    }
    
    .stSuccess {
        background: #e8f5e9 !important;
        color: var(--success) !important;
        border-left-color: var(--success) !important;
    }
    
    .stWarning {
        background: #fff3e0 !important;
        color: var(--warning) !important;
        border-left-color: var(--warning) !important;
    }
    
    .stError {
        background: #ffebee !important;
        color: var(--danger) !important;
        border-left-color: var(--danger) !important;
    }
    
    /* Expander with proper contrast */
    .streamlit-expanderHeader {
        background: var(--background);
        border: 1px solid var(--border);
        border-radius: 8px;
        color: var(--text-primary) !important;
        font-weight: 500;
    }
    
    .streamlit-expanderHeader:hover {
        background: var(--surface);
    }
    
    /* Input fields with accessible styling */
    .stTextInput > div > div > input {
        background: var(--surface) !important;
        border: 2px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        outline: none;
        box-shadow: 0 0 0 3px rgba(57, 73, 171, 0.1);
    }
    
    .stSelectbox > div > div > select {
        background: var(--surface) !important;
        border: 2px solid var(--border) !important;
        color: var(--text-primary) !important;
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: var(--primary) !important;
        outline: none;
    }
    
    /* Slider with accessible colors */
    .stSlider > div > div > div > div {
        background: var(--primary);
    }
    
    .stSlider > div > div > div {
        background: var(--border);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--primary-light));
    }
    
    /* Column styling */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Headers with proper hierarchy */
    .main h1 {
        color: var(--primary-dark);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .main h2 {
        color: var(--primary-dark);
        font-size: 1.875rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--border);
        padding-bottom: 0.5rem;
    }
    
    .main h3 {
        color: var(--primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    /* Data tables with good contrast */
    .dataframe {
        background: var(--surface) !important;
        color: var(--text-primary) !important;
    }
    
    .dataframe th {
        background: var(--background) !important;
        color: var(--text-primary) !important;
        font-weight: 600;
        text-align: left;
        padding: 0.75rem;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid var(--border);
    }
    
    /* Focus indicators for accessibility */
    *:focus {
        outline: 3px solid var(--primary-light);
        outline-offset: 2px;
    }
    
    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .stButton > button {
            border: 2px solid var(--primary-dark);
        }
        
        [data-testid="metric-container"] {
            border: 2px solid var(--primary-dark);
        }
    }
    
    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
        }
    }
    
    /* Custom card styling */
    .custom-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .custom-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure sufficient line height for readability */
    p, li {
        line-height: 1.6;
    }
    
    /* Link styling for accessibility */
    a {
        color: var(--primary);
        text-decoration: underline;
    }
    
    a:hover {
        color: var(--primary-dark);
    }
    
    a:focus {
        outline: 3px solid var(--primary-light);
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Professional header
st.markdown("# ⚕️ ComplianceWatch")
st.markdown(
    "<p style='text-align: center; font-size: 1.25rem; color: #495057; margin-bottom: 2rem;'>"
    "AI-Powered Pharmaceutical Adverse Event Monitoring System</p>",
    unsafe_allow_html=True
)

# Sidebar with professional controls
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")
    
    # Drug input
    drug_name = st.text_input(
        "**Target Drug**",
        placeholder="e.g., Ozempic, Keytruda",
        help="Enter the pharmaceutical drug name to monitor"
    )
    
    # Data sources
    st.markdown("### Data Sources")
    data_sources = st.multiselect(
        "Select monitoring platforms",
        ["Reddit", "Twitter/X", "Facebook", "Patient Forums", "FDA FAERS", "Medical Journals"],
        default=["Reddit", "FDA FAERS"],
        help="Choose data sources for adverse event detection"
    )
    
    # Time range
    st.markdown("### Time Period")
    time_range = st.selectbox(
        "Analysis window",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
        help="Select the time period for historical analysis"
    )
    
    # Severity threshold
    st.markdown("### Alert Threshold")
    severity_threshold = st.slider(
        "Minimum severity level",
        min_value=1,
        max_value=10,
        value=5,
        help="Events above this severity will trigger alerts"
    )
    
    # Confidence level
    st.markdown("### AI Confidence")
    confidence_level = st.slider(
        "Minimum confidence (%)",
        min_value=50,
        max_value=100,
        value=80,
        step=5,
        help="AI confidence threshold for alerts"
    )
    
    st.markdown("---")
    
    # Launch button
    if st.button("▶️ Start Monitoring", use_container_width=True, type="primary"):
        st.session_state.monitoring = True
        st.success("✅ Monitoring system activated")
        
    # System status
    if st.session_state.monitoring:
        st.markdown("---")
        st.markdown("### System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active", "Yes", "Online")
        with col2:
            st.metric("Health", "100%", "Optimal")
        
        # Last update time
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# Main content area
if st.session_state.monitoring and drug_name:
    
    # Key metrics at the top
    st.markdown("## 📊 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_events = 1247 + random.randint(-50, 50)
        st.metric(
            label="Total Events",
            value=f"{total_events:,}",
            delta=f"+{random.randint(10, 50)} today"
        )
    
    with col2:
        critical_alerts = random.randint(2, 5)
        st.metric(
            label="Critical Alerts",
            value=critical_alerts,
            delta="Immediate action",
            delta_color="inverse"
        )
    
    with col3:
        detection_speed = random.randint(40, 48)
        st.metric(
            label="Detection Speed",
            value=f"{detection_speed}h faster",
            delta="vs traditional"
        )
    
    with col4:
        accuracy = 94.7 + random.uniform(-1, 1)
        st.metric(
            label="AI Accuracy",
            value=f"{accuracy:.1f}%",
            delta=f"+{random.uniform(0.5, 2):.1f}%"
        )
    
    with col5:
        coverage = random.randint(92, 98)
        st.metric(
            label="Coverage",
            value=f"{coverage}%",
            delta="Global"
        )
    
    st.markdown("---")
    
    # Create professional tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Dashboard",
        "🔔 Alerts",
        "🤖 AI Analysis",
        "🗺️ Geographic View",
        "📊 Predictions",
        "📑 Reports"
    ])
    
    with tab1:
        st.markdown("## Dashboard Overview")
        
        # Severity distribution and source analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Severity Distribution")
            
            severity_data = pd.DataFrame({
                'Severity Level': ['Critical', 'High', 'Medium', 'Low', 'Minimal'],
                'Count': [3, 12, 45, 127, 1060],
                'Percentage': [0.24, 0.96, 3.61, 10.18, 85.01]
            })
            
            fig_severity = go.Figure(data=[
                go.Bar(
                    x=severity_data['Count'],
                    y=severity_data['Severity Level'],
                    orientation='h',
                    marker=dict(
                        color=['#c62828', '#f57c00', '#fbc02d', '#689f38', '#2e7d32'],
                        line=dict(color='white', width=1)
                    ),
                    text=[f"{c} ({p:.1f}%)" for c, p in zip(severity_data['Count'], severity_data['Percentage'])],
                    textposition='outside'
                )
            ])
            
            fig_severity.update_layout(
                height=350,
                margin=dict(l=0, r=50, t=0, b=0),
                xaxis=dict(title='Number of Events'),
                yaxis=dict(title=''),
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                font=dict(size=12)
            )
            
            st.plotly_chart(fig_severity, use_container_width=True)
        
        with col2:
            st.markdown("### Data Source Analysis")
            
            source_data = pd.DataFrame({
                'Source': ['Reddit', 'FDA FAERS', 'Twitter', 'Forums', 'Medical'],
                'Events': [412, 389, 234, 156, 56]
            })
            
            fig_source = go.Figure(data=[go.Pie(
                labels=source_data['Source'],
                values=source_data['Events'],
                hole=0.4,
                marker=dict(
                    colors=['#3949ab', '#00897b', '#5e72e4', '#fbc02d', '#c62828']
                )
            )])
            
            fig_source.update_layout(
                height=350,
                margin=dict(l=0, r=0, t=0, b=0),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=12),
                annotations=[dict(
                    text=f'{sum(source_data["Events"])}<br>Total',
                    x=0.5, y=0.5,
                    font_size=20,
                    showarrow=False
                )]
            )
            
            st.plotly_chart(fig_source, use_container_width=True)
        
        # Trend analysis
        st.markdown("### 30-Day Trend Analysis")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Events': np.cumsum(np.random.randn(30) * 10 + 50),
            'Alerts': np.cumsum(np.random.randn(30) * 2 + 5)
        })
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Events'],
            name='Total Events',
            mode='lines+markers',
            line=dict(color='#3949ab', width=3),
            marker=dict(size=6),
            fill='tonexty',
            fillcolor='rgba(57, 73, 171, 0.1)'
        ))
        
        fig_trend.add_trace(go.Scatter(
            x=trend_data['Date'],
            y=trend_data['Alerts'],
            name='Critical Alerts',
            mode='lines+markers',
            line=dict(color='#c62828', width=2),
            marker=dict(size=5),
            yaxis='y2'
        ))
        
        fig_trend.update_layout(
            height=400,
            xaxis=dict(title='Date', gridcolor='#e0e0e0'),
            yaxis=dict(title='Total Events', gridcolor='#e0e0e0'),
            yaxis2=dict(title='Critical Alerts', overlaying='y', side='right'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(x=0.02, y=0.98),
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
    
    with tab2:
        st.markdown("## Active Alerts")
        
        # Alert filters
        col1, col2, col3 = st.columns(3)
        with col1:
            alert_filter = st.selectbox("Filter by severity", ["All", "Critical", "High", "Medium", "Low"])
        with col2:
            source_filter = st.selectbox("Filter by source", ["All"] + data_sources)
        with col3:
            time_filter = st.selectbox("Time frame", ["Last Hour", "Last 24H", "Last Week"])
        
        st.markdown("---")
        
        # Alert list
        alerts = [
            ("Critical", f"Severe adverse reaction cluster detected for {drug_name}", "FDA FAERS", "2 min ago", 95),
            ("High", f"Unusual symptom pattern emerging - {drug_name}", "Reddit", "15 min ago", 87),
            ("Medium", f"Increased reporting rate for {drug_name} side effects", "Twitter", "1 hour ago", 76),
            ("Low", f"Minor reactions reported for {drug_name}", "Forums", "3 hours ago", 62),
            ("Low", f"Routine monitoring update for {drug_name}", "Medical", "5 hours ago", 58)
        ]
        
        for severity, message, source, time_ago, confidence in alerts:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                if severity == "Critical":
                    st.error(f"🔴 **{severity}**: {message}")
                elif severity == "High":
                    st.warning(f"🟠 **{severity}**: {message}")
                elif severity == "Medium":
                    st.info(f"🟡 **{severity}**: {message}")
                else:
                    st.success(f"🟢 **{severity}**: {message}")
            
            with col2:
                st.metric("Source", source, label_visibility="collapsed")
            
            with col3:
                st.metric("Confidence", f"{confidence}%", label_visibility="collapsed")
            
            with col4:
                st.caption(time_ago)
    
    with tab3:
        st.markdown("## AI Analysis Dashboard")
        
        # AI metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pattern Recognition", f"{random.randint(92, 98)}%", "Active")
        with col2:
            st.metric("Anomaly Detection", f"{random.randint(88, 95)}%", "Scanning")
        with col3:
            st.metric("Prediction Confidence", f"{random.randint(85, 93)}%", "High")
        with col4:
            st.metric("Processing Speed", f"{random.randint(1000, 2000)}/sec", "Optimal")
        
        st.markdown("---")
        
        # Neural network activity
        st.markdown("### Neural Network Activity")
        
        # Generate signal data
        time_points = np.linspace(0, 10, 200)
        
        fig_neural = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Pattern Recognition', 'Anomaly Detection', 
                          'Sentiment Analysis', 'Risk Assessment'),
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Different signals for each subplot
        signals = [
            np.sin(2 * np.pi * 1 * time_points) + np.random.normal(0, 0.1, 200),
            np.sin(2 * np.pi * 2 * time_points) * np.exp(-time_points/10) + np.random.normal(0, 0.1, 200),
            np.cos(2 * np.pi * 1.5 * time_points) + np.sin(4 * np.pi * time_points) * 0.3,
            np.sin(2 * np.pi * 0.5 * time_points) * (1 + 0.5 * np.sin(2 * np.pi * 5 * time_points))
        ]
        
        colors = ['#3949ab', '#00897b', '#ff6b35', '#c62828']
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for signal, color, pos in zip(signals, colors, positions):
            fig_neural.add_trace(
                go.Scatter(
                    x=time_points,
                    y=signal,
                    mode='lines',
                    line=dict(color=color, width=2),
                    showlegend=False
                ),
                row=pos[0], col=pos[1]
            )
        
        fig_neural.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(size=11)
        )
        
        fig_neural.update_xaxes(gridcolor='#e0e0e0', title_text='Time (s)')
        fig_neural.update_yaxes(gridcolor='#e0e0e0', title_text='Signal')
        
        st.plotly_chart(fig_neural, use_container_width=True)
        
        # AI Insights
        st.markdown("### Key AI Insights")
        
        insights = [
            ("Pattern Detected", "Increased adverse events correlation with dosage timing", "High", "#3949ab"),
            ("Anomaly Found", "Unusual reaction cluster in 25-35 age group", "Medium", "#ff6b35"),
            ("Risk Assessment", "Elevated risk for patients with comorbidities", "High", "#c62828"),
            ("Trend Analysis", "Event frequency increasing by 12% week-over-week", "Medium", "#00897b")
        ]
        
        col1, col2 = st.columns(2)
        
        for i, (title, desc, priority, color) in enumerate(insights):
            with col1 if i % 2 == 0 else col2:
                st.markdown(
                    f"""
                    <div style='background: white; padding: 1rem; border-left: 4px solid {color}; 
                    border-radius: 4px; margin-bottom: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                        <strong style='color: {color};'>{title}</strong><br>
                        <span style='color: #495057;'>{desc}</span><br>
                        <small style='color: #6c757d;'>Priority: {priority}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with tab4:
        st.markdown("## Geographic Distribution")
        
        # Generate map data
        map_data = pd.DataFrame({
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
            'State': ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA'],
            'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
                   39.9526, 29.4241, 32.7157, 32.7767, 37.3382],
            'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
                   -75.1652, -98.4936, -117.1611, -96.7970, -121.8863],
            'events': [random.randint(50, 200) for _ in range(10)],
            'severity': [random.choice(['Low', 'Medium', 'High']) for _ in range(10)]
        })
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            size='events',
            color='severity',
            hover_name='City',
            hover_data=['State', 'events'],
            color_discrete_map={
                'High': '#c62828',
                'Medium': '#f57c00',
                'Low': '#2e7d32'
            },
            zoom=3,
            height=500
        )
        
        fig_map.update_layout(
            mapbox_style='carto-positron',
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional statistics
        st.markdown("### Regional Statistics")
        
        regional_data = pd.DataFrame({
            'Region': ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West'],
            'Total Events': [random.randint(200, 400) for _ in range(5)],
            'Critical Alerts': [random.randint(2, 8) for _ in range(5)],
            'Avg Severity': [round(random.uniform(3.0, 7.0), 1) for _ in range(5)],
            'Trend': ['↑', '↓', '→', '↑', '→']
        })
        
        st.dataframe(regional_data, use_container_width=True, hide_index=True)
    
    with tab5:
        st.markdown("## Predictive Analytics")
        
        # Prediction controls
        col1, col2, col3 = st.columns(3)
        with col1:
            pred_horizon = st.selectbox("Forecast horizon", ["7 days", "14 days", "30 days", "90 days"])
        with col2:
            pred_model = st.selectbox("Model type", ["LSTM", "Prophet", "ARIMA", "Ensemble"])
        with col3:
            confidence_int = st.selectbox("Confidence interval", ["80%", "90%", "95%", "99%"])
        
        st.markdown("---")
        
        # Generate prediction
        days = int(pred_horizon.split()[0])
        dates = pd.date_range(start=datetime.now(), periods=days, freq='D')
        
        # Create realistic prediction with trend and seasonality
        trend = np.linspace(100, 120, days)
        seasonal = 10 * np.sin(np.linspace(0, 4*np.pi, days))
        noise = np.random.normal(0, 5, days)
        prediction = trend + seasonal + noise
        
        # Confidence bands
        ci_width = {'80%': 15, '90%': 20, '95%': 25, '99%': 30}[confidence_int]
        upper_bound = prediction + ci_width
        lower_bound = prediction - ci_width
        
        fig_pred = go.Figure()
        
        # Add confidence band
        fig_pred.add_trace(go.Scatter(
            x=dates,
            y=upper_bound,
            fill=None,
            mode='lines',
            line_color='rgba(0,0,0,0)',
            showlegend=False
        ))
        
        fig_pred.add_trace(go.Scatter(
            x=dates,
            y=lower_bound,
            fill='tonexty',
            mode='lines',
            line_color='rgba(0,0,0,0)',
            name=f'{confidence_int} Confidence',
            fillcolor='rgba(57, 73, 171, 0.2)'
        ))
        
        # Add prediction line
        fig_pred.add_trace(go.Scatter(
            x=dates,
            y=prediction,
            mode='lines+markers',
            name='Predicted Events',
            line=dict(color='#3949ab', width=3),
            marker=dict(size=4, color='#3949ab')
        ))
        
        fig_pred.update_layout(
            title=f'{pred_horizon} Event Forecast ({pred_model} Model)',
            xaxis_title='Date',
            yaxis_title='Predicted Event Count',
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified',
            font=dict(size=12),
            legend=dict(x=0.02, y=0.98)
        )
        
        fig_pred.update_xaxes(gridcolor='#e0e0e0')
        fig_pred.update_yaxes(gridcolor='#e0e0e0')
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Prediction metrics
        st.markdown("### Model Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("RMSE", f"{random.uniform(5, 15):.2f}", "Lower is better")
        with col2:
            st.metric("MAE", f"{random.uniform(3, 10):.2f}", "Lower is better")
        with col3:
            st.metric("R² Score", f"{random.uniform(0.85, 0.95):.3f}", "Higher is better")
        with col4:
            st.metric("MAPE", f"{random.uniform(5, 15):.1f}%", "Lower is better")
        
        # Risk assessment
        st.markdown("### Risk Assessment")
        
        risk_data = pd.DataFrame({
            'Risk Factor': ['Severity Escalation', 'Geographic Spread', 'Demographic Shift', 'Source Reliability'],
            'Current Level': ['Medium', 'Low', 'High', 'High'],
            'Predicted Trend': ['Increasing', 'Stable', 'Increasing', 'Stable'],
            'Action Required': ['Monitor closely', 'Routine monitoring', 'Investigate', 'Continue monitoring']
        })
        
        st.dataframe(risk_data, use_container_width=True, hide_index=True)
    
    with tab6:
        st.markdown("## Compliance Reports")
        
        # Report configuration
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Report Configuration")
            
            report_type = st.selectbox(
                "Report type",
                ["FDA MedWatch 3500", "EMA EudraVigilance", "Custom Executive Summary", "Technical Analysis"]
            )
            
            report_period = st.date_input(
                "Report period",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                format="YYYY-MM-DD"
            )
            
            include_sections = st.multiselect(
                "Include sections",
                ["Executive Summary", "Detailed Events", "Statistical Analysis", 
                 "Geographic Distribution", "Trend Analysis", "AI Insights", "Recommendations"],
                default=["Executive Summary", "Detailed Events", "Statistical Analysis", "Recommendations"]
            )
        
        with col2:
            st.markdown("### Quick Actions")
            
            if st.button("📄 Generate Report", use_container_width=True):
                with st.spinner("Generating report..."):
                    progress = st.progress(0)
                    for i in range(100):
                        progress.progress(i + 1)
                        time.sleep(0.01)
                    st.success("Report generated successfully!")
            
            st.button("📧 Email Report", use_container_width=True)
            st.button("💾 Download PDF", use_container_width=True)
            st.button("📤 Submit to FDA", use_container_width=True)
        
        st.markdown("---")
        
        # Report preview
        st.markdown("### Report Preview")
        
        st.markdown(
            f"""
            <div style='background: white; padding: 2rem; border: 1px solid #dee2e6; 
            border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h4 style='color: #1a237e; margin-bottom: 1rem;'>
                    ComplianceWatch Report - {drug_name}
                </h4>
                <p style='color: #495057; margin-bottom: 1rem;'>
                    <strong>Report Period:</strong> {report_period[0]} to {report_period[1]}<br>
                    <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
                    <strong>Report Type:</strong> {report_type}
                </p>
                <h5 style='color: #3949ab; margin-top: 1.5rem;'>Executive Summary</h5>
                <p style='color: #495057; line-height: 1.6;'>
                    During the reporting period, ComplianceWatch detected {total_events} adverse events 
                    related to {drug_name} across {len(data_sources)} data sources. Of these events, 
                    {critical_alerts} were classified as critical severity requiring immediate attention.
                    The AI system achieved {accuracy:.1f}% accuracy in event classification with an average 
                    detection speed {detection_speed} hours faster than traditional monitoring systems.
                </p>
                <h5 style='color: #3949ab; margin-top: 1.5rem;'>Key Findings</h5>
                <ul style='color: #495057; line-height: 1.6;'>
                    <li>Increased adverse event reporting in patients aged 25-35</li>
                    <li>Geographic clustering observed in urban metropolitan areas</li>
                    <li>Correlation identified between dosage timing and symptom onset</li>
                    <li>Social media sentiment analysis indicates growing patient concerns</li>
                </ul>
                <h5 style='color: #3949ab; margin-top: 1.5rem;'>Recommendations</h5>
                <ol style='color: #495057; line-height: 1.6;'>
                    <li>Conduct targeted investigation of the 25-35 age demographic</li>
                    <li>Review and potentially update dosing guidelines</li>
                    <li>Enhance patient education materials regarding potential side effects</li>
                    <li>Continue enhanced monitoring for the next 30 days</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    # Professional welcome screen
    st.markdown("## Welcome to ComplianceWatch")
    
    # Introduction
    st.markdown(
        """
        ComplianceWatch is an advanced AI-powered system for monitoring pharmaceutical adverse events 
        in real-time. Our platform detects potential safety signals up to 48 hours faster than 
        traditional pharmacovigilance methods.
        """
    )
    
    # Feature cards in columns
    st.markdown("### Key Features")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            """
            <div style='background: white; padding: 1.5rem; border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 200px;'>
                <h4 style='color: #3949ab;'>🔍 Real-Time Monitoring</h4>
                <p style='color: #495057; font-size: 0.9rem;'>
                    24/7 surveillance across multiple data sources including social media, 
                    FDA databases, and medical forums.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div style='background: white; padding: 1.5rem; border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 200px;'>
                <h4 style='color: #00897b;'>🤖 AI-Powered Analysis</h4>
                <p style='color: #495057; font-size: 0.9rem;'>
                    Advanced machine learning algorithms detect patterns and anomalies 
                    with 95% accuracy.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div style='background: white; padding: 1.5rem; border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 200px;'>
                <h4 style='color: #ff6b35;'>⚡ Rapid Detection</h4>
                <p style='color: #495057; font-size: 0.9rem;'>
                    Identify adverse events 48 hours faster than traditional 
                    monitoring methods.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            """
            <div style='background: white; padding: 1.5rem; border-radius: 8px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 200px;'>
                <h4 style='color: #c62828;'>📊 Compliance Ready</h4>
                <p style='color: #495057; font-size: 0.9rem;'>
                    Generate FDA-compliant reports automatically with full 
                    audit trails.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # How it works
    with st.expander("📚 How It Works", expanded=True):
        st.markdown(
            """
            ### Getting Started with ComplianceWatch
            
            1. **Enter Drug Name**: Specify the pharmaceutical product you want to monitor in the sidebar
            2. **Select Data Sources**: Choose which platforms and databases to monitor
            3. **Configure Settings**: Set your time range, severity threshold, and confidence level
            4. **Start Monitoring**: Click the "Start Monitoring" button to begin real-time surveillance
            5. **Review Results**: Access dashboards, alerts, and reports through the tabbed interface
            
            ### System Capabilities
            
            - **Multi-source data aggregation** from social media, medical databases, and forums
            - **Natural language processing** to extract and analyze adverse event descriptions
            - **Pattern recognition** to identify emerging safety signals
            - **Geographic mapping** to detect regional clusters
            - **Predictive analytics** to forecast future trends
            - **Automated reporting** for regulatory compliance
            """
        )
    
    # Statistics
    st.markdown("---")
    st.markdown("### Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Drugs Monitored", "2,847", "↑ 127 this month")
    with col2:
        st.metric("Events Detected", "1.2M", "↑ 48K this week")
    with col3:
        st.metric("Active Alerts", "342", "23 critical")
    with col4:
        st.metric("System Uptime", "99.97%", "30 days")
    
    # Call to action
    st.markdown("---")
    st.info(
        "👈 **Ready to begin?** Enter a drug name in the sidebar and click 'Start Monitoring' to activate the system."
    )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6c757d; padding: 1rem;'>
        <p>ComplianceWatch © 2025 | Protecting Patients Through Intelligent Monitoring</p>
        <p style='font-size: 0.9rem;'>Created by Atharva Deshpande | 
        <a href='#' style='color: #3949ab;'>Privacy Policy</a> | 
        <a href='#' style='color: #3949ab;'>Terms of Service</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
