import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
LAYER = "98970"

URL = "https://datafinder.stats.govt.nz/services/query/v1/vector.json"

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

        feature = features[0]

        properties = feature.get("properties", feature)

        return properties.get('SA22019_V1_00')

    except (requests.RequestException, ValueError, KeyError) as e:
        print(e)
        return
    
def freshRun():
    df = pd.read_csv("listings_concat_clean.csv", dtype={"price" : "Int64"})

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

    df.to_csv("listings_SA2.csv", index=False)

    print("Saved to listings_SA2.csv")

def fill_missing_sa2():
    df = pd.read_csv("listings_SA2.csv", dtype={"sa2": str, "price" : "Int64"})

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

    df.to_csv("listings_SA2.csv", index=False)
    
    print("Saved to listings_SA2.csv")

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