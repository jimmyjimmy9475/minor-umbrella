## Artificial Intelligence was used to assist with basic setup and coding,
#  however it was NOT used for join decisions and output was inspected for accuracy and correctness.
import sqlite3
import pandas as pd

conn = sqlite3.connect('D5_airbnb.db')
cursor = conn.cursor()

df_airbnb = pd.read_csv('listings_concat_clean.csv')
df_tenancy = pd.read_csv('tenancy_clean.csv')


#Push to SQLite tables
df_airbnb.to_sql('raw_airbnb', conn, if_exists='replace', index=False)
df_tenancy.to_sql('raw_tenancy', conn, if_exists='replace', index=False)
print("Success: SQLite tables created using Cleaned AirBnB and Tenancy Data.")

## SQL Join Query
cursor.execute("DROP TABLE IF EXISTS combined_listings_master;")

sql_join = """
CREATE TABLE combined_listings_master AS
SELECT 
    a.id,
    a.neighbourhood,
    a.month_year,
    a.price AS airbnb_price,
    t.[Median Rent] AS bond_price,
    t.[Active Bonds] AS bond_property_count
FROM raw_airbnb a
LEFT JOIN raw_tenancy t 
    ON a.neighbourhood = t.[Location Id] 
   AND a.month_year = t.TimeFrame;
"""
cursor.execute(sql_join)
print("Success: SQL Left Join completed.")

#Testing
cursor.execute("SELECT * FROM combined_listings_master;")
results = cursor.fetchall()

print("\n--- Aggregated SQL Join Table Output ---")
for row in results:
    print(row)

#Clean up database pipelines
cursor.close()
conn.close()
print("\n Database closed safely.")