
# 📊 FinSight AI

### AI-Powered Financial Statement Analysis

FinSight AI is an interactive financial analysis platform built with Python, Streamlit, and Google Gemini.

It retrieves financial statement data from the U.S. Securities and Exchange Commission (SEC) and helps users analyze company performance.

## Features

- SEC EDGAR financial data integration
- Analysis of Microsoft, Apple, Alphabet, Amazon, and NVIDIA
- Revenue, operating income, and net income analysis
- Revenue growth and profitability ratios
- Interactive financial performance charts
- Side-by-side company comparisons
- Fiscal reporting period transparency
- AI-generated financial analysis using Google Gemini
- Downloadable financial data and reports

## Technologies

- Python
- Streamlit
- Pandas
- Plotly
- SEC EDGAR API
- Google Gemini API

## Financial Metrics

FinSight AI calculates:

- Revenue Growth
- Operating Margin
- Net Profit Margin

The application uses financial data from annual SEC filings.

## How to Run Locally

1. Clone this repository.
2. Install dependencies:

   pip install -r requirements.txt

3. Configure your Gemini API key using
   Streamlit secrets:

   GEMINI_API_KEY = "your_api_key"

4. Start the application:

   streamlit run app.py

## Data Sources

Financial information is retrieved from SEC EDGAR company facts.

Company comparisons display fiscal reporting dates to help users identify differences between reporting periods.

## Disclaimer

FinSight AI is an educational financial analysis project.

AI-generated insights may contain inaccuracies and should not be considered investment advice.
