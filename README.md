# minor-umbrella

# Data Sources

## Airbnb listings.csv
June 2026 - New Zealand - Source https://docs.google.com/spreadsheets/d/1iWCNJcSutYqpULSQHlNyGInUvHg2BoUGoNRIGa6Szc4/edit

The data set is licenced under the Creative Commons Attribution 4.0 International License.

| Column                           | Data Type | Description                                                                  |
| -------------------------------- | --------- | ---------------------------------------------------------------------------- |
| `id`                             | integer   | Airbnb's unique identifier for the listing                                   |
| `name`                           | string    | Display name of the listing                                                  |
| `host_id`                        | integer   | Airbnb's unique identifier for the host                                      |
| `host_name`                      | string    | Display name of the host                                                     |
| `neighbourhood_group`            | string    | Geocoded from latitude/longitude against public neighbourhood shape files    |
| `neighbourhood`                  | string    | Geocoded from latitude/longitude against public neighbourhood shape files    |
| `latitude`                       | float     | Uses the World Geodetic System (WGS84) projection for latitude and longitude |
| `longitude`                      | float     | Uses the World Geodetic System (WGS84) projection for latitude and longitude |
| `room_type`                      | string    | Room type (e.g., private room or entire home/house)                          |
| `price`                          | currency  | Price in the local currency (sometimes `$` is used incorrectly)              |
| `minimum_nights`                 | integer   | Minimum length of booking                                                    |
| `number_of_reviews`              | integer   | Total number of reviews the listing has received                             |
| `last_review`                    | date      | Date of the most recent review                                               |
| `reviews_per_month`              | float     | Average number of reviews per month over the listing's lifetime              |
| `calculated_host_listings_count` | integer   | Number of listings the host has in the region (NZ)                           |
| `availability_365`               | integer   | Number of bookable days within the next 365 days                             |
| `number_of_reviews_ltm`          | integer   | Number of reviews received in the last 12 months                             |
| `license`                        | string    | Licence, permit, or registration number                                      |


## Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv
Jan 2020 to Apr 2026 New Zealand 
Source: https://www.tenancy.govt.nz/about-tenancy-services/data-and-statistics/rental-bond-data/ 
Data Dictionary: https://docs.google.com/spreadsheets/d/1XxwMOPaXOkFAlvyJCgIcOEooDJwpzXOvV6BusqdjTEk/edit?gid=360684855#gid=360684855 
## Data dictionary doc under progress

This data has been liscensed under a Creative Commons Atribution 3.0 New Zealand License 
| Column                         | Data Type    | Description                                        |
| ------------------------------ | ------------ | -------------------------------------------------- |
| `TimeFrame`                    | text         | Text data representing the time period (e.g., '2026-Q1'). |
| `Location Id`                  | bigint       | Unique identifier code for the location/region.    |
| `Dwelling Type`                | text         | Text description outlining the property style (e.g., House, Apartment). |
| `Number Of Beds`               | text         | The number of bedrooms available, kept as text to accommodate categories like '3+'. |
| `Total Bonds`                  | integer      | Total cumulative number of rental bonds deposited. |
| `Active Bonds`                 | integer      | Number of currently active or open rental bonds.   |
| `Closed Bonds`                 | integer      | Number of resolved or finalized rental bonds.      |
| `Median Rent`                  | numeric      | The middle point value of weekly rent metrics.     |
| `Geometric Mean Rent`          | numeric      | The calculated geometric mean of historical weekly rent values. |
| `Upper Quartile Rent`          | numeric      | The 75th percentile benchmark value of weekly rental prices. |
| `Lower Quartile Rent`          | numeric      | The 25th percentile benchmark value of weekly rental prices. |
| `Log Std Dev Weekly Rent`      | numeric      | The logarithmic standard deviation calculation evaluating weekly rent volatility. |



Cleaning of the listings_concat.csv file:


Bearing in mind that we will be comparing rental prices and number of available properties soon (with the rental tenancy data), it made sense
to cull many columns which were not useful for comparison. 

The following columns were removed: 

name
host_id
host_name
neighbourhood_group
reviews_per_month
calculated_host_listings_count
license
number_of_reviews
last_review
number_of_reviews_ltm
minimum_nights


Additional formatting was undertaken to have latitude and longitude to a consistent number of decimal places, 1. 

As a group, we opted to keep the rows with missing price values, as losing 10667 records out of 28795 would be an incredibly significant loss
of data which could be valuable down the line. 

Note: AI was used in the process of cleaning the data. 