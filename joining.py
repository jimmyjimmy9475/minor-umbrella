import pandas as pd

tenancy = pd.read_csv(
    "tenancy_clean_without_dwelling.csv",
    dtype={"Location Id": "string",'Active Bonds':'Int64',
    'Median Rent':'Int64',}
)



listings = pd.read_csv(
    "listings_SA2.csv",
    dtype={"id": "string", "sa2": "string", 'price': 'Int64'}
)



tenancy = tenancy.rename(columns={"Location Id": "sa2"})
listings["year_quarter"] = pd.to_datetime(
    listings["month_year"],
    format="%B-%Y"
).dt.to_period("Q").astype(str)



tenancy["year_quarter"] = (
    tenancy["year_quarter"].str.replace("_", "", regex=False)
)



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


joined.to_csv("listings_tenancy_joined.csv", index=False)



