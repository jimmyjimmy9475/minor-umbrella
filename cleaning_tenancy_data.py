import pandas as pd

input_filepath = "tenancy_data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv"
output_withdwelling_filepath = "tenancy_clean_with_dwelling.csv"
output_withoutdwelling_filepath = "tenancy_clean_without_dwelling.csv"
stat_area_filepath = "stat_area_data/geographic-areas-table-2023.csv"

# treat location as string
data_types = {
    'Location Id': str,
    'Active Bonds':'Int64',
    'Median Rent':'Int64',
    'Upper Quartile Rent':'Int64',
    'Lower Quartile Rent':'Int64',
}

df = pd.read_csv(input_filepath, dtype=data_types)

assert df['TimeFrame'].notna().all(), "TimeFrame has Na values"
# Convert the "TimeFrame" column to datetime data type
df["TimeFrame"] = pd.to_datetime(df["TimeFrame"])

# Filter the dataset to dates after 1 October 2025
df = df[df["TimeFrame"] >= "2025-10-01"]

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

stat_areas = pd.read_csv(stat_area_filepath)

# Check some assumptions
assert df['year_quarter'].notna().all(), "year_quarter has Na values"
assert df['Location Id'].notna().all(), "Location Id has Na values"
assert (df['Location Id'] != '-99').all(), "Location Id has -99 values"
assert df['Dwelling Type'].notna().all(), "Dwelling Type has Na values"
assert df.duplicated(['Location Id', 'year_quarter', 'Dwelling Type']).sum() == 0, "There are duplicate rows with same year_quarter/Location/Dwelling Type"

print(f'Rows removed due to NA location: {num_before_removena-num_after_removena}')
print(df)

# Dataset with Dwelling Type Info

df_with_dwelling = df[df['Dwelling Type']!='ALL']

df_with_dwelling.to_csv(
    output_withdwelling_filepath,
    index=False
)


# # Dataset without Dwelling Type Info

# df_without_dwelling = df[df['Dwelling Type']!='ALL']

# df = df.drop(
#     columns=['Dwelling Type']
# )

# df_without_dwelling.to_csv(
#     output_withoutdwelling_filepath,
#     index=False
# )

df_without_dwelling = df.loc[
    df["Dwelling Type"] == "ALL"
].drop(columns=["Dwelling Type"]).copy()

assert not df_without_dwelling.duplicated(
    ["Location Id", "year_quarter"]
).any(), "Duplicate overall records for the same area and quarter"

df_without_dwelling.to_csv(
    output_withoutdwelling_filepath,
    index=False
)