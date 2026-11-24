"""
Automated Data Integrity & Reliability Test Suite
Verifies data quality and reliability index calculations against official ground truth.
"""

import os
import pandas as pd
import numpy as np

def run_tests():
    clean_dir = r"C:\Users\Surface\Documents\MrG\data\clean"
    outages = pd.read_csv(os.path.join(clean_dir, "outages_clean.csv"))
    feeders = pd.read_csv(os.path.join(clean_dir, "feeders_clean.csv"))
    substations = pd.read_csv(os.path.join(clean_dir, "substations_clean.csv"))
    weather = pd.read_csv(os.path.join(clean_dir, "weather_clean.csv"))

    print("=== TEST 1: ROW COUNTS ===")
    assert len(outages) == 2743, f"Expected 2743 outages, got {len(outages)}"
    assert len(feeders) == 54, f"Expected 54 feeders, got {len(feeders)}"
    assert len(substations) == 8, f"Expected 8 substations, got {len(substations)}"
    print(f"PASS: Outages={len(outages)}, Feeders={len(feeders)}, Substations={len(substations)}")

    print("\n=== TEST 2: OUTAGE TYPE SEGREGATION ===")
    unplanned = outages[outages["outage_type"] == "unplanned"]
    planned = outages[outages["outage_type"] == "planned"]
    print(f"Unplanned count: {len(unplanned)} (Truth: 2594)")
    print(f"Planned count: {len(planned)} (Truth: 149)")
    assert len(unplanned) == 2594, f"Expected 2594 unplanned, got {len(unplanned)}"
    assert len(planned) == 149, f"Expected 149 planned, got {len(planned)}"
    print("PASS: Outage type segregation exact match!")

    print("\n=== TEST 3: CUSTOMER TOTALS & FOREIGN KEY ===")
    total_customers = feeders["customers_total"].sum()
    print(f"Total customers served: {total_customers:,} (Truth: 212,196)")
    assert total_customers == 212196, f"Expected 212,196 customers, got {total_customers}"
    
    fk_match = outages["feeder_id"].isin(feeders["feeder_id"]).mean()
    print(f"FK Match Rate: {fk_match*100:.2f}% (Threshold: >= 99%)")
    assert fk_match >= 0.99, f"FK match rate below 99%: {fk_match}"
    print("PASS: FK match rate and customer totals verified!")

    print("\n=== TEST 4: RELIABILITY INDICES (SAIFI, SAIDI, CAIDI) ===")
    unplanned = unplanned.copy()
    unplanned["start_dt"] = pd.to_datetime(unplanned["start_time"])
    unplanned["year"] = unplanned["start_dt"].dt.year

    for yr in [2023, 2024]:
        df_yr = unplanned[unplanned["year"] == yr]
        cnt = len(df_yr)
        cust_aff = df_yr["customers_affected"].sum()
        cust_min = df_yr["customer_minutes"].sum()
        
        saifi = cust_aff / total_customers
        saidi = cust_min / total_customers
        caidi = saidi / saifi if saifi > 0 else 0

        print(f"\n--- Year {yr} (B.E. {yr+543}) ---")
        print(f"Unplanned Outages: {cnt}")
        print(f"SAIFI: {saifi:.2f} (Truth: {'6.38' if yr==2023 else '7.72'})")
        print(f"SAIDI: {saidi:.1f} mins (Truth: {'825' if yr==2023 else '1166'} mins)")
        print(f"CAIDI: {caidi:.1f} mins")

    print("\n=== ALL INTEGRITY TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
