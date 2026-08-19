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

71 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp78 Plain NEAR-MISS (val 22.472); Exp79 lr=0.01 and Exp80 depth=4 missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp79–80)

New Exp78 slices: January persist>=150 typical n=149 RMSE **40.32 vs Exp30 31.84 / persist 20.81**, pred **−13.0 vs need −0.8**. Hour 10 **25.23 vs 21.40**. January hour 22 **46.37 vs 34.49**.

**Exp79 DISCARD** CatBoost Plain lr=0.01. Val 22.587 / test 21.040. Jan typical 37.55 / pred −11.4 (right way). Val worse than Exp78.

**Exp80 DISCARD** CatBoost Plain depth=4. Val 22.795 / test 21.057. Jan typical 36.10 / pred −9.6. Onset 108.81 beat Exp30. JJA tax.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. Best CatBoost remains Exp78. CatBoost **6/50**.

## Next (original process)

1. Stay isolated on **CatBoost**. Best 1h CatBoost is Exp78 Plain depth6 lr=0.03
2. Next: l2_leaf_reg or CatBoost t+6. Do not retry Ordered / lr 0.01 / depth 4
3. Do not start MLP. Do not mix t+6 val with the Exp30 1h composite
