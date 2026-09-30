"""
Filter tenancy data to just the time range of the airbnb dataset, and remove aggregate rows.
Produces two datasets, with and without dwelling breakdown.
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILEPATH = ROOT / 'data' / 'tenancy_data' / 'Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv'
STAT_AREA_FILEPATH = ROOT / 'data' / 'stat_area_data/geographic-areas-table-2023.csv'

OUTPUT_WITHDWELLING_FILEPATH = ROOT / 'output' / 'csv' / 'Step3_cleaning_tenancy_data_with_dwelling.csv'
OUTPUT_WITHOUT_DWELLING_FILEPATH = ROOT / 'output' / 'csv' / 'Step3_cleaning_tenancy_data_without_dwelling.csv'

MINIMUM_DATE = "2025-10-01"

# treat location as string
data_types = {
    'Location Id': str,
    'Active Bonds':'Int64',
    'Median Rent':'Int64',
    'Upper Quartile Rent':'Int64',
    'Lower Quartile Rent':'Int64',
}

df = pd.read_csv(INPUT_FILEPATH, dtype=data_types)

assert df['TimeFrame'].notna().all(), "TimeFrame has Na values"
# Convert the "TimeFrame" column to datetime data type
df["TimeFrame"] = pd.to_datetime(df["TimeFrame"])

# Filter the dataset to just what exists in the airbnb datset
df = df[df["TimeFrame"] >= MINIMUM_DATE]

quarter = {
    pd.Timestamp("2025-10-01"): "2025Q4",
    pd.Timestamp("2026-01-01"): "2026Q1",
    pd.Timestamp("2026-04-01"): "2026Q2"
}

df["year_quarter"] = df["TimeFrame"].map(quarter)

# remove national aggregate of bonds
df = df[df['Location Id']!='-99']

# only include aggregated number of beds
df = df[df['Number Of Beds']=='ALL']

# remove unrequired cols
cols_to_remove = [
    'Number Of Beds',
    'Total Bonds',
    'Closed Bonds',
]
df = df.drop(
    columns=cols_to_remove
)

num_before_removena = len(df['Location Id'])
df = df[df['Location Id'].notna()] # remove na
num_after_removena = len(df['Location Id'])

stat_areas = pd.read_csv(STAT_AREA_FILEPATH)

# Check some assumptions
assert df['year_quarter'].notna().all(), "year_quarter has Na values"
assert df['Location Id'].notna().all(), "Location Id has Na values"
assert (df['Location Id'] != '-99').all(), "Location Id has -99 values"
assert df['Dwelling Type'].notna().all(), "Dwelling Type has Na values"
assert df.duplicated(['Location Id', 'year_quarter', 'Dwelling Type']).sum() == 0, "There are duplicate rows with same year_quarter/Location/Dwelling Type"

print(f'Rows removed due to NA location: {num_before_removena-num_after_removena}')


# Dataset with Dwelling Type Info

df_with_dwelling = df[df['Dwelling Type']!='ALL']

df_with_dwelling.to_csv(
    OUTPUT_WITHDWELLING_FILEPATH,
    index=False
)


# Dataset without Dwelling Type Info

df_without_dwelling = df[df['Dwelling Type']=='ALL']

df_without_dwelling = df_without_dwelling.drop(
    columns=['Dwelling Type']
)

assert not df_without_dwelling.duplicated(
    ["Location Id", "year_quarter"]
).any(), "Duplicate overall records for the same area and quarter"

df_without_dwelling.to_csv(
    OUTPUT_WITHOUT_DWELLING_FILEPATH,
    index=False
)