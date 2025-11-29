# Environment Variables for Stormwatch

Stormwatch uses environment variables so the project can be redeployed to different environments without modifying code. Terraform will populate these values at deploy time, but the variables below document what each Lambda function expects and their typical values for the Edinburgh deployment.

---

## Lambda #1 - fetch_weather

### Required Variables

| Variable | Description | Example Value |
|----------|-------------|------------------------------|
| `WEATHER_API_BASE_URL` | Base URL for weather API | `https://api.open-meteo.com/v1/forecast` |
| `LOCATION_LAT` | Latitude of target location | `55.9486` *(Edinburgh Castle)* |
| `LOCATION_LON` | Longitude of target location | `-3.1999` *(Edinburgh Castle)* |
| `TIMEZONE` | Timezone string for API results | `GMT` |
| `RAW_BUCKET_NAME` | S3 bucket for raw JSON drops | `stormwatch-raw-json-xyz` |
| `RAW_BUCKET_PREFIX` | (Optional) Prefix for stored JSON files | `raw/` |
| `FORECAST_DAYS`      | Number of days of forecast to fetch | `1`

### Notes
- `LOCATION_LAT` and `LOCATION_LON` define the location the forecast is pulled for.
- `RAW_BUCKET_PREFIX` defaults to `raw/` if not provided.
- `FORECAST_DAYS=1` means “fetch just one day of forecast data”.


---

## Lambda #2 - transform_store

### Required Variables

| Variable | Description | Example Value |
|----------|-------------|------------------------------|
| `WEATHERRISK_TABLE_NAME` | DynamoDB table for processed data | `stormwatch-risk-db-xyz` |
| `LOCATION_PK` | Partition key value for this deployment | `EDINBURGH` |

### Notes
- `LOCATION_PK` allows deployment to multiple locations in future.
- `WEATHERRISK_TABLE_NAME` must match the DynamoDB table created by Terraform.

---

## DynamoDB Table Schema

### Partition and Sort Keys

| Field | Example | Purpose |
|--------|----------|----------|
| `PK` | `EDINBURGH` | Location identifier |
| `SK` | `1764288000` | Unix timestamp |

### Attribute Summary

Each daily item will include:

- `unix_timestamp`
- `date`
- `location`
- temperature fields (`temp_min`, `temp_max`, `temp_mean`)
- precipitation (`precip_prob_max`)
- wind (`wind_speed_max`, `wind_gust_max`)
- weather condition code (`weathercode`)
- derived fields:
  - `wc_label`
  - `risk_score`
  - `risk_level`

---

## Summary

For development/testing, the following default environment variable set is valid:

```env
WEATHER_API_BASE_URL="https://api.open-meteo.com/v1/forecast"
LOCATION_LAT="55.9486"
LOCATION_LON="-3.1999"
TIMEZONE="GMT"
FORECAST_DAYS="1"

RAW_BUCKET_NAME="stormwatch-raw-json-xyz"
RAW_BUCKET_PREFIX="raw/"

WEATHERRISK_TABLE_NAME="stormwatch-risk-db-xyz"
LOCATION_PK="EDINBURGH"