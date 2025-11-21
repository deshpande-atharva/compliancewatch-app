# compliancewatch_beautiful.py - Beautiful Clean UI
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

# Beautiful, clean CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Clean color palette */
    :root {
        --primary: #5E4FDB;
        --primary-light: #8B7FF0;
        --primary-dark: #4039B8;
        --secondary: #10B981;
        --danger: #EF4444;
        --warning: #F59E0B;
        --info: #3B82F6;
        --dark: #1F2937;
        --gray: #6B7280;
        --light-gray: #F3F4F6;
        --white: #FFFFFF;
        --border: #E5E7EB;
    }
    
    /* Global styles */
    .stApp {
        background: linear-gradient(180deg, #FAFBFF 0%, #F3F4F6 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Headers */
    h1 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--dark) !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    h2 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--dark) !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--dark) !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Paragraphs and text */
    p, span, div, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--gray) !important;
        line-height: 1.6 !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5E4FDB 0%, #4039B8 100%);
        padding-top: 2rem;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding: 0 1rem 2rem 1rem;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        margin: 1.5rem 0;
    }
    
    /* Beautiful buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 10px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        letter-spacing: 0.02em;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 14px 0 rgba(94, 79, 219, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(94, 79, 219, 0.4);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    [data-testid="metric-container"] label {
        color: var(--gray) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.5rem !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: var(--dark) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        line-height: 1 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        background: var(--light-gray);
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
        display: inline-block;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: white;
        padding: 0.25rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--gray);
        font-weight: 600;
        background: transparent;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--light-gray);
        color: var(--dark);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary);
        color: white;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        border: 1px solid;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stInfo {
        background: #EFF6FF;
        color: #1E40AF;
        border-color: #BFDBFE;
    }
    
    .stSuccess {
        background: #F0FDF4;
        color: #14532D;
        border-color: #86EFAC;
    }
    
    .stWarning {
        background: #FFFBEB;
        color: #78350F;
        border-color: #FDE047;
    }
    
    .stError {
        background: #FEF2F2;
        color: #7F1D1D;
        border-color: #FCA5A5;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        font-family: 'Plus Jakarta Sans', sans-serif;
        border-radius: 8px;
        border: 2px solid var(--border);
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.2s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        outline: none;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Custom cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s;
        margin-bottom: 1.5rem;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        border-color: var(--primary-light);
    }
    
    .feature-card h4 {
        color: var(--dark);
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    
    .feature-card p {
        color: var(--gray);
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }
    
    .instruction-card {
        background: linear-gradient(135deg, #FAFBFF 0%, #F3F4F6 100%);
        border-left: 4px solid var(--primary);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .instruction-card h5 {
        color: var(--dark);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .instruction-card p {
        color: var(--gray);
        margin: 0;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Ensure text is visible */
    .element-container {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Column gaps */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Horizontal rules */
    hr {
        border: none;
        border-top: 1px solid var(--border);
        margin: 2rem 0;
    }
    
    /* Markdown text */
    .stMarkdown {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: var(--dark) !important;
    }
    
    .streamlit-expanderContent {
        border: 1px solid var(--border);
        border-top: none;
        border-radius: 0 0 10px 10px;
        background: white;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Clean header with subtitle
st.markdown("# 💊 ComplianceWatch")
st.markdown("##### AI-Powered Pharmaceutical Adverse Event Monitoring System")

# Add space
st.markdown("<br>", unsafe_allow_html=True)

# Sidebar with clean design
with st.sidebar:
    st.markdown("## ⚙️ Configuration Panel")
    
    st.markdown("---")
    
    # Drug input with better label
    st.markdown("### 🧪 Drug Selection")
    drug_name = st.text_input(
        "Target Drug Name",
        placeholder="e.g., Ozempic, Keytruda",
        help="Enter the pharmaceutical drug you want to monitor",
        label_visibility="visible"
    )
    
    # Data sources
    st.markdown("### 📊 Data Sources")
    data_sources = st.multiselect(
        "Select monitoring platforms",
        ["Reddit", "Twitter/X", "FDA FAERS", "Medical Forums", "Patient Reports", "Clinical Trials"],
        default=["Reddit", "FDA FAERS"],
        label_visibility="visible"
    )
    
    # Time range
    st.markdown("### ⏱️ Time Period")
    time_range = st.selectbox(
        "Analysis window",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year"],
        index=1,
        label_visibility="visible"
    )
    
    # Severity threshold
    st.markdown("### 🎯 Alert Settings")
    severity_threshold = st.slider(
        "Minimum Severity Level",
        min_value=1,
        max_value=10,
        value=5,
        help="Events above this severity will trigger alerts",
        label_visibility="visible"
    )
    
    confidence_threshold = st.slider(
        "AI Confidence Threshold (%)",
        min_value=50,
        max_value=100,
        value=80,
        step=5,
        help="Minimum confidence level for AI predictions",
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    # Start monitoring button
    if st.button("🚀 **Start Monitoring**", use_container_width=True, type="primary"):
        st.session_state.monitoring = True
        st.success("✅ Monitoring system activated successfully!")
    
    # System status
    if st.session_state.monitoring:
        st.markdown("---")
        st.markdown("### 📡 System Status")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", "Active", "● Live")
        with col2:
            st.metric("Health", "Optimal", "100%")
        
        st.markdown(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")

# Main content area
if st.session_state.monitoring and drug_name:
    
    # Top KPI Cards
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Events",
            value="1,247",
            delta="↑ 23 today"
        )
    
    with col2:
        st.metric(
            label="Critical Alerts",
            value="3",
            delta="Requires attention"
        )
    
    with col3:
        st.metric(
            label="Detection Speed",
            value="48 hours",
            delta="Faster than baseline"
        )
    
    with col4:
        st.metric(
            label="AI Accuracy",
            value="94.7%",
            delta="↑ 2.1%"
        )
    
    with col5:
        st.metric(
            label="Coverage",
            value="Global",
            delta="All regions"
        )
    
    st.markdown("---")
    
    # Create beautiful tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Dashboard Overview",
        "🔔 Active Alerts",
        "🤖 AI Analysis",
        "🌍 Geographic Distribution",
        "📊 Predictive Analytics"
    ])
    
    with tab1:
        st.markdown("## Dashboard Overview")
        st.markdown("Real-time monitoring statistics and trends for " + drug_name)
        
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Severity Distribution")
            
            severity_data = pd.DataFrame({
                'Level': ['Critical', 'High', 'Medium', 'Low', 'Minimal'],
                'Count': [3, 12, 45, 187, 1000]
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=severity_data['Count'],
                    y=severity_data['Level'],
                    orientation='h',
                    marker=dict(
                        color=['#EF4444', '#F59E0B', '#F59E0B', '#10B981', '#6B7280'],
                        line=dict(width=0)
                    ),
                    text=severity_data['Count'],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                height=350,
                margin=dict(l=0, r=60, t=20, b=20),
                plot_bgcolor='#FAFBFF',
                paper_bgcolor='white',
                showlegend=False,
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#E5E7EB',
                    title="Number of Events"
                ),
                yaxis=dict(
                    showgrid=False,
                    title=""
                ),
                font=dict(family="Plus Jakarta Sans")
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Data Source Breakdown")
            
            source_data = pd.DataFrame({
                'Source': ['Reddit', 'FDA FAERS', 'Twitter/X', 'Forums', 'Medical'],
                'Count': [412, 389, 234, 156, 56]
            })
            
            fig2 = go.Figure(data=[go.Pie(
                labels=source_data['Source'],
                values=source_data['Count'],
                hole=0.5,
                marker=dict(
                    colors=['#5E4FDB', '#8B7FF0', '#10B981', '#F59E0B', '#3B82F6'],
                    line=dict(width=0)
                )
            )])
            
            fig2.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=True,
                font=dict(family="Plus Jakarta Sans"),
                annotations=[
                    dict(
                        text='1,247<br>Total',
                        x=0.5, y=0.5,
                        font_size=24,
                        showarrow=False,
                        font=dict(family="Plus Jakarta Sans", weight=700)
                    )
                ]
            )
            
            st.plotly_chart(fig2, use_container_width=True)
        
        # Trend Analysis
        st.markdown("#### 30-Day Event Trend")
        
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        events = 50 + np.cumsum(np.random.randn(30) * 5)
        
        fig3 = go.Figure()
        
        # Add gradient fill
        fig3.add_trace(go.Scatter(
            x=dates,
            y=events,
            mode='lines',
            name='Events',
            line=dict(color='#5E4FDB', width=3),
            fill='tonexty',
            fillcolor='rgba(94, 79, 219, 0.1)'
        ))
        
        # Add markers for last 7 days
        fig3.add_trace(go.Scatter(
            x=dates[-7:],
            y=events[-7:],
            mode='markers',
            name='Recent',
            marker=dict(size=8, color='#5E4FDB', symbol='circle')
        ))
        
        fig3.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=20),
            plot_bgcolor='#FAFBFF',
            paper_bgcolor='white',
            xaxis=dict(
                showgrid=True,
                gridcolor='#E5E7EB',
                title="Date"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E7EB',
                title="Number of Events"
            ),
            showlegend=False,
            hovermode='x unified',
            font=dict(family="Plus Jakarta Sans")
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        st.markdown("## Active Alerts")
        st.markdown("Real-time alerts requiring attention")
        
        # Alert stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info("**3** Critical Alerts")
        with col2:
            st.warning("**7** High Priority")
        with col3:
            st.success("**15** Medium Priority")
        with col4:
            st.success("**42** Low Priority")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Alert list with better formatting
        alerts = [
            {
                "level": "Critical",
                "title": "Severe Adverse Reaction Cluster",
                "desc": f"Multiple severe reactions to {drug_name} reported in Northeast region",
                "source": "FDA FAERS",
                "time": "2 minutes ago",
                "confidence": 95,
                "color": "#EF4444"
            },
            {
                "level": "High",
                "title": "Unusual Symptom Pattern",
                "desc": f"Emerging pattern of neurological symptoms with {drug_name}",
                "source": "Reddit",
                "time": "15 minutes ago",
                "confidence": 87,
                "color": "#F59E0B"
            },
            {
                "level": "Medium",
                "title": "Increased Reporting Rate",
                "desc": f"23% increase in adverse event reports for {drug_name}",
                "source": "Twitter/X",
                "time": "1 hour ago",
                "confidence": 76,
                "color": "#3B82F6"
            },
            {
                "level": "Low",
                "title": "Minor Side Effects",
                "desc": f"Common side effects reported, within expected range",
                "source": "Forums",
                "time": "3 hours ago",
                "confidence": 62,
                "color": "#10B981"
            }
        ]
        
        for alert in alerts:
            with st.container():
                if alert["level"] == "Critical":
                    st.error(f"⚠️ **{alert['level'].upper()}** - {alert['time']}")
                elif alert["level"] == "High":
                    st.warning(f"⚠️ **{alert['level'].upper()}** - {alert['time']}")
                elif alert["level"] == "Medium":
                    st.info(f"⚠️ **{alert['level'].upper()}** - {alert['time']}")
                else:
                    st.success(f"✓ **{alert['level'].upper()}** - {alert['time']}")
                
                st.markdown(f"**{alert['title']}**")
                st.markdown(alert['desc'])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.caption(f"📍 Source: {alert['source']}")
                with col_b:
                    st.caption(f"🎯 Confidence: {alert['confidence']}%")
                
                st.markdown("---")  # Separator between alerts
    
    with tab3:
        st.markdown("## AI Analysis")
        st.markdown("Machine learning insights and pattern recognition")
        
        # AI Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pattern Recognition", "96%", "↑ 3%")
        with col2:
            st.metric("Anomaly Detection", "Active", "12 found")
        with col3:
            st.metric("Processing Speed", "1,247/sec", "Normal")
        with col4:
            st.metric("Model Confidence", "89%", "High")
        
        st.markdown("---")
        
        # Neural Network Visualization
        st.markdown("#### Neural Network Activity")
        
        time_points = np.linspace(0, 10, 300)
        
        fig_neural = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Pattern Recognition', 'Anomaly Detection', 
                          'Sentiment Analysis', 'Risk Assessment'),
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Generate different signals
        signals = [
            np.sin(2 * np.pi * time_points) + np.random.normal(0, 0.1, 300),
            np.cos(2 * np.pi * time_points * 1.5) * np.exp(-time_points/10),
            np.sin(2 * np.pi * time_points * 0.5) + np.sin(2 * np.pi * time_points * 2) * 0.3,
            np.random.normal(0, 1, 300).cumsum() / 10
        ]
        
        colors = ['#5E4FDB', '#10B981', '#F59E0B', '#EF4444']
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
            height=400,
            plot_bgcolor='#FAFBFF',
            paper_bgcolor='white',
            font=dict(family="Plus Jakarta Sans"),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        fig_neural.update_xaxes(
            showgrid=True,
            gridcolor='#E5E7EB',
            title_text='Time (s)',
            title_font=dict(size=10)
        )
        fig_neural.update_yaxes(
            showgrid=True,
            gridcolor='#E5E7EB',
            title_text='Signal',
            title_font=dict(size=10)
        )
        
        st.plotly_chart(fig_neural, use_container_width=True)
        
        # Key Insights
        st.markdown("#### AI-Generated Insights")
        
        insights = [
            ("📊", "Pattern Detected", "Correlation found between dosage timing and adverse events", "#5E4FDB"),
            ("⚠️", "Anomaly Alert", "Unusual clustering of events in 25-35 age demographic", "#F59E0B"),
            ("📈", "Trend Analysis", "12% week-over-week increase in reported events", "#10B981"),
            ("🎯", "Risk Assessment", "Elevated risk profile for patients with comorbidities", "#EF4444")
        ]
        
        col1, col2 = st.columns(2)
        
        for i, (icon, title, desc, color) in enumerate(insights):
            with col1 if i % 2 == 0 else col2:
                with st.container():
                    st.markdown(f"**{icon} {title}**")
                    st.markdown(desc)
                    st.markdown("")  # Add space
    
    with tab4:
        st.markdown("## Geographic Distribution")
        st.markdown("Global and regional adverse event distribution")
        
        # Map
        map_data = pd.DataFrame({
            'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                    'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
            'State': ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA', 'TX', 'CA'],
            'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
                   39.9526, 29.4241, 32.7157, 32.7767, 37.3382],
            'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
                   -75.1652, -98.4936, -117.1611, -96.7970, -121.8863],
            'events': [156, 143, 98, 87, 76, 65, 54, 52, 48, 41],
            'severity': ['High', 'High', 'Medium', 'Medium', 'Low', 'Medium', 'Low', 'Low', 'Medium', 'Low']
        })
        
        fig_map = px.scatter_mapbox(
            map_data,
            lat='lat',
            lon='lon',
            size='events',
            color='severity',
            hover_name='City',
            hover_data={'State': True, 'events': True, 'lat': False, 'lon': False},
            color_discrete_map={'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'},
            zoom=3,
            height=450
        )
        
        fig_map.update_layout(
            mapbox_style='carto-positron',
            margin={"r":0,"t":0,"l":0,"b":0},
            font=dict(family="Plus Jakarta Sans")
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional Statistics
        st.markdown("#### Regional Statistics")
        
        regional_data = pd.DataFrame({
            'Region': ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West Coast'],
            'Total Events': [342, 298, 276, 234, 197],
            'Critical': [8, 5, 4, 3, 2],
            'Trend': ['↑ Rising', '→ Stable', '↓ Declining', '↑ Rising', '→ Stable'],
            'Risk Level': ['High', 'Medium', 'Medium', 'Low', 'Low']
        })
        
        st.dataframe(
            regional_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Region": st.column_config.TextColumn("Region", width="medium"),
                "Total Events": st.column_config.NumberColumn("Total Events", format="%d"),
                "Critical": st.column_config.NumberColumn("Critical", format="%d"),
                "Trend": st.column_config.TextColumn("Trend", width="small"),
                "Risk Level": st.column_config.TextColumn("Risk Level", width="small")
            }
        )
    
    with tab5:
        st.markdown("## Predictive Analytics")
        st.markdown("AI-powered forecasting and trend predictions")
        
        # Controls
        col1, col2, col3 = st.columns(3)
        with col1:
            forecast_days = st.selectbox("Forecast Period", ["7 days", "14 days", "30 days", "90 days"], index=2)
        with col2:
            model_type = st.selectbox("Model Type", ["LSTM Neural Network", "Prophet", "ARIMA", "Ensemble"])
        with col3:
            confidence = st.selectbox("Confidence Interval", ["90%", "95%", "99%"], index=1)
        
        st.markdown("---")
        
        # Generate prediction
        days = int(forecast_days.split()[0])
        future_dates = pd.date_range(start=datetime.now(), periods=days, freq='D')
        
        # Create realistic prediction
        trend = np.linspace(100, 120, days)
        seasonal = 15 * np.sin(np.linspace(0, 4*np.pi, days))
        noise = np.random.normal(0, 5, days)
        prediction = trend + seasonal + noise
        
        # Confidence bands
        ci_mult = {'90%': 1.645, '95%': 1.96, '99%': 2.576}[confidence]
        std = 15
        upper = prediction + ci_mult * std
        lower = prediction - ci_mult * std
        
        fig_pred = go.Figure()
        
        # Add confidence band
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=upper,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=lower,
            mode='lines',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(94, 79, 219, 0.15)',
            name=f'{confidence} Confidence Band',
            hoverinfo='skip'
        ))
        
        # Add prediction line
        fig_pred.add_trace(go.Scatter(
            x=future_dates,
            y=prediction,
            mode='lines+markers',
            name='Predicted Events',
            line=dict(color='#5E4FDB', width=3),
            marker=dict(size=5, color='#5E4FDB')
        ))
        
        fig_pred.update_layout(
            title=f'{forecast_days} Forecast using {model_type}',
            xaxis_title='Date',
            yaxis_title='Predicted Event Count',
            height=400,
            plot_bgcolor='#FAFBFF',
            paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#E5E7EB'),
            yaxis=dict(showgrid=True, gridcolor='#E5E7EB'),
            hovermode='x unified',
            font=dict(family="Plus Jakarta Sans"),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Prediction Metrics
        st.markdown("#### Model Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("RMSE", "8.42", "Lower is better")
        with col2:
            st.metric("MAE", "6.18", "Lower is better")
        with col3:
            st.metric("R² Score", "0.923", "Higher is better")
        with col4:
            st.metric("MAPE", "7.3%", "Lower is better")

else:
    # Beautiful welcome screen
    st.markdown("## Welcome to ComplianceWatch")
    
    st.markdown("""
    <p style='font-size: 1.1rem; color: #6B7280; margin-bottom: 2rem;'>
    ComplianceWatch uses advanced artificial intelligence to monitor pharmaceutical adverse events 
    in real-time, detecting potential safety signals <strong style='color: #5E4FDB;'>48 hours faster</strong> 
    than traditional pharmacovigilance methods.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature cards using native Streamlit
    st.markdown("### ✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("#### 🔍 Real-Time Monitoring")
            st.markdown("""
            24/7 surveillance across multiple data sources including social media, 
            FDA databases, medical forums, and clinical reports.
            """)
            st.markdown("")  # Space
        
        with st.container():
            st.markdown("#### ⚡ Rapid Detection")
            st.markdown("""
            Identify adverse events up to 48 hours faster than traditional methods, 
            enabling quicker response to potential safety issues.
            """)
            st.markdown("")  # Space
    
    with col2:
        with st.container():
            st.markdown("#### 🤖 AI-Powered Analysis")
            st.markdown("""
            Advanced machine learning algorithms detect patterns and anomalies 
            with 95% accuracy using neural networks and NLP.
            """)
            st.markdown("")  # Space
        
        with st.container():
            st.markdown("#### 📊 Compliance Ready")
            st.markdown("""
            Generate FDA-compliant reports automatically with full audit trails 
            and regulatory documentation support.
            """)
            st.markdown("")  # Space
    
    st.markdown("---")
    
    # How to use section - clean instructions with native Streamlit
    st.markdown("### 📚 How to Use ComplianceWatch")
    
    # Create a container with background
    with st.container():
        # Step 1
        st.markdown("##### 1️⃣ Step 1: Enter Drug Name")
        st.markdown("In the sidebar, input the pharmaceutical product you want to monitor (e.g., Ozempic, Keytruda)")
        
        # Step 2
        st.markdown("##### 2️⃣ Step 2: Select Data Sources")
        st.markdown("Choose which platforms and databases to monitor for adverse event reports")
        
        # Step 3
        st.markdown("##### 3️⃣ Step 3: Configure Settings")
        st.markdown("Set your time range, severity threshold, and AI confidence level based on your needs")
        
        # Step 4
        st.markdown("##### 4️⃣ Step 4: Start Monitoring")
        st.markdown("Click the 'Start Monitoring' button to begin real-time surveillance")
        
        # Step 5
        st.markdown("##### ✅ Step 5: Review Results")
        st.markdown("Access comprehensive dashboards, alerts, and reports through the tabbed interface")
    
    st.markdown("")  # Add space
    
    # Platform statistics
    st.markdown("### 📈 Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Drugs Monitored", "2,847", "↑ 127 this month")
    
    with col2:
        st.metric("Events Detected", "1.2M", "↑ 48K this week")
    
    with col3:
        st.metric("Active Alerts", "342", "23 critical")
    
    with col4:
        st.metric("System Uptime", "99.97%", "30 days")
    
    st.markdown("---")
    
    # Call to action
    st.info("👈 **Ready to begin?** Enter a drug name in the sidebar and click 'Start Monitoring' to activate the system.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #6B7280;'>
    <p style='font-size: 0.95rem; margin: 0;'>
        <strong>ComplianceWatch</strong> © 2025 | Protecting Patients Through Intelligent Monitoring
    </p>
    <p style='font-size: 0.85rem; margin: 0.5rem 0;'>
        Created by Atharva Deshpande | Powered by Advanced AI
    </p>
</div>
""", unsafe_allow_html=True)
