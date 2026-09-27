"""
Group airbnb listings by sa2 region and then join with tenency data on sa2
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

listings_filepath = ROOT / 'output' / 'csv' / 'Step4_listings_with_SA2.csv'
tenancy_filepath = ROOT / 'output' / 'csv' / 'Step3_cleaning_tenancy_data_without_dwelling.csv'
output_filepath = ROOT / 'output' / 'csv' / 'Step5_joined_listings_tenancy.csv'

tenancy = pd.read_csv(
    tenancy_filepath,
    dtype={
        "Location Id": "string",
        'Active Bonds':'Int64',
        'Median Rent':'Int64',
        }
)

listings = pd.read_csv(
    listings_filepath,
    dtype={
        "id": "string", 
        "sa2": "string", 
        'price': 'Int64'
        }
)

tenancy = tenancy.rename(columns={"Location Id": "sa2"})
listings["year_quarter"] = pd.to_datetime(
    listings["month_year"],
    format="%B-%Y"
).dt.to_period("Q").astype(str)

tenancy = tenancy[
    tenancy["year_quarter"].isin(listings["year_quarter"])
]

airbnb_summary = (
    listings.groupby(["sa2", "year_quarter"], as_index=False)
    .agg(
        airbnb_median_price=("price", "median"),
        airbnb_count=("id", "nunique")
    )
)

airbnb_summary["airbnb_median_price"] = (
    airbnb_summary["airbnb_median_price"].round().astype("Int64")
)

tenancy_summary = tenancy[
    ["sa2", "year_quarter", "Median Rent", "Active Bonds"]
].rename(columns={
    "Median Rent": "tenancy_median_weekly_rent",
    "Active Bonds": "tenancy_active_bonds"
})

joined = airbnb_summary.merge(
    tenancy_summary,
    on=["sa2", "year_quarter"],
    how="left",
    validate="one_to_one"
)

joined.insert(0, "row_number", range(1, len(joined) + 1))

joined.to_csv(output_filepath, index=False)



