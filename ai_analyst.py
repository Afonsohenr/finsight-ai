
import time
from google.genai import errors

import json
from google import genai


def generate_ai_report(df, year, company_name, api_key):
    """
    Generate an AI financial report using
    financial data from SEC filings.
    """

    # Select the current fiscal year
    current = df[df["Year"] == year].iloc[0]

    # Select the previous fiscal year, if available
    previous = df[df["Year"] == year - 1]

    # Create a structured financial summary
    financial_summary = {
        "company": company_name,
        "fiscal_year": int(year),
        "units": "USD millions",
        "revenue": float(current["Revenue"]),
        "operating_income": float(current["Operating Income"]),
        "net_income": float(current["Net Income"]),
        "operating_margin_pct": float(
            current["Operating Margin (%)"]
        ),
        "net_margin_pct": float(
            current["Net Margin (%)"]
        )
    }

    # Add previous-year comparisons
    if not previous.empty:
        prior = previous.iloc[0]

        financial_summary["previous_year"] = {
            "year": int(year - 1),
            "revenue": float(prior["Revenue"]),
            "operating_income": float(
                prior["Operating Income"]
            ),
            "net_income": float(prior["Net Income"]),
            "operating_margin_pct": float(
                prior["Operating Margin (%)"]
            )
        }

        financial_summary["revenue_growth_pct"] = float(
            current["Revenue Growth (%)"]
        )

    # Convert financial data into JSON
    financial_json = json.dumps(
        financial_summary,
        indent=2
    )

    # Instructions for the AI
    prompt = f"""
You are a professional corporate financial analyst.

Analyze the following SEC-derived financial metrics:

{financial_json}

Write a concise financial analysis report with:

1. Executive Summary
2. Revenue Performance
3. Profitability Analysis
4. Financial Strengths
5. Potential Risks and Limitations
6. Overall Assessment

Rules:
- Use only the supplied financial figures.
- Do not invent financial numbers.
- Do not invent causes of financial changes.
- Clearly distinguish facts from interpretations.
- If evidence is insufficient, say so.
- Do not assume revenue growth is sustainable.
- Do not give buy, sell, or hold recommendations.
- All monetary values are in USD millions.
- Convert to billions when useful.
- Explain the financial implications in clear language.
- Keep the report under 450 words.
- Do not attribute changes in financial performance to
  specific causes unless the supplied data supports them.
- Distinguish mathematical differences from explanations
  of what caused those differences.
- If prior-year data is available, explicitly calculate
  and interpret year-over-year revenue and profit growth.

"""

    # Connect to Gemini

    client = genai.Client(api_key=api_key)


    # Retry temporary Gemini server errors
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )
            break

        except errors.ServerError as error:
            if getattr(error, "code", None) not in (500, 502, 503, 504):
                raise

            if attempt == 2:
                raise

            time.sleep(2 ** (attempt + 1))

    if not response.text:
        raise ValueError("The AI returned an empty report.")

    return response.text
