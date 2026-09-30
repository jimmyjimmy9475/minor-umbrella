"""
Get the SA2_2019 region for each airbnb using the stats nz api
"""

import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
load_dotenv()

API_KEY = os.getenv("API_KEY")
LAYER = "98970"

URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json"

LISTINGS_NO_SA2_FILEPATH = ROOT / 'output' / 'csv' / 'Step2_cleaned_listings.csv'
LISTINGS_WITH_SA2_FILEPATH = ROOT / 'output' / 'csv' / 'Step4_listings_with_SA2.csv'

def get_sa2(lon, lat):
    if pd.isna(lon) or pd.isna(lat):
        return pd.Series({
            "sa2_code": None,
            "sa2_name": None
        })

    params = {
        "key": API_KEY,
        "layer": LAYER,
        "x": lon,
        "y": lat,
    }

    try:
        r = requests.get(URL, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        features = data.get("vectorQuery", {}).get("layers",{}).get(LAYER,{}).get("features", [])
       
        if not features:
            return

        assert len(features) == 1, "There is more than one feature returned by the api"
        feature = features[0]

        properties = feature.get("properties", feature)

        return properties.get('SA22019_V1_00')

    except (requests.RequestException, ValueError, KeyError) as e:
        print(e)
        return
    
def freshRun():
    df = pd.read_csv(LISTINGS_NO_SA2_FILEPATH, dtype={"price" : "Int64"})

    coordinates = (
        df[["longitude", "latitude"]]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    )

    coordinates = list(coordinates)

    results = concurrentSA2(coordinates)

    
    df["sa2"] = [
        results.get((lon, lat))
        for lon, lat in zip(df["longitude"], df["latitude"])
    ]

    df.to_csv(LISTINGS_WITH_SA2_FILEPATH, index=False)

    print(f"Saved to {LISTINGS_WITH_SA2_FILEPATH}")
    print(df[["row_number","sa2"]].head())

def fill_missing_sa2():
    df = pd.read_csv(LISTINGS_WITH_SA2_FILEPATH, dtype={"sa2": str, "price" : "Int64"})

    missing_mask = df["sa2"].isna() | (df["sa2"].astype(str).str.strip() == "")

    missing_df = df.loc[missing_mask, ["longitude", "latitude"]].dropna().drop_duplicates()

    print(f"Rows missing SA2: {missing_mask.sum():,}")
    print(f"Unique coordinates to query: {len(missing_df):,}")

    if missing_df.empty:
        print("No missing SA2 values to fill.")
        return df

    coordinates = list(
        missing_df.itertuples(index=False, name=None)
    )

    results = concurrentSA2(coordinates)

    for (lon, lat), sa2 in results.items():
        mask = (
            missing_mask
            & df["longitude"].eq(lon)
            & df["latitude"].eq(lat)
        )

        df.loc[mask, "sa2"] = sa2

    print(
        f"SA2 values filled: "
        f"{df.loc[missing_mask, 'sa2'].notna().sum():,}"
    )

    df.to_csv(LISTINGS_WITH_SA2_FILEPATH, index=False)
    
    print(f"Saved to {LISTINGS_WITH_SA2_FILEPATH}")

def concurrentSA2(coordinates):

    results = {}

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = {
            executor.submit(get_sa2, lon, lat): (lon, lat)
            for lon, lat in coordinates
        }

        for i, future in enumerate(as_completed(futures), start=1):

            lon, lat = futures[future]

            try:
                results[(lon, lat)] = future.result()
            except Exception as e:
                print(f"Failed ({lon}, {lat}): {e}")
                results[(lon, lat)] = None

            if i % 100 == 0:
                print(f"Completed {i:,} / {len(futures):,}")

    return results

if __name__ == "__main__":
    freshRun()
