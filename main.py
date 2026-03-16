import streamlit as st
import pandas as pd
import os
import sys

# Ensure the local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.mock_generator import generate_mock_data
from agents.orchestrator_agent import OrchestratorAgent
from datetime import datetime

st.set_page_config(page_title="Pulse - Social Risk Engine", layout="wide")

# Cached data processing to avoid re-running on every Streamlit interaction
@st.cache_data
def load_and_process_data():
    data_path = "mock_social_data.csv"
    if not os.path.exists(data_path):
        st.info("Generating mock data...")
        df = generate_mock_data(200)
        df.to_csv(data_path, index=False)
        
    orchestrator = OrchestratorAgent(data_path)
    results = orchestrator.run_pipeline()
    return pd.DataFrame(results)

def main():
    st.title("🚨 Pulse – Social Risk Engine (Phase 1)")
    st.markdown("Early-stage misinformation and social panic detection from streaming text data using Multi-Agent workflow.")
    
    st.sidebar.header("🧪 Test Your Own Post")
    custom_text = st.sidebar.text_area("Enter a simulated post:")
    test_button = st.sidebar.button("Analyze Post")

    if test_button and custom_text.strip():
        orchestrator = OrchestratorAgent("mock_social_data.csv")
        mock_post = {
            "id": 9999,
            "timestamp": datetime.now().isoformat(),
            "username": "custom_user",
            "text": custom_text,
            "provided_location": "Unknown"
        }
        with st.sidebar:
            with st.spinner("Analyzing..."):
                result = orchestrator.process_post(mock_post)
            st.subheader("Result")
            if result['label'] == 'HIGH':
                st.error(f"**Risk Label:** {result['label']} (Score: {result['score']})")
            elif result['label'] == 'MEDIUM':
                st.warning(f"**Risk Label:** {result['label']} (Score: {result['score']})")
            else:
                st.success(f"**Risk Label:** {result['label']} (Score: {result['score']})")
                
            st.write(f"**Explanation:** {result['explanation']}")
            st.write(f"**Extracted Location:** {result['extracted_location']}")
            if result['label'] in ['HIGH', 'MEDIUM']:
                st.info(f"**PSA (EN):** {result['psa_en']}")
                
    with st.spinner("Processing data stream through AI Agents..."):
        df = load_and_process_data()
        
    if df.empty:
        st.error("No data processed. Please check the data source.")
        return
        
    # Formatting timestamp for charts
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 1. Top Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Posts Analyzed", len(df))
    with col2:
        high_risk_count = len(df[df['label'] == 'HIGH'])
        st.metric("High Risk Posts", high_risk_count)
    with col3:
        bot_count = len(df[df['is_bot'] == True])
        st.metric("Suspected Bots Activity", bot_count)
    with col4:
        avg_risk = df['score'].mean()
        st.metric("Average Risk Score", f"{avg_risk:.1f}/100")
        
    st.divider()
    
    # 2. Charts and Visualization
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Risk Score Over Time")
        # Sort values just in case
        risk_time_df = df.sort_values("timestamp").set_index('timestamp')[['score']]
        # Resample or just plot as is for stream effect
        st.line_chart(risk_time_df)
        
    with col_chart2:
        st.subheader("Geographic Risk Distribution")
        # Count posts by location where risk is medium/high
        risky_geo = df[df['label'].isin(['HIGH', 'MEDIUM'])]['location'].value_counts()
        if not risky_geo.empty:
            st.bar_chart(risky_geo)
        else:
            st.info("No Medium/High risk geo data to display.")
        
    st.divider()
    
    # 3. High Risk Flagged Posts & PSAs
    st.subheader("⚠️ High Risk Alerts & Counter-Messaging")
    
    high_risk_df = df[df['label'] == 'HIGH'].sort_values('timestamp', ascending=False)
    
    if not high_risk_df.empty:
        for idx, row in high_risk_df.head(5).iterrows():
            with st.expander(f"🔴 Score: {row['score']} | Loc: {row['location']} | User: {row['username']}"):
                st.write(f"**Original Post:** {row['text']}")
                st.write(f"**Explanation:** {row['explanation']}")
                st.write(f"**Bot Probability:** {row['bot_probability']:.2f} ({'Bot' if row['is_bot'] else 'Human'})")
                
                st.markdown("---")
                st.markdown("**🛡️ Suggested Counter-Message (PSA)**")
                st.info(f"🇺🇸 EN: {row['psa_en']}")
                st.success(f"🇮🇳 HI: {row['psa_hi']}")
    else:
        st.success("No high-risk posts detected in this time window.")
        
    st.divider()
    
    # 4. Filterable Data Table
    st.subheader("All Processed Posts")
    col_filter1, col_filter2 = st.columns([1, 1])
    with col_filter1:
        filter_label = st.selectbox("Filter by Risk Level", ["ALL", "HIGH", "MEDIUM", "LOW"])
    with col_filter2:
        filter_bot = st.checkbox("Show only Bot Activity")
    
    filtered_df = df
    if filter_label != "ALL":
        filtered_df = filtered_df[filtered_df['label'] == filter_label]
    if filter_bot:
        filtered_df = filtered_df[filtered_df['is_bot'] == True]
        
    display_cols = ["timestamp", "username", "text", "location", "score", "label", "bot_probability", "explanation"]
    st.dataframe(filtered_df[display_cols].sort_values("timestamp", ascending=False), use_container_width=True)

if __name__ == "__main__":
    main()
