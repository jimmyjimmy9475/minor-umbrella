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
This data has been liscensed under a Creative Commons Atribution 3.0 New Zealand License 

Note: Rows are supressed(ommited) when there are less than 5 bonds for a given period

| Column                         | Data Type    | Description                                        |
| ------------------------------ | ------------ | -------------------------------------------------- |
| `TimeFrame`                    | text         | Text data representing the time period (e.g., '2026-Q1'). |
| `Location Id`                  | integer        | Unique identifier code for the location/region. We have assumed -99 is national aggergrate(as this is the case in other tenancy service data) and NA is for tenancies missing data(e.g. were supressed due to having less than 5 bonds) |
| `Dwelling Type`                | text         | Text description outlining the property style (e.g., 'Apartment', 'Boarding House', 'Flat', 'House', 'Room'). ALL is also used as an aggregate |
| `Number Of Beds`               | text         | The number of bedrooms available, kept as text to accommodate categories like '3+'. |
| `Total Bonds`                  | integer      | Number of rental bonds deposited during this period. |
| `Active Bonds`                 | integer      | Number of currently active bonds.   |
| `Closed Bonds`                 | integer      | Number of bonds closed during this period.      |
| `Median Rent`                  | integer        | The middle point value of weekly rent metrics.     |
| `Geometric Mean Rent`          | integer        | The calculated geometric mean of weekly rent values. |
| `Upper Quartile Rent`          | integer        | The 75th percentile benchmark value of weekly rental prices. |
| `Lower Quartile Rent`          | integer        | The 25th percentile benchmark value of weekly rental prices. |
| `Log Std Dev Weekly Rent`      | float        | The logarithmic standard deviation calculation evaluating weekly rent volatility. |

# Data Cleaning

## Cleaning of the listings_concat.csv file:


Bearing in mind that we will be comparing rental prices and number of available properties soon (with the rental tenancy data), it made sense to cull many columns which were not useful for comparison. 

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

As a group, we opted to keep the rows with missing price values, as losing 10667 records out of 28795 would be an incredibly significant loss of data which could be valuable down the line. 

Note: AI was used to help with writing the code for the cleaning process. It was not allowed to make cleaning decisions and all results were checked for accuracy. 

## Cleaning of tenancy data

The date column was replaced with a quarter column.

Original data is not tidy, it contains rows which are aggregates of other rows.
These aggregate rows have been deleted.
- Where location is -99 (national aggregate)
- Where Dwelling Type is ALL
- Where Number Of Beds is *not* ALL (analysis does not require number of beds)

The following columns were dropped as they were deemed to have little relavance to this analysis.
- Geometric Mean Rent
- Total Bonds (not interested in the change in the number of bonds quarter to quarter)
- Closed Bonds (as before)
- Number Of Beds (analysis does not use number of beds, only considering aggregate rows)
- Log Std Dev Weekly Rent (not too helpful for this)

Rows with Location Id = NaN were removed as these did not have price data(median rent etc were also NaN). Unclear what these bonds represent, potentially is an aggregate for those bonds that were supressed due to having less than 5 activie bonds in a location. This removed 15 rows from the filtered dataset.

We checked that there are no duplicated rows.
