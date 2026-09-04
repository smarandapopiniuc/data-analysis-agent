import streamlit as st
import psycopg2
import pandas as pd
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

st.set_page_config(
    page_title="Data Analysis Agent v2",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Data Analysis Agent v2")
st.markdown("*Connect to your PostgreSQL database and let the agent analyse it*")
st.divider()

# ── CONNECTION PANEL ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔌 Database Connection")
    host     = st.text_input("Host",     value="localhost")
    port     = st.text_input("Port",     value="5432")
    database = st.text_input("Database", value="northwind")
    username = st.text_input("Username", value="postgres")
    password = st.text_input("Password", type="password")
    connect  = st.button("Connect", type="primary")

# ── CONNECTION LOGIC ──────────────────────────────────────────────────────────
if "connected" not in st.session_state:
    st.session_state.connected = False
if "conn" not in st.session_state:
    st.session_state.conn = None

if connect:
    try:
        conn = psycopg2.connect(
            host=host, port=port, database=database,
            user=username, password=password
        )
        st.session_state.conn = conn
        st.session_state.connected = True
        st.sidebar.success("✅ Connected!")
    except Exception as e:
        st.sidebar.error(f"❌ Connection failed: {e}")

# ── MAIN PANEL ────────────────────────────────────────────────────────────────
if st.session_state.connected:
    conn = st.session_state.conn

    # Get list of tables
    tables_df = pd.read_sql("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """, conn)

    tables = tables_df["table_name"].tolist()

    st.subheader("📋 Available Tables")
    selected_table = st.selectbox("Select a table to analyse", tables)

    if selected_table:
        # Load selected table
        df = pd.read_sql(f"SELECT * FROM {selected_table} LIMIT 1000", conn)

        st.subheader(f"📊 Table: {selected_table}")
        st.dataframe(df.head(10), use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows (sample)", df.shape[0])
        with col2:
            st.metric("Columns", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())

        # SQL Query section
        st.divider()
        st.subheader("🔍 Run a SQL Query")
        query = st.text_area(
            "Write your SQL query",
            value=f"SELECT * FROM {selected_table} LIMIT 100",
            height=100
        )

        if st.button("▶ Run Query"):
            try:
                result_df = pd.read_sql(query, conn)
                st.dataframe(result_df, use_container_width=True)
                st.session_state.query_result = result_df
                st.session_state.query_text = query
            except Exception as e:
                st.error(f"Query error: {e}")

        # AI Analysis section
        st.divider()
        analysis_type = st.selectbox(
            "What kind of analysis would you like?",
            [
                "General overview — what does this table contain?",
                "Data quality assessment",
                "Key business insights from this data",
                "Business recommendations based on the data",
                "All of the above"
            ]
        )

        if st.button("🧠 Analyse with AI", type="primary"):
            with st.spinner("Agent is analysing your data..."):

                # Build context
                schema_info = f"Table: {selected_table}\nColumns: {list(df.columns)}\nData types: {df.dtypes.to_dict()}\nSample rows:\n{df.head(5).to_string()}\nStatistics:\n{df.describe().to_string()}"

                # Include SQL result if available
                extra_context = ""
                if "query_result" in st.session_state:
                    extra_context = f"\nUser also ran this SQL query: {st.session_state.query_text}\nResult:\n{st.session_state.query_result.head(10).to_string()}"

                prompt = f"""You are a senior data analyst presenting findings to a non-technical business audience.
The user is analysing a PostgreSQL database table and wants: {analysis_type}

Here is the table information:
{schema_info}
{extra_context}

Please provide a clear, structured analysis in plain business language — no code snippets.
Include:
1. What this table contains and its business purpose
2. Data quality observations
3. Key patterns or insights
4. 2-3 concrete business recommendations
5. Suggested next steps for deeper analysis

Write as if presenting to a business stakeholder who has no technical background."""

                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1500,
                    messages=[{"role": "user", "content": prompt}]
                )

                analysis = message.content[0].text

            st.subheader("🧠 Agent Analysis")
            st.markdown(analysis)

            st.download_button(
                label="📥 Download Report",
                data=analysis,
                file_name=f"{selected_table}_analysis.txt",
                mime="text/plain"
            )

else:
    st.info("👈 Connect to your database using the sidebar to get started")
    st.markdown("""
    **What's new in v2:**
    - 🔌 Direct PostgreSQL database connection
    - 📋 Browse all tables in your database
    - 🔍 Run custom SQL queries
    - 🧠 AI analysis of any table or query result
    - 📥 Downloadable reports per table
    """)