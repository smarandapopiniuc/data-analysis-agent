import streamlit as st
import pandas as pd
import anthropic
import os
from dotenv import load_dotenv
from io import StringIO

# Load API key
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Page config
st.set_page_config(
    page_title="Data Analysis Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Data Analysis Agent")
st.markdown("*Upload any CSV file and let the agent analyse it for you*")
st.divider()

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load and display the data
    df = pd.read_csv(uploaded_file)
    
    st.subheader("📊 Your Data")
    st.dataframe(df.head(10), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", df.shape[0])
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Missing Values", df.isnull().sum().sum())

    # Build data summary for the agent
    def build_summary(df):
        summary = f"""
DATASET OVERVIEW:
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {list(df.columns)}
- Data types: {df.dtypes.to_dict()}
- Missing values per column: {df.isnull().sum().to_dict()}

STATISTICAL SUMMARY:
{df.describe().to_string()}

FIRST 5 ROWS SAMPLE:
{df.head().to_string()}
"""
        return summary

    # Analysis button
    st.divider()
    
    analysis_type = st.selectbox(
        "What kind of analysis would you like?",
        [
            "General overview — what is this data about?",
            "Data quality assessment",
            "Key insights and patterns",
            "Business recommendations based on the data",
            "All of the above"
        ]
    )
    
    if st.button("🔍 Analyse with AI", type="primary"):
        with st.spinner("Agent is analysing your data..."):
            
            data_summary = build_summary(df)
            
            prompt = f"""You are a senior data analyst presenting findings to a non-technical business audience. A user has uploaded a CSV dataset and wants you to perform the following analysis: {analysis_type}

Here is the dataset information:
{data_summary}

Please provide a clear, structured analysis that any business stakeholder could understand.
Important: write in plain business language only — no code snippets, no technical syntax, no DataFrame operations.
Include:
1. What this dataset appears to be about
2. Data quality observations in plain language
3. Key patterns or insights you can identify
4. 2-3 concrete business recommendations with clear next steps
5. What additional data would add value

Be specific, use the actual column names and numbers from the data, and write as if presenting to a CEO or department head who has no technical background."""

            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = message.content[0].text
        
        st.subheader("🧠 Agent Analysis")
        st.markdown(analysis)
        
        # Download button for the analysis
        st.download_button(
            label="📥 Download Analysis Report",
            data=analysis,
            file_name="data_analysis_report.txt",
            mime="text/plain"
        )

else:
    st.info("👆 Upload a CSV file to get started")
    
    st.markdown("""
    **What this agent does:**
    - 📋 Explores your dataset automatically
    - 🔍 Identifies data quality issues
    - 💡 Extracts key insights and patterns  
    - 📈 Provides business recommendations
    - 📥 Generates a downloadable report
    """)