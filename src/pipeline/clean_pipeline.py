"""
Clean Data Pipeline
Cleans and standardizes all 4 competition datasets:
1. outages_raw.csv -> data/clean/outages_clean.csv & .parquet
2. feeders.xlsx    -> data/clean/feeders_clean.csv & .parquet
3. substations.json-> data/clean/substations_clean.csv & .parquet
4. weather_daily.csv-> data/clean/weather_clean.csv & .parquet
Also creates sample data under data/sample/
"""

import json
import os
import re
import numpy as np
import pandas as pd

def run_pipeline(raw_dir: str, clean_dir: str, sample_dir: str):
    os.makedirs(clean_dir, exist_ok=True)
    os.makedirs(sample_dir, exist_ok=True)
    
    # ----------------------------------------------------
    # 1. CLEAN FEEDERS
    # ----------------------------------------------------
    print("--- 1. Cleaning Feeders ---")
    f_raw = pd.read_excel(os.path.join(raw_dir, "feeders.xlsx"), sheet_name="feeders")
    f = f_raw.copy()
    f.columns = [
        "feeder_id", "substation_id", "area_type", "length_km",
        "customers_total", "tree_cover", "overhead_pct", "install_year"
    ]
    
    # Drop exact duplicate rows (e.g. CMI-F18)
    f = f.drop_duplicates(subset=["feeder_id"], keep="first").reset_index(drop=True)
    
    # Standardize area_type
    area_map = {
        "เมือง": "urban", "urban": "urban", "urban ": "urban",
        "ชานเมือง": "suburban", "suburban": "suburban",
        "ชนบท": "rural", "rural": "rural", "RURAL": "rural"
    }
    f["area_type"] = f["area_type"].astype(str).str.strip().map(area_map).fillna(f["area_type"])
    
    # Standardize length: if > 1000, it's entered in metres, divide by 1000
    f["length_km"] = f["length_km"].astype(float)
    f.loc[f["length_km"] > 1000, "length_km"] /= 1000.0
    f["length_km"] = f["length_km"].round(2)
    
    # Tree cover and overhead %
    f["tree_cover"] = f["tree_cover"].astype(str).str.strip().str.lower()
    f["overhead_pct"] = pd.to_numeric(f["overhead_pct"], errors="coerce").round(1)
    f["install_year"] = pd.to_numeric(f["install_year"], errors="coerce").astype(int)
    
    # Impute missing customers for CMI-F02 and LPG-F12 (known missing in GIS export)
    known_customers = {"CMI-F02": 5321, "LPG-F12": 2260}
    for fid, cval in known_customers.items():
        f.loc[f["feeder_id"] == fid, "customers_total"] = cval
    area_cust_medians = f.groupby("area_type")["customers_total"].transform("median").round()
    f["customers_total"] = f["customers_total"].fillna(area_cust_medians).astype(int)
    
    valid_feeders = set(f["feeder_id"])
    print(f"Feeders cleaned: {len(f)} rows (expected 54)")

    # ----------------------------------------------------
    # 2. CLEAN SUBSTATIONS
    # ----------------------------------------------------
    print("--- 2. Cleaning Substations ---")
    with open(os.path.join(raw_dir, "substations.json"), "r", encoding="utf-8") as file:
        subs_raw = json.load(file)
    
    subs_rows = []
    for s in subs_raw:
        # capacity_mva might be "75 MVA" string or int
        cap = s.get("capacity_mva")
        if isinstance(cap, str):
            cap = int(re.sub(r"[^\d]", "", cap))
        
        loc = s.get("location", {})
        subs_rows.append({
            "substation_id": s.get("substation_id"),
            "substation_name": s.get("substation_name"),
            "capacity_mva": cap,
            "commissioned_year": s.get("commissioned_year"),
            "province": loc.get("province"),
            "region": loc.get("region")
        })
    df_subs = pd.DataFrame(subs_rows)
    print(f"Substations cleaned: {len(df_subs)} rows (expected 8)")

    # ----------------------------------------------------
    # 3. CLEAN WEATHER
    # ----------------------------------------------------
    print("--- 3. Cleaning Weather ---")
    w = pd.read_csv(os.path.join(raw_dir, "weather_daily.csv"))
    
    # Date formatting
    w["date"] = pd.to_datetime(w["date"]).dt.strftime("%Y-%m-%d")
    
    # Convert Fahrenheit to Celsius: Lamphun sensor recorded °F in Jun-Jul 2023 (> 50°C)
    f_mask = (w["province"] == "ลำพูน") & (w["max_temp_c"] > 50)
    w.loc[f_mask, "max_temp_c"] = ((w.loc[f_mask, "max_temp_c"] - 32) * 5 / 9).round(1)
    
    # Sentinel -999 in rainfall_mm -> replace with NaN or 0.0
    w.loc[w["rainfall_mm"] == -999, "rainfall_mm"] = np.nan
    # Impute missing rainfall with 0.0 (or provincial median for rainy days)
    w["rainfall_mm"] = w["rainfall_mm"].fillna(0.0).round(1)
    
    w["max_wind_kmh"] = pd.to_numeric(w["max_wind_kmh"], errors="coerce").round(1)
    w["thunderstorm"] = w["thunderstorm"].astype(bool)
    print(f"Weather cleaned: {len(w)} rows")

    # ----------------------------------------------------
    # 4. CLEAN OUTAGES
    # ----------------------------------------------------
    print("--- 4. Cleaning Outages ---")
    o = pd.read_csv(os.path.join(raw_dir, "outages_raw.csv"), dtype=str, keep_default_na=False, na_values=[""])
    
    # Step 4.1: Drop exact duplicates
    o = o.drop_duplicates().reset_index(drop=True)
    
    # Step 4.2: Normalize feeder_id format (e.g. CMI-F07)
    def norm_feeder(s):
        s = str(s).strip().upper()
        m = re.match(r"^([A-Z]{3})-?F(\d+)$", s)
        return f"{m.group(1)}-F{int(m.group(2)):02d}" if m else s
    o["feeder_id"] = o["feeder_id"].map(norm_feeder)
    
    # Step 4.3: Parse timestamps (handle Buddhist era dd/mm/YYYY+543 and ISO formats)
    def parse_time(s):
        if pd.isna(s) or s is None or str(s).strip() == "":
            return pd.NaT
        s_str = str(s).strip()
        m_be = re.match(r"^(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})$", s_str)
        if m_be:
            d, mo, y, h, mi = map(int, m_be.groups())
            # Convert Buddhist Era to CE
            year_ce = y - 543 if y > 2400 else y
            return pd.Timestamp(year_ce, mo, d, h, mi)
        # Parse ISO format (handling T and timezone offsets)
        clean_s = s_str[:19].replace("T", " ")
        return pd.to_datetime(clean_s, errors="coerce")
    
    o["start_time_dt"] = o["start_time"].map(parse_time)
    o["end_time_dt"] = o["end_time"].map(parse_time)

    # Step 4.3.1: Fix typo years (2014, 2042, 2204) using outage_id or end_time
    def fix_year(row, col):
        ts = row[col]
        if pd.isna(ts):
            return ts
        if ts.year not in [2023, 2024]:
            m = re.search(r"OUT-(\d{4})-", str(row["outage_id"]))
            if m:
                return ts.replace(year=int(m.group(1)))
            other = row["end_time_dt"] if col == "start_time_dt" else row["start_time_dt"]
            if pd.notna(other) and other.year in [2023, 2024]:
                return ts.replace(year=other.year)
        return ts

    o["start_time_dt"] = o.apply(lambda r: fix_year(r, "start_time_dt"), axis=1)
    o["end_time_dt"] = o.apply(lambda r: fix_year(r, "end_time_dt"), axis=1)
    
    # Step 4.4: Swap timestamps if end < start
    swapped = (o["end_time_dt"] < o["start_time_dt"]) & o["end_time_dt"].notna() & o["start_time_dt"].notna()
    o.loc[swapped, ["start_time_dt", "end_time_dt"]] = o.loc[swapped, ["end_time_dt", "start_time_dt"]].values
    
    # Step 4.5: Calculate & reconcile duration_min
    calc_dur = (o["end_time_dt"] - o["start_time_dt"]).dt.total_seconds() / 60.0
    dur_raw = pd.to_numeric(o["duration_min"], errors="coerce").abs()
    
    # Detect placeholder (9999, 14400)
    placeholder = dur_raw >= 9999
    # Detect entered in hours
    in_hours = (dur_raw.notna()) & (calc_dur.notna()) & ((dur_raw * 60 - calc_dur).abs() <= 1) & (calc_dur > 0) & (dur_raw < calc_dur - 1)
    
    # Standardize duration
    o["duration_min_clean"] = np.where(calc_dur.notna(), calc_dur.round(), np.where(placeholder, np.nan, dur_raw))
    
    # If end_time was missing, estimate it from start_time + duration
    need_end = o["end_time_dt"].isna() & o["start_time_dt"].notna() & o["duration_min_clean"].notna()
    o.loc[need_end, "end_time_dt"] = o.loc[need_end, "start_time_dt"] + pd.to_timedelta(o.loc[need_end, "duration_min_clean"], unit="m")
    
    # Step 4.6: Customers Affected
    cust_str = o["customers_affected"].astype(str).str.replace(",", "").str.strip()
    cust_num = pd.to_numeric(cust_str, errors="coerce")
    
    # Merge feeder customer total for validation & imputation
    o = o.merge(f[["feeder_id", "customers_total", "area_type"]], on="feeder_id", how="left")
    
    # If customer exceeds feeder total, cap at total
    o["customers_affected_clean"] = np.where(
        (cust_num.notna()) & (o["customers_total"].notna()) & (cust_num > o["customers_total"]),
        o["customers_total"],
        cust_num
    )
    # If missing, impute with 30% of feeder customer total or median
    default_cust = (o["customers_total"] * 0.35).round().fillna(500)
    o["customers_affected_clean"] = o["customers_affected_clean"].fillna(default_cust).astype(int)
    
    # Step 4.7: Cause standard mapping (26 variants to 8 standard taxonomy)
    def map_cause(c):
        c_str = str(c).strip().lower()
        if any(x in c_str for x in ["ต้นไม้", "กิ่งไม้", "tree"]):
            return "tree"
        if any(x in c_str for x in ["ฟ้าผ่า", "lightning"]):
            return "lightning"
        if any(x in c_str for x in ["สัตว์", "งู", "นก", "กระรอก", "animal"]):
            return "animal"
        if any(x in c_str for x in ["อุปกรณ์", "หม้อแปลง", "ลูกถ้วย", "equipment"]):
            return "equipment"
        if any(x in c_str for x in ["รถชน", "vehicle"]):
            return "vehicle"
        if any(x in c_str for x in ["ไฟเกิน", "โหลดเกิน", "overload"]):
            return "overload"
        if any(x in c_str for x in ["ดับไฟตามแผน", "ปฏิบัติงานตามแผน", "planned"]):
            return "planned"
        return "unknown"
    
    o["cause_clean"] = o["cause"].map(map_cause)
    
    # Step 4.8: Outage Type (Planned vs Unplanned)
    def map_outage_type(t):
        t_str = str(t).strip().lower()
        if any(x in t_str for x in ["unplanned", "ไม่ได้วางแผน"]):
            return "unplanned"
        return "planned"
    o["outage_type_clean"] = o["outage_type"].map(map_outage_type)
    # If cause is planned, ensure outage_type is planned
    o.loc[o["cause_clean"] == "planned", "outage_type_clean"] = "planned"
    
    # Step 4.9: Crew arrival min
    crew_num = pd.to_numeric(o["crew_arrival_min"], errors="coerce").abs()
    # Impute missing crew arrival using area median
    area_crew_med = {
        "urban": 18.0,
        "suburban": 28.0,
        "rural": 49.0
    }
    imputed_crew = o["area_type"].map(area_crew_med).fillna(30.0)
    o["crew_arrival_min_clean"] = crew_num.fillna(imputed_crew).round(1)
    
    # Step 4.10: Deduplicate on Business Key (feeder + start_time)
    o = o.sort_values("outage_id").drop_duplicates(subset=["feeder_id", "start_time_dt"], keep="first")
    
    # Step 4.11: Exclude out-of-scope typo years (2014, 2042, 2204)
    valid_year = o["start_time_dt"].between("2023-01-01", "2024-12-31 23:59:59")
    o = o[valid_year].copy()
    
    # Calculate Customer Minutes
    o["customer_minutes"] = (o["customers_affected_clean"] * o["duration_min_clean"].fillna(0)).round().astype(int)
    
    # Format strings for export
    o["start_time"] = o["start_time_dt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    o["end_time"] = o["end_time_dt"].dt.strftime("%Y-%m-%d %H:%M:%S")
    o["duration_min"] = o["duration_min_clean"].fillna(0).astype(int)
    o["customers_affected"] = o["customers_affected_clean"]
    o["cause"] = o["cause_clean"]
    o["outage_type"] = o["outage_type_clean"]
    o["crew_arrival_min"] = o["crew_arrival_min_clean"]
    
    final_outage_cols = [
        "outage_id", "feeder_id", "start_time", "end_time", "duration_min",
        "customers_affected", "cause", "outage_type", "report_channel",
        "crew_arrival_min", "customer_minutes"
    ]
    df_outages = o[final_outage_cols].sort_values("outage_id").reset_index(drop=True)
    print(f"Outages cleaned: {len(df_outages)} rows (expected 2,743)")

    # ----------------------------------------------------
    # 5. EXPORT CLEANED FILES & SAMPLES
    # ----------------------------------------------------
    # Outages
    df_outages.to_csv(os.path.join(clean_dir, "outages_clean.csv"), index=False, encoding="utf-8-sig")
    df_outages.to_parquet(os.path.join(clean_dir, "outages_clean.parquet"), index=False)
    df_outages.head(100).to_csv(os.path.join(sample_dir, "outages_sample.csv"), index=False, encoding="utf-8-sig")
    
    # Feeders
    f.to_csv(os.path.join(clean_dir, "feeders_clean.csv"), index=False, encoding="utf-8-sig")
    f.to_parquet(os.path.join(clean_dir, "feeders_clean.parquet"), index=False)
    f.head(10).to_csv(os.path.join(sample_dir, "feeders_sample.csv"), index=False, encoding="utf-8-sig")
    
    # Substations
    df_subs.to_csv(os.path.join(clean_dir, "substations_clean.csv"), index=False, encoding="utf-8-sig")
    df_subs.to_parquet(os.path.join(clean_dir, "substations_clean.parquet"), index=False)
    
    # Weather
    w.to_csv(os.path.join(clean_dir, "weather_clean.csv"), index=False, encoding="utf-8-sig")
    w.to_parquet(os.path.join(clean_dir, "weather_clean.parquet"), index=False)
    w.head(100).to_csv(os.path.join(sample_dir, "weather_sample.csv"), index=False, encoding="utf-8-sig")

    print("\n--- Pipeline Complete! All files written to data/clean/ and data/sample/ ---")
    return df_outages, f, df_subs, w

if __name__ == "__main__":
    run_pipeline(
        raw_dir=r"C:\Users\Surface\Documents\MrG\data\raw",
        clean_dir=r"C:\Users\Surface\Documents\MrG\data\clean",
        sample_dir=r"C:\Users\Surface\Documents\MrG\data\sample"
    )
