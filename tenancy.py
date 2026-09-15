import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and explore the tenancy dataset

df_tenancy = pd.read_csv("Tenancy.csv")
print(df_tenancy.info())
print()
print(df_tenancy.head())
print()

# Convert the "TimeFrame" column to datetime data type
df_tenancy["TimeFrame"] = pd.to_datetime(df_tenancy["TimeFrame"])

# Filter the dataset
tenancy_filtered = df_tenancy[df_tenancy["TimeFrame"] >= "2025-10-01"].copy()
print(tenancy_filtered.info())
print()
print(tenancy_filtered["TimeFrame"].unique())

# Create the "year_quarter" column for October 2025 to June 2026
# "TimeFrame" represents the start date of each quarter
quarter = {
    pd.Timestamp("2025-10-01"): "2025_Q4",
    pd.Timestamp("2026-01-01"): "2026_Q1",
    pd.Timestamp("2026-04-01"): "2026_Q2"
}

tenancy_filtered["year_quarter"] = tenancy_filtered["TimeFrame"].map(quarter)

print(tenancy_filtered.head())
print()

# Data cleaning

#checking for duplicates
duplicated_rows = tenancy_filtered.duplicated().sum()
print("Number of duplicated rows:", duplicated_rows) 
print()
# Filter and count rows containing "Location Id" == -99.0
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).head(20))  # Explore the filtered data
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).count())  # Count the number of rows containing -99.0
print()
# Replace "Location Id" values of -99.0 with NaN
tenancy_filtered["Location Id"] = tenancy_filtered["Location Id"].replace(-99.0, np.nan)
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).count())  # Check whether any -99.0 values remain
print()
print(tenancy_filtered.isna().sum())

# drop rows containing missing value for location Id
tenancy_clean = tenancy_filtered.dropna(subset=["Location Id"])
print()

# Check for number of missing values
print(tenancy_clean.isna().sum())
print(tenancy_clean.shape)

# Number of rows befor and after cleaning
print("Rows before cleaning:", tenancy_filtered.shape[0])
print("Rows after cleaning:", tenancy_clean.shape[0])
print("Rows removed:", tenancy_filtered.shape[0] - tenancy_clean.shape[0])

# Save the cleaned dataset as a CSV file
tenancy_clean.to_csv("tenancy_cleaned.csv", index=False)

