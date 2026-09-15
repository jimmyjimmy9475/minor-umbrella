import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and explore the tenancy dataset

df_tenancy = pd.read_csv("Tenancy.csv")
print(df_tenancy.info())
print()
print(df_tenancy.head())
print()
print(df_tenancy.info())
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

# Data cleaning

# Filter and count rows containing "Location Id" == -99.0
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).head(20))  # Explore the filtered data
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).count())  # Count the number of rows containing -99.0

# Replace "Location Id" values of -99.0 with NaN
tenancy_filtered["Location Id"] = tenancy_filtered["Location Id"].replace(-99.0, np.nan)
print((tenancy_filtered[tenancy_filtered["Location Id"] == -99.0]).count())  # Check whether any -99.0 values remain

# Identify rows containing more than 40% missing values
rows_with_high_na = tenancy_filtered[(tenancy_filtered.isna().mean(axis=1) * 100) > 40]

# Define columns used to identify rows with missing rental information
cols = [
    "Location Id",
    "Median Rent",
    "Geometric Mean Rent",
    "Upper Quartile Rent",
    "Lower Quartile Rent",
    "Log Std Dev Weekly Rent"
]

# Identify rows containing missing values in any of the specified columns
missing_rows = tenancy_filtered[tenancy_filtered[cols].isna().any(axis=1)]

# Count the number of rows where all of the specified columns are missing
print(missing_rows[cols].isna().all(axis=1).sum())

# Identify rows where all of the specified columns are missing
all_missing = missing_rows[missing_rows[cols].isna().all(axis=1)]

print(all_missing.shape)

# Drop rows where all of the specified columns are missing
tenancy_clean = tenancy_filtered[
    ~tenancy_filtered[cols].isna().all(axis=1)
].copy()

print(tenancy_clean.isna().sum())
print(tenancy_clean.shape)

# Count dwelling types with missing "Number Of Beds" values
print(tenancy_clean[
        tenancy_clean["Number Of Beds"].isna()]["Dwelling Type"].value_counts())

# Number of rows befor and after cleaning
print("Rows before cleaning:", tenancy_filtered.shape[0])
print("Rows after cleaning:", tenancy_clean.shape[0])
print("Rows removed:", tenancy_filtered.shape[0] - tenancy_clean.shape[0])

# Save the cleaned dataset as a CSV file
tenancy_clean.to_csv("tenancy_clean.csv")

