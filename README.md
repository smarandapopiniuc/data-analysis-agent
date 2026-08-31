# 🤖 Data Analysis Agent

An AI-powered data analysis tool built with Python, Streamlit and Claude (Anthropic).

Upload any CSV file and receive an instant professional analysis report — including data quality assessment, key insights, pattern detection and business recommendations.

## ⚡ What it does

- Automatically profiles any CSV dataset
- Identifies data quality issues (missing values, outliers, type mismatches)
- Extracts key patterns and business insights
- Generates concrete recommendations
- Produces a downloadable analysis report

## 🛠️ Tech stack

- Python 3.11
- Streamlit — web interface
- Pandas — data processing
- Anthropic Claude API — AI analysis engine

## 🚀 How to run locally

```bash
# Clone the repository
git clone https://github.com/smarandapopiniuc/data-analysis-agent

# Navigate into the folder
cd data-analysis-agent

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
# Create a .env file with: ANTHROPIC_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

## ⚙️ Customisation

This agent is intentionally built as a **generic analytical foundation**.

Every organisation has its own data structures, KPI definitions, business logic and reporting requirements. This tool is designed to be extended and customised — potential adaptations include:

- **Domain-specific prompts** tailored to your industry (retail, finance, energy, public sector)
- **Custom KPI frameworks** aligned to your organisation's metrics
- **Branded report templates** matching your visual identity
- **Automated data source connections** (SQL databases, APIs, SharePoint)
- **Multi-dataset comparison** across time periods or business units
- **Alerting and scheduling** for recurring analysis workflows

If you are interested in a customised version for your organisation, feel free to reach out.

## 👤 Author

**Smaranda Popiniuc**
Data & AI Analyst | Brussels, Belgium
[linkedin.com/in/smarandapopiniuc](https://linkedin.com/in/smarandapopiniuc)

## 📄 Licence

MIT — free to use and adapt with attribution.