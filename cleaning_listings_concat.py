import pandas as pd


df_chch_all = pd.read_csv("listings_concat.csv")

df_chch_clean = df_chch_all.copy()

original_rows = len(df_chch_clean)

cols_to_remove = [
    "name",
    "host_id",
    "host_name",
    "neighbourhood_group",
    "reviews_per_month",
    "calculated_host_listings_count",
    "license",
    "number_of_reviews",
    "last_review",
    "number_of_reviews_ltm",
    "minimum_nights",
]

df_chch_clean = df_chch_clean.drop(
    columns=cols_to_remove
)

df_chch_clean[["latitude", "longitude"]] = (
    df_chch_clean[["latitude", "longitude"]].round(1)
)

rows_before = len(df_chch_clean)



print("Original rows:", original_rows)
print("Final rows:", len(df_chch_clean))
print(
    "Total rows removed:",
    original_rows - len(df_chch_clean)
)



df_chch_clean = df_chch_clean.drop(
    columns=["Unnamed: 0"],
    errors="ignore"
)

df_chch_clean = df_chch_clean.reset_index(drop=True)

df_chch_clean.insert(0, "row_number", range(1, len(df_chch_clean) + 1))

df_chch_clean.to_csv(
    "listings_concat_clean.csv",
    index=False
)

