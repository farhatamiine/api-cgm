# api-cgm

A project created with FastAPI CLI.

## Quick Start

### Start the development server

```bash
uv run fastapi dev
```

Visit http://localhost:8000

### Deploy to FastAPI Cloud

> FastAPI Cloud is currently in private beta. Join the waitlist at https://fastapicloud.com

```bash
uv run fastapi login
uv run fastapi deploy
```

## Clinical Calculations & Logic

This project implements several clinical metrics essential for effective diabetes management:

- **Glucose Management Indicator (GMI):** Estimates laboratory A1c using the formula `3.31 + (0.02392 * average_glucose_mgdL)`.
- **Time in Range (TIR):** Measures the percentage of time glucose is within **70–180 mg/dL**.
- **Glucose Variability (CV):** Assesses glucose stability; a Coefficient of Variation **≤ 36%** is considered stable.
- **Dawn Phenomenon:** Detects early morning hormonal surges by comparing 2 AM and 7 AM averages.
- **Bolus Timing:** Calculates the optimal injection-to-meal interval based on current glucose and meal GI.
- **Ambulatory Glucose Profile (AGP):** Provides a "modal day" view by calculating percentiles (5th–95th) for every hour.

For more detailed information on formulas and clinical rationale, see [CALCULATIONS.md](./CALCULATIONS.md).

## Project Structure

- `main.py` - Your FastAPI application
- `pyproject.toml` - Project dependencies

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [FastAPI Cloud](https://fastapicloud.com)
