import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt

months = {
    "June": "June-2026",
    "May": "May-2026",
    "April": "April-2026",
    "March": "March-2026",
    "Feb": "Feb-2026",
    "Jan": "Jan-2026",
    "Dec": "Dec-2025",
    "Nov": "Nov-2025",
    "Oct": "Oct-2025"
}

dfs = []

for month, month_year in months.items():
    # Read the file
    df = pd.read_csv(f"airbnb_data/listings_{month}.csv")

    # Filter Christchurch City
    df_chch = df[df["neighbourhood_group"] == "Christchurch City"].copy()

    # Add Month-Year column
    df_chch["month_year"] = month_year

    dfs.append(df_chch)

# Combine all months
df_chch_all = pd.concat(dfs, ignore_index=True)

# Check
print(df_chch_all[["month_year", "neighbourhood_group"]].head())
print(df_chch_all.tail())
print(df_chch_all["neighbourhood_group"].unique())

# Print number of missing values in each column
print(df_chch_all.isnull().sum())

# print summary statistics for the selected columns
print(df_chch_all[['price', 'minimum_nights', 'number_of_reviews','availability_365', 'calculated_host_listings_count', 'number_of_reviews_ltm']].describe())

# Save the concatenated AirBnB listings for christchurch from Oct-2025 to June-2026
df_chch_all.to_csv("listings_concat.csv")

# Distribution(histogram) of price (>= 3000)

plt.hist(df_chch_all[df_chch_all['price']<=3000]['price'], bins=80)
plt.title("Distribution Of Price")
plt.show()

# The number of days since last review

     # A publish date column created. 
     # Since some of the values for the number of days since last review were negative(ranging from -13 to -1), the publish datead was justed .

conditions = [df_chch_all["month_year"] == "June-2026", df_chch_all["month_year"] == "May-2026",
df_chch_all["month_year"] =="April-2026",
df_chch_all["month_year"] == "March-2026", df_chch_all["month_year"] == "Feb-2026", 
df_chch_all["month_year"] == "Jan-2026", df_chch_all["month_year"]== "Dec-2025",
df_chch_all["month_year"]== "Nov-2025"]

choice = ["2026-06-22", "2026-06-03", "2026-04-23", "2026-03-23", "2026-02-16", 
"2026-01-24", "2025-12-13", "2025-11-21"]

df_chch_all["publish_date"] = np.select(conditions, choice, default= "2025-10-09")

# last review and publish date columns are converted to datetime data type
df_chch_all["last_review"] = pd.to_datetime(df_chch_all["last_review"])
df_chch_all["publish_date"] = pd.to_datetime(df_chch_all["publish_date"])
df_chch_all.info()

# number of days since last review
df_chch_all["num_days_since_last_review"] = (df_chch_all["publish_date"]-df_chch_all["last_review"]).dt.days

# distribution of the number of days since last review(histogram)
plt.hist(df_chch_all['num_days_since_last_review'], bins = 80)
plt.title("distribution of nimber of days since last review")
plt.show()

# Top 10 percent highest numbers of reviews

review_threshold = df_chch_all["number_of_reviews"].quantile(0.90)
top_10_reviews = df_chch_all[df_chch_all["number_of_reviews"] >= review_threshold ].copy()
top_10_reviews = top_10_reviews.sort_values(by = "number_of_reviews", ascending = False)

print(top_10_reviews[["id", "name", "number_of_reviews", "month_year", "price"]])

print("Top 10 percent highest numbers of reviews", len(top_10_reviews))
