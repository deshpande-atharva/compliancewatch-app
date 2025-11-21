# compliancewatch_app.py - Fixed Version
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

# Custom CSS - Simplified and more compatible
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .alert-card {
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease;
    }
    
    .alert-high {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.1));
        border-left: 4px solid #ef4444;
    }
    
    .alert-medium {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
        border-left: 4px solid #f59e0b;
    }
    
    .alert-low {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        border-left: 4px solid #10b981;
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
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center; color: white; font-size: 3.5rem; font-weight: 800;'>ComplianceWatch</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.9); font-size: 1.2rem; font-weight: 400; letter-spacing: 2px; text-transform: uppercase;'>AI-Powered Pharmaceutical Monitoring</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.8);'>🟢 Live Monitoring Active</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 💊 Control Panel")
    st.markdown("Configure monitoring parameters")
    
    st.divider()
    
    # Drug selection
    st.markdown("### 🔬 Target Drug")
    drug_name = st.text_input(
        "Drug Name",
        placeholder="e.g., Ozempic, Keytruda",
        help="Enter the pharmaceutical drug name you want to monitor for adverse events",
        label_visibility="collapsed"
    )
    
    # Data source selection
    st.markdown("### 📡 Data Sources")
    data_sources = st.multiselect(
        "Select Sources",
        ["Reddit", "Twitter/X", "Facebook Groups", "Patient Forums", "FDA FAERS"],
        default=["Reddit", "FDA FAERS"],
        help="Choose which platforms to monitor for adverse event reports",
        label_visibility="collapsed"
    )
    
    # Time range
    st.markdown("### ⏱️ Time Period")
    time_range = st.selectbox(
        "Time Range",
        ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 90 Days"],
        help="Select the time period for historical data analysis",
        label_visibility="collapsed"
    )
    
    # Severity threshold
    st.markdown("### ⚠️ Alert Threshold")
    severity_threshold = st.slider(
        "Severity",
        min_value=1,
        max_value=10,
        value=5,
        help="Set minimum severity score (1-10) for alerts",
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Monitor button
    monitor_button = st.button("🚀 Start Monitoring", use_container_width=True, type="primary")
    
    # Stats in sidebar
    if monitor_button and drug_name:
        st.divider()
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Monitors", "4")
        with col2:
            st.metric("Total Alerts", "23")
        st.metric("System Health", "✅ Optimal")

# Main content area
if monitor_button and drug_name:
    # Loading animation
    with st.spinner('🔍 Analyzing data sources...'):
        time.sleep(1)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🚨 Live Alerts", "📈 Analytics", "🗺️ Geo Map", "📄 Reports"])
    
    with tab1:
        st.markdown("##### Last updated: just now")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Events",
                value="247",
                delta="23 from yesterday"
            )
        
        with col2:
            st.metric(
                label="Critical Alerts",
                value="3",
                delta="Immediate attention",
                delta_color="inverse"
            )
        
        with col3:
            st.metric(
                label="Detection Speed",
                value="48h faster",
                delta="vs traditional"
            )
        
        with col4:
            st.metric(
                label="Accuracy",
                value="94.7%",
                delta="2.3% improvement"
            )
        
        st.divider()
        
        # Charts
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
                        color=['#ef4444', '#f59e0b', '#667eea', '#10b981']
                    ),
                    text=severity_data['Count'],
                    textposition='outside'
                )
            ])
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
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
                    colors=['#667eea', '#764ba2', '#10b981', '#f59e0b']
                )
            )])
            
            fig2.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=False,
                annotations=[dict(text='Sources', x=0.5, y=0.5, font_size=20, showarrow=False)]
            )
            
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.markdown("### 🚨 Real-Time Alert Feed")
        
        # Alert 1 - High
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown("""
                <div class='alert-card alert-high'>
                    <strong>🔴 HIGH SEVERITY (8.7/10)</strong><br>
                    Multiple severe reactions to {} reported<br>
                    <small>📍 Reddit | 👥 12 reports | 📈 Rising</small>
                </div>
                """.format(drug_name), unsafe_allow_html=True)
            with col2:
                st.caption("2 min ago")
        
        # Alert 2 - Medium
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown("""
                <div class='alert-card alert-medium'>
                    <strong>🟡 MEDIUM SEVERITY (6.2/10)</strong><br>
                    Vision changes with {} reported<br>
                    <small>📍 Twitter | 👥 8 reports | 📊 Stable</small>
                </div>
                """.format(drug_name), unsafe_allow_html=True)
            with col2:
                st.caption("15 min ago")
        
        # Alert 3 - Low
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown("""
                <div class='alert-card alert-low'>
                    <strong>🟢 LOW SEVERITY (3.1/10)</strong><br>
                    Mild side effects reported<br>
                    <small>📍 Forums | 👥 3 reports | 📉 Declining</small>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption("1 hour ago")
    
    with tab3:
        st.markdown("### 📈 30-Day Trend Analysis")
        
        # Generate sample trend data
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
                line=dict(color=colors[i], width=2),
                stackgroup='one'
            ))
        
        fig.update_layout(
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
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("📊 **Average Daily Events:** 82.4")
        with col2:
            st.info("📈 **Trend:** Increasing (+12%)")
        with col3:
            st.info("⚠️ **Peak Day:** {}".format((datetime.now() - timedelta(days=3)).strftime("%B %d")))
    
    with tab4:
        st.markdown("### 🗺️ Geographic Distribution")
        
        # Create sample geo data
        geo_data = pd.DataFrame({
            'State': ['California', 'Texas', 'New York', 'Florida', 'Illinois'],
            'Events': [45, 38, 32, 28, 24],
            'Severity': ['High', 'Medium', 'High', 'Low', 'Medium']
        })
        
        # Display as a simple table with styling
        st.dataframe(
            geo_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Events": st.column_config.ProgressColumn(
                    "Events",
                    help="Number of reported events",
                    format="%d",
                    min_value=0,
                    max_value=50,
                ),
            }
        )
        
        st.info("🌍 Interactive map visualization would show real-time geographic distribution of adverse events")
    
    with tab5:
        st.markdown("### 📄 Compliance Report Generator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Report Summary")
            
            report_data = {
                "Generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Drug": drug_name,
                "Period": time_range,
                "Total Events": "247",
                "Critical Alerts": "3",
                "Data Sources": ", ".join(data_sources),
                "Recommendation": "⚠️ Immediate investigation required"
            }
            
            for key, value in report_data.items():
                st.write(f"**{key}:** {value}")
        
        with col2:
            st.markdown("#### Actions")
            st.button("📥 Download PDF", use_container_width=True)
            st.button("📧 Email to Team", use_container_width=True)
            st.button("📤 Submit to FDA", use_container_width=True)

else:
    # Welcome screen using native Streamlit components
    st.markdown("## Welcome to ComplianceWatch")
    st.markdown("### Detect adverse drug reactions **48 hours faster** than traditional monitoring")
    
    st.markdown("---")
    
    # Feature cards using columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔍")
        st.markdown("**Real-Time Monitoring**")
        st.caption("24/7 surveillance across all platforms")
    
    with col2:
        st.markdown("### 🤖")
        st.markdown("**AI-Powered Analysis**")
        st.caption("GPT-4 severity scoring")
    
    with col3:
        st.markdown("### 📊")
        st.markdown("**FDA Ready Reports**")
        st.caption("Compliance-ready documentation")
    
    st.markdown("---")
    
    # Quick Start Guide
    with st.expander("⚡ Quick Start Guide", expanded=True):
        st.markdown("""
        1. **Enter the drug name** you want to monitor in the sidebar
        2. **Select your preferred data sources** (Reddit, Twitter, FDA, etc.)
        3. **Set your monitoring parameters** (time range and severity threshold)
        4. **Click "Start Monitoring"** to begin real-time surveillance
        
        The system will immediately begin scanning selected platforms for adverse event reports,
        using AI to score severity and generate compliance-ready reports.
        """)
    
    # Info boxes
    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Tip:** Start with popular drugs like Ozempic or Keytruda to see sample data")
    with col2:
        st.success("🚀 **Ready to start?** Enter a drug name in the sidebar")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0;'>
        <p>ComplianceWatch © 2025 | Protecting Patients, Preserving Trust</p>
        <p>Created by Atharva Deshpande</p>
    </div>
    """,
    unsafe_allow_html=True
)
