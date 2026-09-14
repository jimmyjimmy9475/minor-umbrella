import os

import pandas as pd
df = pd.read_csv(r"C:\Users\muzam\OneDrive - University of Canterbury\DATA201\Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv")
data_dict = pd.DataFrame({"Columns": df.columns, "Data Type": df.dtypes.astype(str)})

data_dict.to_csv("data_dictionary.csv", index=False)

# Define your schema fields: (Field Name, Data Type, Description)
schema_data = [
    ("TimeFrame", "text", "Text data representing the time period (e.g., '2026-Q1')."),
    ("Location Id", "float", "Unique identifier code for the location/region."),
    ("Dwelling Type", "text", "Text description outlining the property style (e.g., House, Apartment)."),
    ("Number Of Beds", "text", "The number of bedrooms available, kept as text to accommodate categories like '3+'."),
    ("Total Bonds", "integer", "Total cumulative number of rental bonds deposited."),
    ("Active Bonds", "integer", "Number of currently active or open rental bonds."),
    ("Closed Bonds", "integer", "Number of resolved or finalized rental bonds."),
    ("Median Rent", "float", "The middle point value of weekly rent metrics."),
    ("Geometric Mean Rent", "float", "The calculated geometric mean of historical weekly rent values."),
    ("Upper Quartile Rent", "float", "The 75th percentile benchmark value of weekly rental prices."),
    ("Lower Quartile Rent", "float", "The 25th percentile benchmark value of weekly rental prices."),
    ("Log Std Dev Weekly Rent", "float", "The logarithmic standard deviation calculation evaluating weekly rent volatility.")
]

# Print the top headers matching your style
print(f"| {'Column':<30} | {'Data Type':<12} | {'Description':<50} |")
print(f"| {'-'*30} | {'-'*12} | {'-'*50} |")

# Print the rows automatically formatted with padding spacer alignments
for col_name, data_type, desc in schema_data:
    # `host_id` styling wrap style (enclosing backticks if desired)
    formatted_name = f"`{col_name}`"
    print(f"| {formatted_name:<30} | {data_type:<12} | {desc:<50} |")