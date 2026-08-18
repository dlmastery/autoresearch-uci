# Published numbers on UCI 381 Beijing PM2.5

There is **no official leaderboard**. Compare protocols before comparing RMSE.

## Frozen protocol in this repo

`uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`

- train: 2010-01-03 → 2012-12-30 (after 24 h embargo)
- val: 2013-01-01 → 2013-12-28
- test: **2014-01-01 → 2014-12-31** (frozen; `test_hash` in `data/split_manifest.json`)

This is the operational / industry cut (future calendar year), not Brownlee's first-365-days-train tutorial cut and not a random 80/20.

## 1-hour-ahead published numbers (other splits)

| Source | Task | Split | Model | Test RMSE | Test MAE |
|---|---|---|---|---:|---:|
| Guo & Lin 2018 arXiv:1806.06384 | 1-step ARX | 70/10/20 | MV-LSTM | 24.79 ± 0.09 | 15.24 |
| same | same | same | XGBoost | 25.00 | 15.72 |
| Brownlee 2017 | t+1 | first 365×24 train, rest test | untuned LSTM | 26.50 | — |
| **This repo Exp1** | nowcast t | **frozen 2014** | XGBoost C&G 2016 | **21.768** | — |
| **This repo** | ŷ(t)=y(t−1) | **frozen 2014** | persistence | **22.316** | 12.035 |

Exp1 skill vs 2014 persistence is **+2.5%**. 1-hour nowcast is nearly a last-value problem. The unsaturated work is t+6 / t+12 / episode onsets (2014 persistence p99 |err| = 80.5 µg/m³, max 500).
