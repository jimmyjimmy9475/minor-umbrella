# Design principles

This document was created using Github CoPilot

This document describes the design of the Airbnb and tenancy-data pipeline. The
pipeline is intended to produce a reproducible comparison of short-term Airbnb
prices and long-term rental indicators for Christchurch City, using SA2 regions
and comparable time periods as the common structure.

## 1. Pipeline inputs

All input paths are relative to the repository root and are read from the
`data/` directory. The source data is kept separate from generated files and is
not modified by the pipeline.

### Airbnb listings

The `data/airbnb_data/` directory contains monthly Airbnb listing CSV files from
October 2025 to June 2026. These files provide listing identifiers, coordinates,
room types, prices, availability, review information, and neighbourhood
information. Step 1 uses the neighbourhood group to select Christchurch City
listings and adds a month-year label to each record.

### Tenancy data

The file
`data/tenancy_data/Detailed-Quarterly-Tenancy-Q1-2020-Q3-2026.csv` contains
quarterly rental-bond and rent statistics, including location IDs, dwelling
types, active bonds, and rent measures. The pipeline uses the records that
overlap the Airbnb period, excludes national aggregates and bedroom-level
breakdowns, and retains the aggregate and dwelling-level forms as separate
cleaned outputs.

### Geographic data and external lookup

The file `data/stat_area_data/geographic-areas-table-2023.csv` provides SA2
geographic names and territorial-authority information for the analysis stage.
Step 4 also uses the Stats NZ Datafinder API to map each listing's longitude and
latitude to an SA2 region. The API key is supplied through the `API_KEY`
environment variable rather than being written into source code.

## 2. Pipeline outputs

Generated tabular outputs are written to `output/csv/`:

- `Step1_aggregate_listings.csv`: Christchurch Airbnb listings concatenated
  across the monthly source files.
- `Step2_cleaned_listings.csv`: listings with columns not needed for the
  comparison removed and a stable row number added.
- `Step3_cleaning_tenancy_data_with_dwelling.csv`: cleaned tenancy records
  retaining dwelling type.
- `Step3_cleaning_tenancy_data_without_dwelling.csv`: cleaned aggregate tenancy
  records without dwelling type, used for the main join.
- `Step4_listings_with_SA2.csv`: Airbnb listings enriched with an SA2 code.
- `Step5_joined_listings_tenancy.csv`: one record per SA2 and quarter containing
  Airbnb median price, Airbnb listing count, tenancy median weekly rent, and
  active tenancy bonds.

The pipeline also produces:

- `output/joined.db`: a SQLite database containing `raw_airbnb`, `raw_tenancy`,
  and `joined` tables.
- `output/image/airbnb_vs_rental_price.png`: a plot comparing Airbnb and
  long-term rental property counts for Christchurch SA2 regions.
- Console summaries and checks, including missing-value counts, descriptive
  statistics, and price-gap summaries.

## 3. Main pipeline steps

The scripts are numbered to make their intended execution order explicit.

1. **Aggregate Airbnb listings** (`Step1_aggregate_listings.py`). Read each
   monthly listing file, filter to Christchurch City, add the observation
   month, concatenate the records, convert price to a numeric nullable type,
   and save the combined data.
2. **Clean listings** (`Step2_cleaned_listings.py`). Remove listing and review
   fields that are not required for the rental comparison, reset the index, and
   save the analysis-ready Airbnb records.
3. **Clean tenancy data** (`Step3_cleaning_tenancy_data.py`). Convert dates to
   quarters, restrict the time range, remove aggregate and unnecessary fields,
   remove missing location IDs, validate uniqueness, and write both dwelling
   and non-dwelling versions.
4. **Add SA2 regions** (`Step4_listings_with_SA2.py`). Query Stats NZ for the
   SA2 associated with each unique coordinate. The separate
   `Step4b_listings_with_SA2_fill_missing.py` script retries missing mappings.
5. **Join the datasets** (`Step5_joined_listings_tenancy.py`). Convert Airbnb
   month-year values to quarters, aggregate listings by SA2 and quarter, and
   left-join them to tenancy statistics using SA2 and quarter as keys.
6. **Create a database copy** (`Step6_SQL.py`). Load the cleaned Airbnb,
   tenancy, and joined CSV files into SQLite tables for query-based analysis.
7. **Analyse the joined data** (`Step7_airbnb_rental_analysis.py`). Restrict
   records to Christchurch geographic areas, convert weekly rent to a nightly
   measure, calculate price gaps, compare property counts, and save a plot.

## 4. Coding and software strategies

### Separation of concerns

The repository separates `data/`, `code/`, and `output/`. Each numbered script
has one main pipeline responsibility and communicates with the next stage
through named files. This makes intermediate results inspectable and allows a
stage to be rerun without rewriting the source data.

### Reproducible and portable file handling

Scripts derive the repository root from `Path(__file__)` and build paths with
`pathlib`, rather than depending on the user's current working directory.
Input and output paths are declared near the top of each script. The numbered
filenames document the required order of execution and make the workflow easy
to follow.

### Explicit data preparation and validation

Pandas dtypes are specified for identifiers, integer measures, and nullable
values where appropriate. Dates are converted before time filtering and
quarter matching. Assertions and merge validation check assumptions such as
valid locations, non-duplicated tenancy keys, and one-to-one joined records.
These checks fail early when an upstream file or assumption changes.

### Preserve useful missing data

Missing Airbnb prices are retained during cleaning because removing them would
discard a substantial part of the source data. They are excluded only from
calculations that require a price. This separates data preservation from
analysis-specific filtering and keeps later analyses possible.

### Efficient and responsible external access

SA2 requests are made once per unique coordinate and executed concurrently with
a bounded thread pool. Requests use a timeout and handle request or response
errors. The API credential is read from an environment variable, keeping
secrets out of the repository.

### Lecture-aligned best practices

The project adopts the coding practices recorded in `better_coding_practices.md`:

- use clear filenames and numbered scripts that communicate purpose and order;
- keep code, input data, and generated output in separate directories;
- use relative, repository-based paths for portability;
- place a brief description at the top of each script;
- use comments to divide major processing sections;
- remove unused files and keep the repository focused; and
- add assertions to document and test important assumptions.

Together these practices improve readability, reproducibility, maintainability,
and the ability to detect incorrect data early.