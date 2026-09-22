import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# FILE PATHS

folder = Path(__file__).resolve().parent

joined_file = folder / "listings_tenancy_joined.csv"

geography_file = (
    folder
    / "stat_area_data"
    / "geographic-areas-table-2023.csv"
)

# LOAD DATA


joined = pd.read_csv(
    joined_file,
    dtype={
        "sa2": "string",
        "id": "string"
    }
)

geography = pd.read_csv(
    geography_file,
    dtype={
        "SA22018_code": "string"
    }
)

# CLEAN COLUMN NAMES

joined.columns = joined.columns.str.strip()
geography.columns = geography.columns.str.strip()


# Clean SA2 codes

joined["sa2"] = joined["sa2"].str.strip()

geography["SA22018_code"] = (
    geography["SA22018_code"]
    .str.strip()
)

# CREATE CHRISTCHURCH SA2 LOOKUP


sa2_lookup = geography[
    [
        "SA22018_code",
        "SA22018_name",
        "TA2023_name"
    ]
].copy()


# Keep Christchurch City only

sa2_lookup = sa2_lookup[
    sa2_lookup["TA2023_name"].eq(
        "Christchurch City"
    )
].copy()


# Keep one record per SA2

sa2_lookup = sa2_lookup.drop_duplicates(
    subset=["SA22018_code"]
)

# MERGE GEOGRAPHIC INFORMATION

analysis = joined.merge(
    sa2_lookup,
    left_on="sa2",
    right_on="SA22018_code",
    how="left",
    validate="many_to_one"
)

# Keep Christchurch records

christchurch = analysis[
    analysis["TA2023_name"].eq(
        "Christchurch City"
    )
].copy()


if christchurch.empty:
    raise ValueError(
        "No Christchurch records were found."
    )

# CONVERT NUMERIC VARIABLES

christchurch["price"] = pd.to_numeric(
    christchurch["price"],
    errors="coerce"
)

christchurch["Median Rent"] = pd.to_numeric(
    christchurch["Median Rent"],
    errors="coerce"
)

christchurch["Active Bonds"] = pd.to_numeric(
    christchurch["Active Bonds"],
    errors="coerce"
)

# AIRBNB VS LONG-TERM RENTAL PRICE GAP

# Median Rent is weekly. Convert weekly rent to a nightly amount.

christchurch["long_term_price_per_night"] = (
    christchurch["Median Rent"] / 7
)

# Airbnb price is already per night.

christchurch["short_term_price_per_night"] = (
    christchurch["price"]
)

# Calculate the price difference for every Airbnb.

christchurch["price_gap"] = (
    christchurch["short_term_price_per_night"]
    - christchurch["long_term_price_per_night"]
)

# 7. PRICE GAP BY SA2

price_gap_by_sa2 = (
    christchurch
    .dropna(
        subset=[
            "price_gap",
            "SA22018_name"
        ]
    )
    .groupby(
        [
            "sa2",
            "SA22018_name"
        ],
        as_index=False
    )
    .agg(
        median_price_gap=(
            "price_gap",
            "median"
        ),
        mean_price_gap=(
            "price_gap",
            "mean"
        ),
        minimum_price_gap=(
            "price_gap",
            "min"
        ),
        maximum_price_gap=(
            "price_gap",
            "max"
        ),
        number_of_airbnbs=(
            "id",
            "nunique"
        )
    )
    .sort_values(
        "median_price_gap",
        ascending=False
    )
)

# DISPLAY PRICE GAP RESULTS

print()
print("=" * 70)
print(
    "QUESTION 1: AIRBNB VS LONG-TERM RENTAL PRICE GAP"
)
print("=" * 70)

print(
    price_gap_by_sa2.head(10).to_string(
        index=False
    )
)

# PLOT PRICE GAP DISTRIBUTION

top_locations = (
    price_gap_by_sa2
    .head(10)["SA22018_name"]
    .tolist()
)


plot_data = christchurch[
    christchurch["SA22018_name"].isin(
        top_locations
    )
].dropna(
    subset=["price_gap"]
)


plt.figure(figsize=(14, 8))

plot_data.boxplot(
    column="price_gap",
    by="SA22018_name",
    rot=60
)

plt.title(
    "Distribution of Airbnb vs Long-Term Rental "
    "Price Gaps"
)

plt.suptitle("")

plt.xlabel("Christchurch SA2")

plt.ylabel(
    "Price Gap ($ per night)"
)

plt.tight_layout()

plt.savefig(
    folder / "price_gap_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# AIRBNB VS LONG-TERM RENTAL PROPERTIES

# Number of unique Airbnb listings

airbnb_counts = (
    christchurch
    .groupby(
        [
            "sa2",
            "SA22018_name"
        ],
        as_index=False
    )
    .agg(
        airbnb_properties=(
            "id",
            "nunique"
        )
    )
)


# Number of long-term rental properties
# Active Bonds is used as the long-term rental property count.

long_term_counts = (
    christchurch
    .groupby(
        [
            "sa2",
            "SA22018_name"
        ],
        as_index=False
    )
    .agg(
        long_term_properties=(
            "Active Bonds",
            "first"
        )
    )
)

# 10. COMBINE PROPERTY COUNTS

property_comparison = airbnb_counts.merge(
    long_term_counts,
    on=[
        "sa2",
        "SA22018_name"
    ],
    how="left"
)


property_comparison = property_comparison.sort_values(
    "airbnb_properties",
    ascending=False
)

# DISPLAY PROPERTY RESULTS

print()
print("=" * 70)
print(
    "QUESTION 2: AIRBNB VS LONG-TERM RENTAL PROPERTIES"
)
print("=" * 70)

print(
    property_comparison.to_string(
        index=False
    )
)

# PLOT PROPERTY COMPARISON

plot_properties = (
    property_comparison
    .sort_values(
        "airbnb_properties",
        ascending=False
    )
    .head(15)
    .set_index("SA22018_name")
)


plot_properties[
    [
        "airbnb_properties",
        "long_term_properties"
    ]
].plot(
    kind="bar",
    figsize=(14, 8)
)


plt.title(
    "Airbnb vs Long-Term Rental Properties "
    "by Christchurch SA2"
)

plt.xlabel("Christchurch SA2")

plt.ylabel("Number of properties")

plt.xticks(
    rotation=60,
    ha="right"
)

plt.legend(
    [
        "Airbnb properties",
        "Long-term rental properties"
    ]
)

plt.tight_layout()

plt.savefig(
    folder / "airbnb_vs_longterm_properties.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# SAVE RESULTS

price_gap_by_sa2.to_csv(
    folder / "price_gap_by_sa2.csv",
    index=False
)


property_comparison.to_csv(
    folder / "property_comparison_by_sa2.csv",
    index=False
)


# COMPLETION MESSAGE

print()
print("=" * 70)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print()
print("Output files:")
print("  1. price_gap_by_sa2.csv")
print("  2. property_comparison_by_sa2.csv")
print("  3. price_gap_distribution.png")
print("  4. airbnb_vs_longterm_properties.png")