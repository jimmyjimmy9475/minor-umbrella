import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

months = {
    "June": "June-2026",
    "May": "May-2026",
    "April": "April-2026",
    "March": "March-2026",
    "Feb": "Feb-2026",
    "Jan": "Jan-2026",
    "Dec": "Dec-2025",
    "Nov": "Nov-2025",
    "Oct": "Oct-2025"
}

dfs = []

for month, month_year in months.items():
    # Read the file
    df = pd.read_csv(f"airbnb_data/listings_{month}.csv")

    # Clean neighbourhood_group
    df["neighbourhood_group"] = (
        df["neighbourhood_group"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    # Filter Christchurch City
    df_chch = df[df["neighbourhood_group"] == "Christchurch City"].copy()

    # Add Month-Year column
    df_chch["month_year"] = month_year

    dfs.append(df_chch)

# Combine all months
df_chch_all = pd.concat(dfs, ignore_index=True)

# Check
print(df_chch_all[["month_year", "neighbourhood_group"]].head())

print(df_chch_all.tail())

print(df_chch_all.describe())

# Print number of missing values in each column
print(df_chch_all.isnull().sum())

print(df_chch_all[['price', 'minimum_nights', 'number_of_reviews', 'availability_365', 'calculated_host_listings_count', 'number_of_reviews_ltm']].describe())

df_chch_all.to_csv("listings_concat.csv")