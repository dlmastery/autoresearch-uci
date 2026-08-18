"""Build as-of-t-6 features for the same rows/target timestamps.

Target stays pm25[t]. Weather and PM lags are information available at t-6.
Calendar encodings stay at valid time t (known when issuing a 6h forecast).
Row count and order are frozen so the calendar split hash is unchanged.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def main() -> None:
    src = pd.read_csv(DATA / "features_full.csv")
    n0 = len(src)
    out = src.copy()
    weather = ["DEWP", "TEMP", "PRES", "Iws", "Is", "Ir", "cbwd_NE", "cbwd_NW", "cbwd_SE", "cbwd_cv"]
    for c in weather:
        out[c] = src[c].shift(6)
    # Most recent PM at issue time t-6 is src.pm25 shifted 6, i.e. current lag6.
    out["pm25_lag1"] = src["pm25"].shift(6)
    for k in range(2, 25):
        out[f"pm25_lag{k}"] = src["pm25"].shift(5 + k)
    out["pm25_delta1"] = out["pm25_lag1"] - out["pm25_lag2"]
    out["pm25_delta6"] = out["pm25_lag1"] - out["pm25_lag7"]
    out["inversion_spread"] = out["TEMP"] - out["DEWP"]
    times = pd.read_csv(DATA / "times.csv", parse_dates=["time"])
    assert len(times) == n0
    out["month_sin"] = np.sin(2.0 * np.pi * times["time"].dt.month / 12.0)
    out["month_cos"] = np.cos(2.0 * np.pi * times["time"].dt.month / 12.0)
    # First ~29 train rows are NaN; bfill so n_rows stays frozen (all in 2010 train).
    fill_cols = weather + [f"pm25_lag{k}" for k in range(1, 25)] + ["pm25_delta1", "pm25_delta6", "inversion_spread"]
    out[fill_cols] = out[fill_cols].bfill()
    out["stagn_index"] = out["inversion_spread"] / (out["Iws"] + 1.0)
    # Issue-time 1h tendencies (t-6 minus t-7). Iws is cumulative and resets on
    # direction change, so Iws_delta is nearly collinear with Iws level.
    out["pres_delta"] = out["PRES"] - src["PRES"].shift(7)
    out["iws_delta"] = out["Iws"] - src["Iws"].shift(7)
    out["dewp_delta"] = out["DEWP"] - src["DEWP"].shift(7)
    out["haze_hours6"] = (
        out[[f"pm25_lag{k}" for k in range(1, 7)]] >= 150.0
    ).sum(axis=1).astype(float)
    fill_cols = fill_cols + ["pres_delta", "iws_delta", "dewp_delta"]
    out[fill_cols] = out[fill_cols].bfill()
    assert len(out) == n0
    assert out[fill_cols].isna().sum().sum() == 0
    assert out["stagn_index"].isna().sum() == 0
    dest = DATA / "features_horizon6.csv"
    out.to_csv(dest, index=False)
    print("wrote", dest, out.shape)
    # Persist-6 residual target: same rows/features, y := pm25[t] - last PM at t-6.
    resid = out.copy()
    resid["pm25"] = out["pm25"] - out["pm25_lag1"]
    rdest = DATA / "features_horizon6_resid.csv"
    resid.to_csv(rdest, index=False)
    print("wrote", rdest, resid.shape)


if __name__ == "__main__":
    main()
