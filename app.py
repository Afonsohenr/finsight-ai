
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FinSight AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 FinSight AI")
st.write("Your AI-powered financial analysis platform")

# Sample financial data (USD millions)
# These are NOT actual Microsoft figures.
data = {
    "Year": [2023, 2024, 2025],
    "Revenue": [100000, 115000, 135000],
    "Operating Income": [30000, 36000, 43000],
    "Net Income": [25000, 29000, 35000]
}

df = pd.DataFrame(data)

df["Revenue Growth (%)"] = df["Revenue"].pct_change() * 100
df["Operating Margin (%)"] = (
    df["Operating Income"] / df["Revenue"] * 100
)
df["Net Margin (%)"] = (
    df["Net Income"] / df["Revenue"] * 100
)

year = st.selectbox("Select Fiscal Year", df["Year"])

selected = df[df["Year"] == year].iloc[0]

col1, col2, col3 = st.columns(3)

col1.metric("Revenue", f"${selected['Revenue']:,.0f}M")
col2.metric("Net Income", f"${selected['Net Income']:,.0f}M")
col3.metric(
    "Operating Margin",
    f"{selected['Operating Margin (%)']:.2f}%"
)

st.subheader("Financial Performance")

fig = px.line(
    df,
    x="Year",
    y=["Revenue", "Net Income"],
    markers=True
)

st.plotly_chart(fig, width="stretch")

st.subheader("Financial Data")
st.dataframe(df.round(2), hide_index=True)

st.download_button(
    "Download Financial Report",
    df.to_csv(index=False),
    "financial_report.csv",
    "text/csv"
)

st.caption(
    "Demo data only. Real SEC financial statements coming soon."
)
