
import pandas as pd


def generate_financial_analysis(df, year):
    """
    Generate financial commentary using calculated
    financial metrics.

    All financial values are in USD millions.
    """

    current = df[df["Year"] == year].iloc[0]

    previous = df[df["Year"] == year - 1]

    revenue = current["Revenue"]
    net_income = current["Net Income"]
    operating_margin = current["Operating Margin (%)"]
    net_margin = current["Net Margin (%)"]

    insights = []

    # 1. Revenue analysis
    if not previous.empty:
        previous_revenue = previous.iloc[0]["Revenue"]

        growth = (
            (revenue / previous_revenue) - 1
        ) * 100

        if growth > 0:
            insights.append(
                f"Revenue increased by {growth:.2f}% "
                f"year over year, reaching "
                f"${revenue / 1000:,.2f} billion."
            )
        elif growth < 0:
            insights.append(
                f"Revenue declined by {abs(growth):.2f}% "
                f"year over year."
            )
        else:
            insights.append(
                "Revenue remained unchanged "
                "compared with the previous year."
            )
    else:
        insights.append(
            "No previous-year data is available "
            "for revenue growth comparison."
        )

    # 2. Operating profitability
    insights.append(
        f"Operating margin was {operating_margin:.2f}%, "
        f"meaning the company generated approximately "
        f"${operating_margin / 100:.2f} in operating "
        f"profit per dollar of revenue."
    )

    # 3. Net profitability
    insights.append(
        f"Net income reached "
        f"${net_income / 1000:,.2f} billion, "
        f"representing a net profit margin "
        f"of {net_margin:.2f}%."
    )

    # 4. Compare operating margins
    if not previous.empty:
        previous_margin = previous.iloc[0][
            "Operating Margin (%)"
        ]

        change = operating_margin - previous_margin

        if change > 0:
            insights.append(
                f"Operating margin improved by "
                f"{change:.2f} percentage points "
                f"compared with the previous year."
            )
        elif change < 0:
            insights.append(
                f"Operating margin decreased by "
                f"{abs(change):.2f} percentage points."
            )
        else:
            insights.append(
                "Operating margin remained unchanged."
            )

    return insights
