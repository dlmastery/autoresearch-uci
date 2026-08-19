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

67 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, **Exp75** rh_magnus (val 57.19 / test 54.73), **Exp76** linear_lambda=1 (val 57.16 / test 54.31). Exp74 bagging_freq=1 missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp75–76)

New Exp72 slices: persist>=250 typical n=237 RMSE **82.39 vs persist-6 28.27 (skill −191.5%)**, need **−0.1**, pred **−51.5**. Hour 22 RMSE **65.19**. RH 70-85 persist>=150 skill only **+4.8%**.

**Exp75 t+6 side-KEEP** (1h DISCARD) Magnus RH. Val 57.191 beat 57.429, test 54.730. Hour-6 RH=100 row predicted 872 vs 116.

**Exp76 t+6 side-KEEP** (1h DISCARD) linear_lambda=1. Val 57.161 / test 54.312. Hour-6 67.07→53.55, blow-up 872→132. persist>=250 typical still −52.7.

t+6 recipe is now Exp76. 1h champion unchanged: Exp30. LightGBM **50/50**. Snapshot `code_versions/lightgbm_final/`.

## Next (original process)

1. Isolated **CatBoost** cycle (currently 2/50). Do not mix t+6 val with the Exp30 1h composite
2. Do not retry bagging / max_bin / another RH formula / linear_lambda nearby values first
3. persist>=250 typical still predicts −53 vs need 0 on Exp76 — open residual if returning to t+6 after CatBoost snapshot
