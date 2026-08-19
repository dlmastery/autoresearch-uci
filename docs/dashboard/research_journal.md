# Research journal — UCI 381 Beijing PM2.5

Karpathy rule: one change, KEEP if composite rose, otherwise revert. Test year 2014 never moved.

## The ladder

persistence (2014) test RMSE 22.316

**Exp1 KEEP** Chen & Guestrin 2016 XGBoost → 21.768. Skill +2.5%.

**Exp2 KEEP** max_depth 4. Test 21.996 (worse) but val 23.205 (better). Composite rose because val was the min(). Gate working.

**Exp4 KEEP** lr 0.01. Shrinkage on the depth-4 tree.

**Exp8 KEEP** subsample 0.6. Stochastic rows.

**Exp14 KEEP** inversion_spread = TEMP−DEWP (Liang 2015). First real test drop (21.823).

**Exp15 KEEP** pm25_delta1 = lag1−lag2. Onset momentum. Test 21.290.

**Exp22 KEEP** stack inversion onto delta. Test 21.122, val 22.470, skill +5.4%.

**Exp29 KEEP** LightGBM on those exact features. Test 20.784, val 22.428. First backbone KEEP that is not XGBoost.

**Exp30 KEEP** num_leaves 31→63. Test 20.945 (slightly worse) but val 22.397 (better). **Current champion.** Skill +6.15%.

## What was thrown away

77 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp85 Ordered t+6 val 57.66 closest CatBoost val, still miss; Exp86 random_strength=2 missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp85–86)

New Exp81 slices: wrong-sign onsets n=164 RMSE **129.01 vs persist-6 100.47**, persist mean **204**, need **+91.5**, pred **−24.9**. Val-test gap **3.93** vs LGB **2.85**.

**Exp85 DISCARD** CatBoost Ordered t+6. Val **57.658** beat Exp81 57.857, missed Exp76 57.161. Test 53.940. Wrong-sign pred −23.1. Closest CatBoost t+6 val.

**Exp86 DISCARD** Ordered random_strength=2. Val 57.684 / test 54.254. Wrong-sign still −23.8.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. CatBoost **12/50**.

## Next (original process)

1. Stay isolated on **CatBoost**. Return to **1h Exp78 Plain** with a new slice
2. Exp85 Ordered is the CatBoost t+6 val leader (still MISS)
3. Do not retry random_strength / bagging_temperature / l2=10 / drop rh_magnus / 1h Ordered / lr 0.01 / depth 4. Do not start MLP
