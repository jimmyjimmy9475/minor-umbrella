import pandas as pd
from pathlib import Path

folder = Path(__file__).resolve().parent


tenancy = pd.read_csv(
    folder / "tenancy_data" / "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv",
    dtype={"Location Id": "string"}
)

listings = pd.read_csv(
    folder / "listings_SA2.csv",
    dtype={"id": "string", "sa2": "string"}
)

listings.columns = listings.columns.str.strip()
tenancy.columns = tenancy.columns.str.strip()


tenancy = tenancy.loc[
    tenancy["Dwelling Type"].astype("string").str.strip().eq("ALL")
    & tenancy["Number Of Beds"].astype("string").str.strip().eq("ALL")
].copy()

if tenancy.empty:
    raise ValueError("No records found with both categories set to ALL.")

tenancy = tenancy.rename(columns={"Location Id": "sa2"})


for df in [listings, tenancy]:
    df["sa2"] = df["sa2"].str.strip().replace("", pd.NA)


needs_review = listings["sa2"].eq("363800").fillna(False)
listings = listings.loc[~needs_review].copy()


listings["quarter"] = pd.to_datetime(
    listings["month_year"].str[:3]
    + "-"
    + listings["month_year"].str[-4:],
    format="%b-%Y"
).dt.to_period("Q")

tenancy["quarter"] = pd.to_datetime(
    tenancy["TimeFrame"]
).dt.to_period("Q")



tenancy = tenancy.dropna(subset=["sa2", "quarter"])

tenancy = tenancy.loc[
    tenancy["quarter"].isin(listings["quarter"].dropna().unique())
].copy()


if tenancy.duplicated(["sa2", "quarter"]).any():
    raise ValueError(
        "Multiple ALL records remain per area and quarter."
    )

tenancy_clean = tenancy[
    ["sa2", "quarter", "Median Rent", "Active Bonds"]
].copy()

for column in ["Median Rent", "Active Bonds"]:
    tenancy_clean[column] = pd.to_numeric(
        tenancy_clean[column], errors="raise"
    )


listings = listings[
    [
        "id", "sa2", "neighbourhood", "quarter", "month_year",
        "room_type", "price", "minimum_nights", "availability_365"
    ]
].copy()

listings["price"] = pd.to_numeric(listings["price"], errors="raise")

if listings[["id", "sa2", "quarter", "month_year"]].isna().any().any():
    raise ValueError("Resolve missing Airbnb identifiers or join keys.")

if listings.duplicated(["id", "month_year"]).any():
    raise ValueError("Check duplicate Airbnb listing-month records.")


joined = listings.merge(
    tenancy_clean,
    on=["sa2", "quarter"],
    how="left",
    validate="many_to_one"
)


joined = joined[
    [
        "sa2", "neighbourhood", "quarter", "month_year",
        "id", "room_type", "price", "minimum_nights",
        "availability_365", "Median Rent", "Active Bonds"
    ]
].sort_values(
    ["sa2", "quarter", "id", "month_year"]
).reset_index(drop=True)

joined.insert(0, "row_number", range(1, len(joined) + 1))

central = joined.loc[joined["sa2"].eq("326600")]
central_median = central["price"].median()

print(f"\nChristchurch Central median Airbnb price: ${central_median:.2f}")

joined.to_csv(
    folder / "listings_tenancy_joined.csv",
    index=False
)