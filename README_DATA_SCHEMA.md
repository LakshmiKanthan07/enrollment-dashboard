# Data Schema & Validation

This document describes the expected structure, data types and validation checks for `unified_enrolment_data.csv` used by the Aadhaar Insight AI dashboard.

## Required Columns

- `date` (datetime) — ISO format (YYYY-MM-DD). Used for all time-series analysis and forecasting.
- `state` (string) — State name.
- `district` (string) — District name.
- `pincode` (integer) — 6-digit postal code.
- `bio_age_5_17` (int) — Biometric updates for age group 5–17.
- `bio_age_17_` (int) — Biometric updates for age group 17+.
- `demo_age_5_17` (int) — Demographic updates for age group 5–17.
- `demo_age_17_` (int) — Demographic updates for age group 17+.
- `age_0_5` (int) — New enrolments for age group 0–5.
- `age_5_17` (int) — New enrolments for age group 5–17.
- `age_18_greater` (int) — New enrolments for age 18+.

## Derived Columns (computed by the app)

- `Biometric Updates` = `bio_age_5_17` + `bio_age_17_`
- `Demographic Updates` = `demo_age_5_17` + `demo_age_17_`
- `Total Updates` = `Biometric Updates` + `Demographic Updates`
- `Total Enrolments` = `age_0_5` + `age_5_17` + `age_18_greater`
- `MBU_Gap_Index` = `bio_age_5_17` / `age_5_17` (safe-guarded for zero denominators)
- `Migration_Intensity` = `demo_age_17_` / (`age_18_greater` + 1)
- `Weighted_Effort` = (`Total Enrolments` * 3) + (`Biometric Updates` * 2) + (`Demographic Updates` * 1)

## Validation Rules

- `date` must parse to pandas datetime; rows with unparsable dates should be investigated.
- Numeric fields must be non-negative integers; negative values should be cleaned.
- `pincode` should be 6 digits; filter out or flag invalid pins.
- Check for duplicates (same `date`, `pincode`) — decide whether to aggregate or dedupe.

## Minimal Example (CSV)

```
date,state,district,pincode,bio_age_5_17,bio_age_17_,demo_age_5_17,demo_age_17_,age_0_5,age_5_17,age_18_greater
2024-01-01,Maharashtra,Mumbai,400001,10,5,3,2,20,30,50
2024-01-02,Karnataka,Bengaluru,560001,5,2,1,4,15,25,30
```

## Quick Validation Script (python)

```python
import pandas as pd

df = pd.read_csv('unified_enrolment_data.csv')
# parse dates
df['date'] = pd.to_datetime(df['date'], errors='coerce')
print('Missing dates:', df['date'].isna().sum())
# negative checks
num_cols = ['bio_age_5_17','bio_age_17_','demo_age_5_17','demo_age_17_','age_0_5','age_5_17','age_18_greater']
print('Negative values per col:')
for c in num_cols:
    print(c, (df[c] < 0).sum())
# pincode format
print('Invalid pincodes:', df[~df['pincode'].astype(str).str.match(r"^\\d{6}$")].shape[0])
```

## Notes
- Keep a copy of raw CSV before transformations.
- If data is coming from multiple sources, standardize column names first.
- For small datasets, set missing numeric values to 0; for larger, consider imputations.
