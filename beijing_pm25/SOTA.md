# Published numbers on UCI 381 Beijing PM2.5 (this file)

There is **no official leaderboard**. Papers disagree on horizon, split, NA handling, and whether weather at time t is allowed. Compare protocols before comparing RMSE.

Source series: US Embassy hourly PM2.5 + Capital Airport meteorology, 2010-01-01 to 2014-12-31 (Liang, Zou, Guo, Li, Zhang, Zhang, Huang, Chen 2015 *Proc. Royal Society A*; UCI doi:10.24432/C5JS49). 43,824 hours, ~2k NA targets.

## 1-hour-ahead (the usual "SOTA" table)

| Source | Task | Split (as stated) | Model | Test RMSE | Test MAE |
|---|---|---|---|---:|---:|
| Brownlee 2017 MLM tutorial (most-copied Keras LSTM) | t+1 from multivariate window | last 12 months test | untuned LSTM | **26.50** | — |
| Guo & Lin 2018 arXiv:1806.06384 Table 1 (window 30) | 1-step ARX on this series | paper's rolling/held-out | **MV-LSTM** | **24.79 ± 0.09** | **15.24 ± 0.04** |
| same paper | same | same | XGBoost (XGT) | 25.00 ± 0.02 | 15.72 ± 0.04 |
| same paper | same | same | Elastic Net | 26.03 ± 0.19 | 15.92 ± 0.02 |
| same paper | same | same | Random Forest | 33.84 ± 1.13 | 22.27 ± 0.03 |
| same paper | same | same | ARIMAX | 42.51 ± 0.13 | 40.05 ± 0.10 |
| Guo & Lin window 10 / 20 | 1-step | same family | MV-LSTM | 24.73 / 24.70 | 15.40 / 14.89 |
| **This repo Exp1 (2026-08-18)** | **nowcast t** from lag-1..24 + weather at t | last 20% time test (n=7519) | XGBoost Chen-Guestrin defaults | **20.49** | **11.21** |
| **This repo, same split** | persistence ŷ(t)=y(t−1) | same frozen test | — | **21.26** | **11.58** |

Guo & Lin 2018 MV-LSTM is the cleanest published 1-step number on **this exact UCI file**. Later blogs that report RMSE 5–10 usually leaked the target, used random CV, or predicted a scaled/normalized series without inverting.

## What those numbers mean

1-hour PM2.5 is **highly autocorrelated**. On our frozen tail, persistence already has RMSE 21.26 and spike-F1@75 ≈ 0.936. Beating it by 0.77 µg/m³ (Exp1 skill +3.6%) is real but small. R² 0.95 is mostly lag-1, not meteorology.

So:

- **1-hour nowcast/forecast on this file is nearly saturated by persistence.** That is why Guo & Lin's "SOTA" (24.8) is only a few points from a last-value carry. Different NA fills and year cuts move RMSE by more than most model upgrades.
- **The unsaturated, useful work is longer horizon and episode onsets.** Persistence p99 |error| = 75 µg/m³ and max = 500 on our test tail. 6 h / 12 h / 24 h forecasts in the literature routinely sit at RMSE 40–80+ and are what health alerts actually need.
- Papers on the **12-site PRSA 2013–2017** set (UCI 501), not this file, are a different benchmark. Do not mix them.

## Implication for the Grok loop

Do not spend the next 20 experiments shaving 0.2 RMSE off 1-hour nowcast. Next KEEP-worthy axes:

1. **t+6 / t+12 / t+24** on the same frozen dates (harder, still useful).
2. **Spike / exceedance F1** at 75 or 150 µg/m³ (operational).
3. **Weather-only ablation** (no PM2.5 lags) to measure the Liang 2015 ventilation mechanism without the lag-1 crutch.
