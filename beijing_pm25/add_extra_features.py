"""Add optional feature columns without changing row order or the frozen split."""
from __future__ import annotations

from pathlib import Path

import numpy as np
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
    extra["pm25_roll6max"] = extra[[f"pm25_lag{k}" for k in range(1, 7)]].max(axis=1)
    extra["Iws_lag1"] = extra["Iws"].shift(1)
    extra["TEMP_lag1"] = extra["TEMP"].shift(1)
    extra["DEWP_lag1"] = extra["DEWP"].shift(1)
    extra["hour"] = pd.to_datetime(times["time"]).dt.hour.astype(float)
    mo = pd.to_datetime(times["time"]).dt.month
    extra["is_heating"] = mo.isin([11, 12, 1, 2]).astype(float)
    extra["month_sin"] = np.sin(2.0 * np.pi * mo / 12.0)
    extra["rh_magnus"] = (
        100.0 * np.exp(17.625 * extra["DEWP"] / (243.04 + extra["DEWP"])) / np.exp(
            17.625 * extra["TEMP"] / (243.04 + extra["TEMP"])
        )
    ).clip(0.0, 100.0)
    # First row of weather lags is NaN; fill from contemporaneous so n_rows stays frozen.
    extra["Iws_lag1"] = extra["Iws_lag1"].fillna(extra["Iws"])
    extra["TEMP_lag1"] = extra["TEMP_lag1"].fillna(extra["TEMP"])
    extra["DEWP_lag1"] = extra["DEWP_lag1"].fillna(extra["DEWP"])
    extra["cbwd_prev_NW"] = extra["cbwd_NW"].shift(1).fillna(extra["cbwd_NW"])
    extra["dewp_delta"] = extra["DEWP"].diff().fillna(0.0)
    extra["heating_night"] = extra["is_heating"] * (
        (extra["hour"] >= 18.0) | (extra["hour"] <= 6.0)
    ).astype(float)
    extra["rh_iws"] = extra["rh_magnus"] / (extra["Iws"] + 1.0)
    extra["heating_build"] = extra["is_heating"] * np.maximum(extra["pm25_delta1"], 0.0)
    extra["pres_delta"] = extra["PRES"].diff().fillna(0.0)
    extra["pm25_delta6"] = extra["pm25_lag1"] - extra["pm25_lag7"]
    extra["log_iws"] = np.log1p(extra["Iws"])
    extra["is_severe"] = (extra["pm25_lag1"] >= 250.0).astype(float)
    extra["evening_peak"] = (
        (extra["hour"] >= 18.0) & (extra["hour"] <= 21.0)
    ).astype(float)
    extra.to_csv(DATA / "features_full.csv", index=False)
    print("wrote", DATA / "features_full.csv", extra.shape)


if __name__ == "__main__":
    main()
