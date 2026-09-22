## Artificial Intelligence was used to assist with basic setup and coding,
#  however it was NOT used for join decisions and output was inspected for accuracy and correctness.
import sqlite3
import pandas as pd

conn = sqlite3.connect('D5_airbnb.db')
cursor = conn.cursor()

df_airbnb = pd.read_csv('listing_concat_clean.csv')
df_tenancy = pd.read_csv('tenancy_clean.csv')


# Using mock data for template/troubleshooting before applying actual dataframes - 
# Following code based on template, needs to be adapted for actual dataframes and column names and join structure.
mock_airbnb = {
    'id': [1, 2],
    'sa2': ['326600', '326600'], # Christchurch Central
    'time_period': ['2026-01', '2026-01'],
    'price': [200, 250],
    'beds': [2, 3]
    }

mock_tenancy = {
    'sa2': ['326600'],
    'time_period': ['2026-01'],
    'price': [150], # Weekly rent index
    'property_count': [45]
}

# Turn the mock data into DataFrames
df_airbnb = pd.DataFrame(mock_airbnb)
df_tenancy = pd.DataFrame(mock_tenancy)

#Push to SQLite tables
df_airbnb.to_sql('raw_airbnb', conn, if_exists='replace', index=False)
df_tenancy.to_sql('raw_tenancy', conn, if_exists='replace', index=False)
print("Success: SQLite tables created using Mock data.")

## SQL Join Query
cursor.execute("DROP TABLE IF EXISTS combined_listings_master;")

sql_join = """
CREATE TABLE combined_listings_master AS
SELECT 
    a.id,
    a.sa2,
    a.time_period,
    a.price AS airbnb_price,
    a.beds,
    t.price AS bond_price,
    t.property_count AS bond_property_count
FROM raw_airbnb a
LEFT JOIN raw_tenancy t 
    ON a.sa2 = t.sa2 
   AND a.time_period = t.time_period;
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