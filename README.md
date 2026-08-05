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
