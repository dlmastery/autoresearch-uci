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

65 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, **Exp72** (extra_trees + linear_tree, val 57.43 / test 54.33). Exp74 bagging_freq=1 missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp74)

New Exp72 slices: **inv<=6 persist>=150 onsets n=129 RMSE 110.39 vs persist-6 98.51 (skill −12.1%)**, need **+91.0**, pred **−7.4**.

**Exp74 DISCARD** bagging_freq=1. Val 57.502 lost to 57.429, test 54.581. Moist-onset increment −9.3. Axis closed: extra_trees+linear bagging.

t+6 recipe remains Exp72. 1h champion unchanged: Exp30.

## Next (original process)

1. Stay on Exp72 extra_trees + linear_tree + ff=1.0. Do not retry bagging freq / max_bin 63 / linear_tree off / extra_trees off
2. Do not retry lags / rain products / persist×hour / prev-direction / leaf L1-L2 / PRES dummies
3. Two LGB slots left; then snapshot `lightgbm_final` or start CatBoost. Do not start CatBoost/MLP until LGB 50 or that snapshot.
