import pandas as pd

# treat location as string
data_types = {
    'Location Id': str,
    'Active Bonds':'Int64',
    'Median Rent':'Int64',
    'Upper Quartile Rent':'Int64',
    'Lower Quartile Rent':'Int64',
}

# data must be in tenancy_data folder, and named "Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
df = pd.read_csv("tenancy_data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv", dtype=data_types)

assert df['TimeFrame'].notna().all(), "TimeFrame has Na values"
# Convert the "TimeFrame" column to datetime data type
df["TimeFrame"] = pd.to_datetime(df["TimeFrame"])

# Filter the dataset to dates after 1 October 2025
df = df[df["TimeFrame"] >= "2025-10-01"]

quarter = {
    pd.Timestamp("2025-10-01"): "2025_Q4",
    pd.Timestamp("2026-01-01"): "2026_Q1",
    pd.Timestamp("2026-04-01"): "2026_Q2"
}

df["year_quarter"] = df["TimeFrame"].map(quarter)

# remove national aggregate of bonds
df = df[df['Location Id']!='-99']

# remove aggregation of dwelling types
df = df[df['Dwelling Type']!='ALL']

# only include aggregated number of beds
df = df[df['Number Of Beds']=='ALL']

# remove unrequired cols
cols_to_remove = [
    'Number Of Beds',
    'Total Bonds',
    'Closed Bonds',
    'Geometric Mean Rent',
    'Log Std Dev Weekly Rent',
]
df = df.drop(
    columns=cols_to_remove
)

num_before = len(df['Location Id'])
df = df[df['Location Id'].notna()] # remove na
num_after = len(df['Location Id'])

# Check some assumptions
assert df['year_quarter'].notna().all(), "year_quarter has Na values"
assert df['Location Id'].notna().all(), "Location Id has Na values"
assert (df['Location Id'] != '-99').all(), "Location Id has -99 values"
assert df['Dwelling Type'].notna().all(), "Dwelling Type has Na values"
assert df.duplicated(['Location Id', 'year_quarter', 'Dwelling Type']).sum() == 0, "There are duplicate rows with same year_quarter/Location/Dwelling Type"

print(f'Rows removed due to NA location: {num_before-num_after}')
print(df)

df.to_csv(
    "tenancy_clean.csv",
    index=False
)
