"""Download UCI 381 Beijing PM2.5 and write a causal nowcast feature table.

Target: pm25 at hour t.
Features: pm25 lags 1..24 + contemporaneous meteorology at t (nowcast contract).
No future PM2.5 enters any feature.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlretrieve

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
import sys
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
RAW_NAME = "PRSA_data_2010.1.1-2014.12.31.csv"
URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/00381/"
    "PRSA_data_2010.1.1-2014.12.31.csv"
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download_raw() -> Path:
    DATA.mkdir(parents=True, exist_ok=True)
    dest = DATA / RAW_NAME
    meta = DATA / f"{RAW_NAME}.meta.json"
    if dest.exists() and meta.exists():
        print(f"cache hit {dest}")
        return dest
    print(f"downloading {URL}")
    urlretrieve(URL, dest)
    rec = {
        "source": "UCI ML Repository 381 — Beijing PM2.5 Data",
        "url": URL,
        "query": {"dataset": "beijing-pm25", "uci_id": 381},
        "variables": ["pm2.5", "DEWP", "TEMP", "PRES", "cbwd", "Iws", "Is", "Ir"],
        "spatial_extent": ["Beijing US Embassy"],
        "time_range": ["2010-01-01", "2014-12-31"],
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "tool_version": "prepare_data.py",
        "license": "UCI — cite Liang et al. 2015",
        "checksum": _sha256(dest),
    }
    meta.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return dest


def build_features(raw_path: Path) -> Path:
    df = pd.read_csv(raw_path)
    df["time"] = pd.to_datetime(df[["year", "month", "day", "hour"]])
    df = df.sort_values("time").reset_index(drop=True)
    df = df.rename(columns={"pm2.5": "pm25"})

    # Wind direction one-hot (cbwd is categorical: NE/NW/SE/cv)
    wind = pd.get_dummies(df["cbwd"], prefix="cbwd", dtype=float)
    out = pd.concat(
        [
            df[["time", "pm25", "DEWP", "TEMP", "PRES", "Iws", "Is", "Ir"]],
            wind,
        ],
        axis=1,
    )
    for lag in range(1, 25):
        out[f"pm25_lag{lag}"] = out["pm25"].shift(lag)

    out["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    out["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    out["dow"] = df["time"].dt.dayofweek.astype(float)
    out["is_weekend"] = (out["dow"] >= 5).astype(float)

    before = len(out)
    out = out.dropna().reset_index(drop=True)
    print(f"dropped {before - len(out)} rows (NaN pm25 or warmup lags); kept {len(out)}")

    # Time-sorted; runner HoldoutSplit order=time uses row order.
    # Keep `time` out of the runner CSV so every remaining column is numeric.
    times_path = DATA / "times.csv"
    out[["time"]].to_csv(times_path, index=False)
    feature_path = DATA / "features.csv"
    model_df = out.drop(columns=["time"])
    model_df.to_csv(feature_path, index=False)
    print(f"wrote {feature_path} shape={model_df.shape}")
    print(f"pm25 mean={model_df['pm25'].mean():.2f} std={model_df['pm25'].std():.2f} "
          f"min={model_df['pm25'].min():.1f} max={model_df['pm25'].max():.1f}")
    print(f"time {out['time'].iloc[0]} → {out['time'].iloc[-1]}")
    from calendar_split import build_manifest
    build_manifest(out["time"], DATA)
    return feature_path


def main() -> None:
    raw = download_raw()
    build_features(raw)


if __name__ == "__main__":
    main()
