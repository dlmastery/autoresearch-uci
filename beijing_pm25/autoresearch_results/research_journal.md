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

86 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp91 rh_magnus NEAR-MISS val **22.449**; Exp94 cbwd_prev_NW and Exp95 random_strength=2 both DISCARD.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp93)

New Exp91 slices: hour 10 RMSE **23.95 vs Exp30 21.40 / persist 22.86**. Hour 22 **20.95 vs persist 20.19**. January cv **32.53 vs persist 26.72**.

**Exp93 DISCARD** rsm=0.8. Val 22.569 worse than Exp91 22.449. Test **20.945** ties Exp30. Hour-10 23.27.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. CatBoost **19/50**. Best CatBoost val remains Exp91.

## This fire (2026-08-18, Exp94–Exp95)

New Exp91 slices: PRES>=1025 persist>=150 n=413 RMSE **44.27 vs Exp30 41.59 / persist 40.56**. Over-cleans pred_d **−12.2 vs need −3.2**. No previous-hour NW subset n=277 RMSE **43.72 vs persist 38.64**.

**Exp94 DISCARD** cbwd_prev_NW. Val 22.528 test 21.063. hiP dirty 44.27→43.36 (in 40–43) but no-NW stagnant 43.72→43.66 flat; dummy helped previous-NW hours instead.

**Exp95 DISCARD** random_strength=2. Val 22.451 vs Exp91 22.449 (inert). Test 21.005. hiP dirty 43.89 missed 40–43.5.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. CatBoost **21/50**. Best CatBoost val remains Exp91.

## Next (original process)

1. Stay isolated on **CatBoost Exp91** (Plain + rh_magnus, val 22.449)
2. Do not retry rsm=0.6 / l2=10 / month_sin / accel / Lossguide / cbwd_prev_SE / random_strength=5
3. Leave the 0.052 NEAR-MISS or bagging_temperature on 1h (wired, t+6 inert). Do not start MLP
