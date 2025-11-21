# compliancewatch_app.py - Enhanced UI Version
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="ComplianceWatch - AI Pharmaceutical Monitoring",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS with animations and glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        position: relative;
    }
    
    .main::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(255, 219, 98, 0.2) 0%, transparent 50%);
        z-index: 0;
    }
    
    /* Glass morphism cards */
    .stApp > div > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
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
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Metric cards with gradient borders */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.7) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid transparent;
        background-clip: padding-box;
        position: relative;
        transition: transform 0.3s ease;
    }
    
    [data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: -2px; right: -2px; bottom: -2px; left: -2px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 16px;
        z-index: -1;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    /* Alert cards with animations */
    .alert-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: slideIn 0.5s ease;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .alert-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea, #764ba2);
    }
    
    .alert-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    .alert-high::before {
        background: linear-gradient(180deg, #ef4444, #dc2626);
    }
    
    .alert-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .alert-medium::before {
        background: linear-gradient(180deg, #f59e0b, #d97706);
    }
    
    .alert-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .alert-low::before {
        background: linear-gradient(180deg, #10b981, #059669);
    }
    
    .alert-card:hover {
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Header animation */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        margin-bottom: 2rem;
        animation: fadeInDown 1s ease;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .logo-text {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 10px 40px rgba(255, 255, 255, 0.2);
        letter-spacing: -1px;
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        font-weight: 400;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px;
        color: white !important;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }
    
    /* Label styling */
    .stTextInput > label,
    .stSelectbox > label,
    .stMultiSelect > label,
    .stSlider > label {
        color: white !important;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    /* Slider styling */
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Chart containers */
    .plot-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .plot-container:hover {
        transform: translateY(-5px);
    }
    
    /* Welcome screen card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
        margin: 2rem auto;
        max-width: 800px;
        animation: fadeIn 1s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
    }
    
    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Pulse animation for live indicator */
    .pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# Animated header
st.markdown("""
    <div class="main-header">
        <h1 class="logo-text">ComplianceWatch</h1>
        <p class="subtitle">AI-Powered Pharmaceutical Monitoring</p>
        <div style="margin-top: 1rem;">
            <span class="pulse"></span>
            <span style="color: rgba(255,255,255,0.8); margin-left: 10px; font-size: 0.9rem;">Live Monitoring Active</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Enhanced sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">💊</div>
            <h2 style="color: white; font-weight: 700; margin: 0;">Control Panel</h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Configure monitoring parameters</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Drug selection with icon
    st.markdown("### 🔬 Target Drug")
    drug_name = st.text_input(
        "",
        placeholder="e.g., Ozempic, Keytruda",
        help="Enter the pharmaceutical drug name you want to monitor for adverse events",
        label_visibility="collapsed"
    )
    
    # Data source selection with icons
    st.markdown("### 📡 Data Sources")
    data_sources = st.multiselect(
        "",
        ["Reddit", "Twitter/X", "Facebook Groups", "Patient Forums", "FDA FAERS"],
        default=["Reddit", "FDA FAERS"],
        help="Choose which platforms to monitor for adverse event reports",
        label_visibility="collapsed"
    )
    
    # Time range with icon
    st.markdown("### ⏱️ Time Period")
    time_range = st.selectbox(
        "",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
        help="Select the time period for historical data analysis",
        label_visibility="collapsed"
    )
    
    # Severity threshold with gradient
    st.markdown("### ⚠️ Alert Threshold")
    severity_threshold = st.slider(
        "",
        min_value=1,
        max_value=10,
        value=5,
        help="Set minimum severity score (1-10) for alerts",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Monitor button with loading animation
    monitor_button = st.button("🚀 Start Monitoring", use_container_width=True, type="primary")
    
    # Stats in sidebar
    if monitor_button and drug_name:
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        st.metric("Active Monitors", "4")
        st.metric("Total Alerts Today", "23")
        st.metric("System Health", "Optimal")

# Main content area
if monitor_button and drug_name:
    # Loading animation
    with st.spinner('🔍 Analyzing data sources...'):
        time.sleep(1)
    
    # Create modern tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🚨 Live Alerts", "📈 Analytics", "🗺️ Geo Map", "📄 Reports"])
    
    with tab1:
        # Live indicator
        st.markdown("""
            <div style="text-align: right; margin-bottom: 1rem;">
                <span class="pulse"></span>
                <span style="color: white; margin-left: 10px;">Last updated: just now</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Animated metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="feature-card">
                    <h3 style="color: #667eea; font-size: 2.5rem; margin: 0;">247</h3>
                    <p style="color: rgba(0,0,0,0.7); margin: 0.5rem 0;">Total Events</p>
                    <small style="color: #10b981;">↑ 23 from yesterday</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="feature-card">
                    <h3 style="color: #ef4444; font-size: 2.5rem; margin: 0;">3</h3>
                    <p style="color: rgba(0,0,0,0.7); margin: 0.5rem 0;">Critical Alerts</p>
                    <small style="color: #ef4444;">⚠️ Immediate attention</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="feature-card">
                    <h3 style="color: #764ba2; font-size: 2.5rem; margin: 0;">48h</h3>
                    <p style="color: rgba(0,0,0,0.7); margin: 0.5rem 0;">Faster Detection</p>
                    <small style="color: #667eea;">vs traditional methods</small>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="feature-card">
                    <h3 style="color: #10b981; font-size: 2.5rem; margin: 0;">94.7%</h3>
                    <p style="color: rgba(0,0,0,0.7); margin: 0.5rem 0;">Accuracy</p>
                    <small style="color: #10b981;">↑ 2.3% improvement</small>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced charts with glassmorphism
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Severity Distribution")
            severity_data = pd.DataFrame({
                'Level': ['Critical', 'High', 'Medium', 'Low'],
                'Count': [3, 12, 45, 187]
            })
            
            fig = go.Figure(data=[
                go.Bar(
                    x=severity_data['Count'],
                    y=severity_data['Level'],
                    orientation='h',
                    marker=dict(
                        color=['#ef4444', '#f59e0b', '#667eea', '#10b981'],
                        line=dict(color='white', width=2)
                    ),
                    text=severity_data['Count'],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("### 📱 Source Distribution")
            source_data = pd.DataFrame({
                'Source': ['Reddit', 'FDA', 'Twitter', 'Forums'],
                'Events': [89, 67, 54, 37]
            })
            
            fig2 = go.Figure(data=[go.Pie(
                labels=source_data['Source'],
                values=source_data['Events'],
                hole=0.6,
                marker=dict(
                    colors=['#667eea', '#764ba2', '#10b981', '#f59e0b'],
                    line=dict(color='white', width=2)
                ),
                textinfo='label+percent'
            )])
            
            fig2.update_layout(
                plot_bgcolor='rgba(255,255,255,0)',
                paper_bgcolor='rgba(255,255,255,0)',
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                annotations=[dict(text='Sources', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    
    with tab2:
        st.markdown("### 🚨 Real-Time Alert Feed")
        
        # Live alert cards with animations
        alerts = [
            {
                'severity': 'high',
                'time': '2 min ago',
                'source': 'Reddit',
                'event': f"Multiple severe reactions to {drug_name}",
                'score': 8.7,
                'trend': 'rising'
            },
            {
                'severity': 'medium',
                'time': '15 min ago',
                'source': 'Twitter',
                'event': f"Vision changes with {drug_name}",
                'score': 6.2,
                'trend': 'stable'
            },
            {
                'severity': 'low',
                'time': '1 hour ago',
                'source': 'Forums',
                'event': f"Mild side effects reported",
                'score': 3.1,
                'trend': 'declining'
            }
        ]
        
        for alert in alerts:
            severity_class = f"alert-{alert['severity']}"
            icon = "🔴" if alert['severity'] == 'high' else "🟡" if alert['severity'] == 'medium' else "🟢"
            trend_icon = "📈" if alert['trend'] == 'rising' else "📊" if alert['trend'] == 'stable' else "📉"
            
            st.markdown(f"""
                <div class="alert-card {severity_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 1.5rem;">{icon}</span>
                            <strong style="font-size: 1.1rem; margin-left: 10px;">Severity: {alert['score']}/10</strong>
                            <span style="margin-left: 20px;">{trend_icon} {alert['trend'].title()}</span>
                        </div>
                        <small style="color: rgba(255,255,255,0.8);">{alert['time']}</small>
                    </div>
                    <p style="margin: 1rem 0; color: white; font-size: 1rem;">{alert['event']}</p>
                    <div style="display: flex; gap: 1rem;">
                        <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                            📍 {alert['source']}
                        </span>
                        <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                            👥 12 reports
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📈 Advanced Analytics")
        
        # Trend chart with gradient
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'Critical': np.random.randint(0, 5, 30),
            'High': np.random.randint(5, 15, 30),
            'Medium': np.random.randint(20, 50, 30),
            'Low': np.random.randint(50, 200, 30)
        })
        
        fig = go.Figure()
        
        colors = ['#ef4444', '#f59e0b', '#667eea', '#10b981']
        for i, severity in enumerate(['Critical', 'High', 'Medium', 'Low']):
            fig.add_trace(go.Scatter(
                x=trend_data['Date'],
                y=trend_data[severity],
                name=severity,
                mode='lines',
                line=dict(color=colors[i], width=3),
                fill='tonexty' if i > 0 else 'tozeroy',
                fillcolor=f'rgba{tuple(list(int(colors[i][j:j+2], 16) for j in (1, 3, 5)) + [0.1])}'
            ))
        
        fig.update_layout(
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0)',
            height=400,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🗺️ Geographic Distribution")
        
        # Placeholder for map
        st.markdown("""
            <div style="background: rgba(255,255,255,0.9); border-radius: 16px; padding: 2rem; text-align: center;">
                <img src="https://via.placeholder.com/800x400/667eea/ffffff?text=Interactive+Heat+Map" style="width: 100%; border-radius: 12px;">
                <p style="margin-top: 1rem; color: #667eea;">Real-time geographic distribution of adverse events</p>
            </div>
        """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown("### 📄 Compliance Report Generator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
                <div class="feature-card" style="background: rgba(255,255,255,0.95); padding: 2rem;">
                    <h4 style="color: #667eea; margin-bottom: 1rem;">Report Summary</h4>
                    <div style="color: #333;">
                        <p><strong>Generated:</strong> {}</p>
                        <p><strong>Drug:</strong> {}</p>
                        <p><strong>Period:</strong> {}</p>
                        <p><strong>Total Events:</strong> 247</p>
                        <p><strong>Critical Alerts:</strong> 3</p>
                        <p><strong>Recommendation:</strong> Immediate investigation required</p>
                    </div>
                </div>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M"), drug_name, time_range), unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("📥 Download PDF Report", use_container_width=True)
            st.button("📧 Email to Team", use_container_width=True)
            st.button("📤 Submit to FDA", use_container_width=True)

else:
    # Enhanced welcome screen
    st.markdown("""
        <div class="welcome-card">
            <h2 style="color: #667eea; font-size: 2.5rem; text-align: center; margin-bottom: 2rem;">
                Welcome to ComplianceWatch
            </h2>
            <p style="color: #333; font-size: 1.2rem; text-align: center; margin-bottom: 3rem;">
                Detect adverse drug reactions <strong style="color: #667eea;">48 hours faster</strong> than traditional monitoring
            </p>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; margin-bottom: 3rem;">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
                    <h4 style="color: #667eea;">Real-Time Monitoring</h4>
                    <p style="color: #666;">24/7 surveillance across all platforms</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
                    <h4 style="color: #667eea;">AI-Powered Analysis</h4>
                    <p style="color: #666;">GPT-4 severity scoring</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                    <h4 style="color: #667eea;">FDA Ready Reports</h4>
                    <p style="color: #666;">Compliance-ready documentation</p>
                </div>
            </div>
            
            <div style="background: linear-gradient(135deg, #667eea15, #764ba215); padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: #667eea; margin-bottom: 1rem;">⚡ Quick Start Guide</h4>
                <ol style="color: #333; margin-left: 1rem;">
                    <li>Enter the drug name you want to monitor</li>
                    <li>Select your preferred data sources</li>
                    <li>Set your monitoring parameters</li>
                    <li>Click "Start Monitoring" to begin</li>
                </ol>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 3rem 0; color: rgba(255,255,255,0.8);">
        <p>ComplianceWatch © 2025 | Protecting Patients, Preserving Trust</p>
        <p>Created by Atharva Deshpande | <a href="https://your-portfolio.com" style="color: #667eea;">View Portfolio</a></p>
    </div>
""", unsafe_allow_html=True)
