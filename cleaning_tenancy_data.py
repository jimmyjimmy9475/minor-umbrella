import pandas as pd

# treat location as string to handle "NULL"
data_types = {
    'Location Id': str,
    'Active Bonds':'Int64',
    'Median Rent':'Int64',
    'Upper Quartile Rent':'Int64',
    'Lower Quartile Rent':'Int64',
}

df = pd.read_csv("tenancy_data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv", dtype=data_types)

# remove national aggregate of bonds
df = df[df['Location Id']!='-99']

# remove aggregation of dwelling types
df = df[df['Dwelling Type']!='ALL']

# only include aggregated number of beds
df = df[df['Number Of Beds']=='ALL']

cols_to_remove = [
    'Number Of Beds',
    'Total Bonds',
    'Closed Bonds',
    'Geometric Mean Rent',
    'Log Std Dev Weekly Rent'
]
df = df.drop(
    columns=cols_to_remove
)

num_before = len(df['Location Id'])
df = df[df['Location Id'].notna()] # remove na
df['Location Id'] = df['Location Id'].astype('int64') # convert to int
num_after = len(df['Location Id'])

assert df['TimeFrame'].notna().all(), "TimeFrame has Na values"
assert df['Location Id'].notna().all(), "Location Id has Na values"
assert df['Dwelling Type'].notna().all(), "Dwelling Type has Na values"

print(f'Rows removed due to NA location: {num_before-num_after}')
print(df)

df.to_csv(
    "tenancy_clean.csv",
    index=False
)