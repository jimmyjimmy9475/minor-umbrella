## Artificial Intelligence was used to assist with basic setup and coding,
#  however it was NOT used for join decisions and output was inspected for accuracy and correctness.
import sqlite3
import pandas as pd

conn = sqlite3.connect('D5_airbnb.db')
cursor = conn.cursor()

df_airbnb = pd.read_csv('listings_SA2.csv')
df_tenancy = pd.read_csv('tenancy_clean_without_dwelling.csv')
df_joined = pd.read_csv('listings_tenancy_joined.csv')



#Push to SQLite tables
df_airbnb.to_sql('raw_airbnb', conn, if_exists='replace', index=False)
df_tenancy.to_sql('raw_tenancy', conn, if_exists='replace', index=False)
df_joined.to_sql('joined', conn, if_exists='replace', index=False)
print("Success: SQLite tables created using Cleaned AirBnB and Tenancy Data.")

cursor.close()
conn.close()
print("\n Database closed safely.")