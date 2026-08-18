"""Add optional feature columns without changing row order or the frozen split."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def main() -> None:
    base = pd.read_csv(DATA / "features.csv")
    times = pd.read_csv(DATA / "times.csv", parse_dates=["time"])
    assert len(base) == len(times)
    extra = base.copy()
    extra["inversion_spread"] = extra["TEMP"] - extra["DEWP"]
    extra["pm25_delta1"] = extra["pm25_lag1"] - extra["pm25_lag2"]
    extra["pm25_accel"] = extra["pm25_lag1"] - 2.0 * extra["pm25_lag2"] + extra["pm25_lag3"]
    extra["vent_index"] = extra["Iws"] * extra["inversion_spread"]
    extra["Iws_lag1"] = extra["Iws"].shift(1)
    extra["TEMP_lag1"] = extra["TEMP"].shift(1)
    extra["DEWP_lag1"] = extra["DEWP"].shift(1)
    extra["hour"] = pd.to_datetime(times["time"]).dt.hour.astype(float)
    mo = pd.to_datetime(times["time"]).dt.month
    extra["is_heating"] = mo.isin([11, 12, 1, 2]).astype(float)
    # First row of weather lags is NaN; fill from contemporaneous so n_rows stays frozen.
    extra["Iws_lag1"] = extra["Iws_lag1"].fillna(extra["Iws"])
    extra["TEMP_lag1"] = extra["TEMP_lag1"].fillna(extra["TEMP"])
    extra["DEWP_lag1"] = extra["DEWP_lag1"].fillna(extra["DEWP"])
    extra.to_csv(DATA / "features_full.csv", index=False)
    print("wrote", DATA / "features_full.csv", extra.shape)


if __name__ == "__main__":
    main()
