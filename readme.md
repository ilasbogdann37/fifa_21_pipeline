# ⚽ Data Engineering Project

An end-to-end Data Engineering and GenAI pipeline applied to sports analytics (SoFIFA/Football Dataset), specifically designed to simulate core production use cases in sports analytics, fantasy sports, and hype correlation

## 🚀 Project Architecture
1. **Extract**: Ingestion of raw football data containing over 18,000 records and 77 complex columns.
2. **Transform (Pandas)**: A robust, custom cleaning pipeline built to handle missing values (`NaN` fields in `Hits`), parse and convert mixed metrics (`Height` from metric/imperial formats, `Weight` from lbs/kg), strip special characters (`★`), and normalize financial metrics (`Value`, `Wage`, `Release Clause` from text-based `€M`/`€K` expressions into accurate numeric types).
3. **Analytics (DuckDB & SQL)**: Loading the structured datasets into a high-performance, in-memory analytical database engine to run complex SQL queries and extract business insights (Underpriced Gems, Hype vs. Salary Correlation, Veteran Bargains, and Club Valuation Aggregations).
4. **GenAI Layer (g4f/GPT-4)**: Integration of a Large Language Model (LLM) that ingests the structured markdown tables outputted by SQL and automatically translates them into narrative, journalistic reports tailored for sports bettors and analysts across all dashboard modules.
5. **UI Layer (Streamlit)**: An interactive web dashboard built to visualize the structured data streams and trigger the automated AI reporting engine with a single click.

## 🛠️ Tech Stack
- **Language**: Python 3
- **Data Wrangling**: Pandas, NumPy
- **Database / SQL Engine**: DuckDB (OLAP optimized)
- **GenAI**: g4f (GPT-4 Integration), Prompt Engineering
- **Dashboard UI**: Streamlit
- **OS Environment**: Fedora Linux

## 📦 Installation & Setup

1. Clone the repository:
```bash
git clone <your-github-link-here>
cd faducl-data-pipeline

2. Configure the virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Run the ETL cleaning pipeline:

python clean_data.py

4.Launch the interactive Streamlit web dashboard:

streamlit run app.py