## Artificial Intelligence was used to assist with basic setup and coding,
#  however it was NOT used for join decisions and output was inspected for accuracy and correctness.
import sqlite3
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

db_filepath = ROOT / 'output' / 'joined.db'
listings_filepath = ROOT / 'output' / 'csv' / 'Step4_listings_with_SA2.csv'
tenancy_filepath = ROOT / 'output' / 'csv' / 'Step3_cleaning_tenancy_data_without_dwelling.csv'
joinned_filepath = ROOT / 'output' / 'csv' / 'Step5_joined_listings_tenancy.csv'

conn = sqlite3.connect(db_filepath)
cursor = conn.cursor()

df_airbnb = pd.read_csv(listings_filepath)
df_tenancy = pd.read_csv(tenancy_filepath)
df_joined = pd.read_csv(joinned_filepath)

#Push to SQLite tables
df_airbnb.to_sql('raw_airbnb', conn, if_exists='replace', index=False)
df_tenancy.to_sql('raw_tenancy', conn, if_exists='replace', index=False)
df_joined.to_sql('joined', conn, if_exists='replace', index=False)
print("Success: SQLite tables created using Cleaned AirBnB and Tenancy Data.")

cursor.close()
conn.close()
