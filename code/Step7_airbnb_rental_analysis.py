"""
Analyse the dataset, price gap, chch central
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

listing_tenancy_filepath = ROOT / 'output' / 'csv' / 'Step5_joined_listings_tenancy.csv'
geography_file = ROOT / 'data' / 'stat_area_data' / 'geographic-areas-table-2023.csv'
plot_filepath = ROOT / 'output' / 'image' / 'airbnb_vs_rental_price.png'

# LOAD DATA

joined = pd.read_csv(
    listing_tenancy_filepath,
    dtype={
        "sa2": "string", 
        "id": "string", 
        "airbnb_median_price": "Int64", 
        "tenancy_median_weekly_rent": "Int64", 
        "tenancy_active_bonds": "Int64"
        }
)

geography = pd.read_csv(
    geography_file,
    dtype={"SA22018_code": "string"}
)

joined.columns = joined.columns.str.strip()
geography.columns = geography.columns.str.strip()

joined["sa2"] = joined["sa2"].str.strip()
geography["SA22018_code"] = geography["SA22018_code"].str.strip()

# CHRISTCHURCH SA2-2018 LOOKUP

sa2_lookup = geography[
    ["SA22018_code", "SA22018_name", "TA2023_name"]
].drop_duplicates("SA22018_code")

sa2_lookup = sa2_lookup[
    sa2_lookup["TA2023_name"].eq("Christchurch City")
]



# MERGE GEOGRAPHIC INFORMATION

christchurch = joined.merge(
    sa2_lookup,
    left_on="sa2",
    right_on="SA22018_code",
    how="inner",
    validate="many_to_one"
)

if christchurch.empty:
    raise ValueError("No Christchurch records were found.")


# PRICE GAP

# Long-term rent is weekly, so convert it to a nightly value.
christchurch["long_term_price_per_night"] = (
    christchurch["tenancy_median_weekly_rent"] / 7
)

# Airbnb price is already per night.
christchurch["price_gap"] = (
    christchurch["airbnb_median_price"]
    - christchurch["long_term_price_per_night"]
)

# Missing Airbnb prices are retained in christchurch.
# They are excluded only from the price-gap calculation.
price_gap_data = christchurch.dropna(
    subset=["price_gap", "SA22018_name"]
)

price_gap_by_sa2 = (
    price_gap_data
    .groupby(
        ["sa2", "SA22018_name"],
        as_index=False
    )
    .agg(
        median_price_gap=("price_gap", "median"),
        mean_price_gap=("price_gap", "mean"),
        minimum_price_gap=("price_gap", "min"),
        maximum_price_gap=("price_gap", "max"),
    )
    .sort_values(
        "median_price_gap",
        ascending=False
    )
)

print("\n" + "=" * 70)
print("AIRBNB VS LONG-TERM RENTAL PRICE GAP")
print("=" * 70)

print(
    price_gap_by_sa2.head(10).to_string(index=False)
)

# AIRBNB VS LONG-TERM RENTAL PROPERTIES

property_comparison = (
    christchurch
    .groupby(
        ["sa2", "SA22018_name"],
        as_index=False
    )
    .agg(
        airbnb_properties=("airbnb_count", "max"),
        long_term_properties=("tenancy_active_bonds", "max"),
    )
)

property_comparison = property_comparison.sort_values(
    "airbnb_properties",
    ascending=False
)

print("\n" + "=" * 70)
print("AIRBNB VS LONG-TERM RENTAL PROPERTIES")
print("=" * 70)

print(
    property_comparison.head(15)
)

# PROPERTY COMPARISON PLOT

plot_properties = (
    property_comparison
    .head(15)
    .set_index("SA22018_name")
)

plot_properties[
    ["airbnb_properties", "long_term_properties"]
].plot(
    kind="bar",
    figsize=(14, 8)
)

plt.title(
    "Airbnb vs Long-Term Rental Properties by Christchurch SA2"
)

plt.xlabel("Christchurch SA2")
plt.ylabel("Number of properties")

plt.xticks(
    rotation=60,
    ha="right"
)

plt.legend(
    ["Airbnb properties", "Long-term rental properties"]
)

plt.tight_layout()

plt.savefig(
    plot_filepath,
    dpi=300,
    bbox_inches="tight"
)

# COMPLETION

print("\n" + "=" * 70)
print("Median AirBnb price for Christchurch Central")
print("=" * 70)

christchurch_central_data=joined[joined["sa2"]=='326600']
print(christchurch_central_data[["year_quarter", "airbnb_median_price"]])
