# Features and data — UCI 381 Beijing PM2.5

Authoritative sources: `beijing_pm25/prepare_data.py`, `beijing_pm25/add_extra_features.py`, `beijing_pm25/calendar_split.py`, `beijing_pm25/data/split_manifest.json`.

## 1. Prediction target

| Field | Formula | Use |
|---|---|---|
| `pm25` | US Embassy hourly PM2.5 (µg/m³) at hour **t** | **PRIMARY** nowcast target |

Contract: features at row t may use `pm25[t−1] … pm25[t−24]` and meteorology at **t**. They may **not** use `pm25[t]` or any future PM2.5. Contemporaneous weather is allowed (nowcast, not multi-hour forecast).

## 2. Raw source

- Liang, Zou, Guo, Li, Zhang, Zhang, Huang, Chen 2015 *Proc. Royal Society A* — UCI 381, doi:10.24432/C5JS49
- File: `PRSA_data_2010.1.1-2014.12.31.csv`
- 43,824 hours, 2010-01-01 00:00 to 2014-12-31 23:00
- Target NA hours are dropped after lag construction (manifest `n_rows=37596`)

| Column | Meaning |
|---|---|
| `pm2.5` | Embassy PM2.5 µg/m³ |
| `DEWP` | Dew point °C |
| `TEMP` | Temperature °C |
| `PRES` | Pressure hPa |
| `cbwd` | Combined wind direction (NE/NW/SE/cv) |
| `Iws` | Cumulative wind speed m/s |
| `Is` | Snow hours |
| `Ir` | Rain hours |

## 3. Frozen split

Protocol id: `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`

| Role | Years | n | Time range | SHA-256 |
|---|---|---:|---|---|
| train | 2010–2012 (− last 24 h) | 21725 | 2010-01-03 00:00 → 2012-12-30 23:00 | `a3cb4146ec49d917…` |
| val | 2013 (− last 24 h) | 7884 | 2013-01-01 00:00 → 2013-12-28 19:00 | `0f1e8f4e0f4e7c94…` |
| test | **2014 full year** | 7950 | 2014-01-01 00:00 → 2014-12-31 23:00 | `efb0012c1873e5bf…` |
| unused embargo | year-boundary 24 h | 37 | — | — |

`test_hash` full: `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

Random / stratified k-fold is forbidden (Bergmeir, Hyndman & Koo 2018 IJF, arXiv:1905.11744).

## 4. Engineered features

### 4.1 Base (always on after prepare_data)

| Feature | Citation / reason |
|---|---|
| `pm25_lag1` … `pm25_lag24` | Persistence + diurnal cycle; 24 h = max lag and embargo |
| `DEWP` `TEMP` `PRES` `Iws` `Is` `Ir` | Liang 2015 meteorology / ventilation |
| `cbwd_NE` `cbwd_NW` `cbwd_SE` `cbwd_cv` | One-hot wind direction (NW often clean) |
| `hour_sin` `hour_cos` | Cyclic hour |
| `dow` `is_weekend` | Weekly activity cycle |

### 4.2 KEEP features

| Feature | First KEEP | Citation |
|---|---|---|
| `inversion_spread` = TEMP − DEWP | Exp14 | Liang 2015 ventilation / mixing |
| `pm25_delta1` = lag1 − lag2 | Exp15 | Onset momentum (diagnosed residual) |

### 4.3 Tried and discarded

| Feature | Exp | Why discarded |
|---|---|---|
| `Iws_lag1` `TEMP_lag1` `DEWP_lag1` | 16, 23 | Composite fell; contemporaneous weather already present |
| raw `hour` plus cyclic hour | 24 | Redundant with hour_sin/cos |
| `is_heating` Nov–Feb flag | 31 | Redundant with TEMP; val/test both worse |

## 5. Persistence floor

On the frozen 2014 test year, ŷ(t)=y(t−1):

| Split | n | RMSE | MAE | p99 \|err\| | max |
|---|---:|---:|---:|---:|---:|
| train | 21725 | 24.543 | 13.046 | 91.0 | 769 |
| val | 7884 | 24.500 | 12.947 | 101.0 | 348 |
| test | 7950 | **22.316** | 12.035 | 80.5 | 500 |

Every model must beat 22.316 on this exact test hash. Exp30 skill = **+6.15%**.
