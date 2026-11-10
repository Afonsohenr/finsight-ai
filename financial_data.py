
import requests
import pandas as pd

# SEC company identifiers
COMPANIES = {
    "Microsoft": "0000789019",
    "Apple": "0000320193",
    "Alphabet": "0001652044",
    "Amazon": "0001018724",
    "NVIDIA": "0001045810"
}


# Replace with your own contact email before running
USER_AGENT = "FinSightAI Student afonsohenr213@gmail.com"



def get_financial_data(company_name="Microsoft"):
    cik = COMPANIES[company_name]
    url = (
        "https://data.sec.gov/api/xbrl/companyfacts/"
        f"CIK{cik}.json"
    )


    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=30
    )
    response.raise_for_status()

    company = response.json()
    facts = company["facts"]["us-gaap"]

    # Three income statement metrics

    # Different companies may use different SEC revenue tags
    revenue_tags = [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet"
    ]

    revenue_tag = None
    latest_end = None

    for tag in revenue_tags:
        if tag not in facts:
            continue

        records = facts[tag]["units"].get("USD", [])

        annual_records = [
            r for r in records
            if r.get("form") == "10-K"
            and r.get("fp") == "FY"
            and r.get("start")
            and r.get("end")
            and 350 <= (
                pd.Timestamp(r["end"]) -
                pd.Timestamp(r["start"])
            ).days <= 380
        ]

        if annual_records:
            newest = max(r["end"] for r in annual_records)

            if latest_end is None or newest > latest_end:
                latest_end = newest
                revenue_tag = tag

    if revenue_tag is None:
        raise ValueError("No supported annual revenue tag found.")

    tags = {
        "Revenue": revenue_tag,
        "Operating Income": "OperatingIncomeLoss",
        "Net Income": "NetIncomeLoss"
    }

    # Find Microsoft's latest annual 10-K filing
    revenue_records = facts[tags["Revenue"]]["units"]["USD"]

    annual_filings = [
        r for r in revenue_records
        if r.get("form") == "10-K"
        and r.get("fp") == "FY"
        and r.get("start")
        and r.get("end")
        and 350 <= (
            pd.Timestamp(r["end"]) -
            pd.Timestamp(r["start"])
        ).days <= 380
    ]

    if not annual_filings:
        raise ValueError("No annual SEC filings found.")

    latest = max(
        annual_filings,
        key=lambda r: (r["end"], r["filed"])
    )

    accession = latest["accn"]
    latest_year = int(latest["end"][:4])
    years = list(range(latest_year - 2, latest_year + 1))

    
    results = {
        "Year": years,
        "Period Start": [None] * len(years),
        "Period End": [None] * len(years)
    }


    for label, tag in tags.items():
        records = facts[tag]["units"]["USD"]

        # Use comparable figures from one annual filing
        matching = [
            r for r in records
            if r.get("accn") == accession
            and r.get("start")
            and r.get("end")
            and 350 <= (
                pd.Timestamp(r["end"]) -
                pd.Timestamp(r["start"])
            ).days <= 380
        ]

        values = {}

        
        for r in matching:
            year = int(r["end"][:4])

            if year in years:
                values[year] = r["val"] / 1_000_000

                # Record fiscal period dates from revenue
                if label == "Revenue":
                    index = years.index(year)
                    results["Period Start"][index] = r["start"]
                    results["Period End"][index] = r["end"]


        results[label] = [values.get(y) for y in years]

    df = pd.DataFrame(results)

    if df[["Period Start", "Period End"]].isna().any().any():
        raise ValueError(
            "Missing fiscal reporting period dates."
        )

    if df.isna().any().any():
        raise ValueError(
            "Missing SEC financial values. "
            "Review available tags and filing periods."
        )

    df["Revenue Growth (%)"] = (
        df["Revenue"].pct_change() * 100
    )

    df["Operating Margin (%)"] = (
        df["Operating Income"] / df["Revenue"] * 100
    )

    df["Net Margin (%)"] = (
        df["Net Income"] / df["Revenue"] * 100
    )

    return company["entityName"], df, accession
