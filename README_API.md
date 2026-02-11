# API & Integration Notes

This project is currently a Streamlit dashboard and does not expose a public API. This document outlines recommended API contracts and integration points if you plan to add programmatic access.

## Use Cases for an API
- Provide aggregated metrics to other systems (e.g., dashboards, mobile apps)
- Allow remote upload of CSVs or streaming data
- Trigger anomaly scans or forecasting runs remotely

## Suggested Endpoints (Flask/FastAPI examples)

### 1. GET /api/v1/summary
Returns aggregated KPIs for the requested date range and states.

Request params:
- `start_date` (YYYY-MM-DD)
- `end_date` (YYYY-MM-DD)
- `states` (comma-separated)

Response (JSON):
```json
{
  "total_enrolments": 12345,
  "total_updates": 6789,
  "top_districts": [{"district":"X","enrolments":2000}],
  "pareto_pct": 82.3
}
```

### 2. POST /api/v1/upload
Upload a CSV file for processing (multipart/form-data).

Response: job id + status. Server processes file, returns validation report.

### 3. POST /api/v1/forecast
Trigger forecasting with optional model parameters.

Request body:
```json
{ "horizon": 30, "method": "arima" }
```

Response: forecast id and a short summary or direct forecast array.

### 4. GET /api/v1/anomalies
Return list of detected anomalies for provided filters.

Params: `start_date`, `end_date`, `states`

Response: list of pincodes + anomaly score.

## Implementation Notes
- Use **FastAPI** for a production-ready async API.
- Keep ML workloads in background tasks (Celery/RQ) if heavy.
- Use authentication (JWT / API keys) when exposing to the network.

## Minimal FastAPI Sketch

```python
from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post('/api/v1/upload')
async def upload(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    # validate and store
    return {"status": "received", "rows": len(df)}
```

## Data Contract
- Reuse the same data schema as `README_DATA_SCHEMA.md`.
- API responses should include timestamps and data versioning.

## Security
- Use HTTPS for all endpoints.
- Rate-limit heavy endpoints (forecast, anomaly) to prevent abuse.

---

If you'd like, I can scaffold a minimal `FastAPI` service inside this repo and wire one example endpoint to return basic KPIs.