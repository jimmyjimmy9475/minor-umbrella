"""
Run the complete Airbnb and tenancy data processing pipeline.
"""

import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent


PIPELINE_STEPS = [
    "Step1_aggregate_listings.py",
    "Step2_cleaned_listings.py",
    "Step3_cleaning_tenancy_data.py",
    "Step4_listings_with_SA2.py",
    "Step4b_listings_with_SA2_fill_missing.py",
    "Step5_joined_listings_tenancy.py",
    "Step6_SQL.py",
    "Step7_airbnb_rental_analysis.py",
]


def run_step(script):
    """Run one pipeline step and stop if it fails."""

    script_path = ROOT / script

    print("\n" + "=" * 70)
    print(f"RUNNING: {script}")
    print("=" * 70)

    start_time = time.perf_counter()

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
    )

    elapsed = time.perf_counter() - start_time

    if result.returncode != 0:
        print(f"\nFAILED: {script}")
        print(f"Time: {elapsed:.2f} seconds")
        sys.exit(result.returncode)

    print(f"\nCOMPLETED: {script}")
    print(f"Time: {elapsed:.2f} seconds")


def main():
    total_start = time.perf_counter()

    print("=" * 70)
    print("AIRBNB + TENANCY DATA PIPELINE")
    print("=" * 70)

    for script in PIPELINE_STEPS:
        run_step(script)

    total_elapsed = time.perf_counter() - total_start

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Total time: {total_elapsed:.2f} seconds")


if __name__ == "__main__":
    main()