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

52 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, **Exp59** (cbwd_prev_NW, val 57.60 / test 54.42). Exp60–61 rain_mass and bagging_freq missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp61)

New Exp59 slices: **hours 21–23 × persist≥150 n=167 actual increment +0.92, pred +30.81**. Late-clean air is calibrated. Wednesday RMSE 61.22 vs Monday 47.13. bagging_fraction 0.6 was inert (freq 0).

**Exp61 DISCARD** bagging_freq=1. Val 57.736 lost to 57.601, test 54.430 flat. Late-dirty increment stayed +30.63. Axis closed: t+6 bagging.

t+6 recipe remains Exp59. 1h champion unchanged: Exp30.

## Next (original process)

1. Stay on Exp59. Late-dirty +31 overforecast is open; do not add persist×hour products
2. Do not retry bagging / L2 / ff / path_smooth / rain products / prev-direction
3. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
