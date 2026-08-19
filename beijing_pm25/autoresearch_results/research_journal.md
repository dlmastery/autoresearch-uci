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

75 DISCARDs on the 1h gate. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp81 t+6 test 53.93 beat Exp76 but val 57.86 missed; Exp83 bagging_temperature no-op; Exp84 drop rh_magnus missed.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp83–84)

New Exp81 slices: January **82.18 vs Exp76 80.40**. RH<40 **47.28 vs 46.72**. RH>=85 **56.25 vs 55.53**. RH 40-70 is the only CatBoost win (**56.00 vs 57.44**).

**Exp83 DISCARD** bagging_temperature=2. Bit-identical to Exp81. Axis closed: T=2 inert on Plain.

**Exp84 DISCARD** drop rh_magnus. Val 58.075 / test 54.155. RH<40 47.49 worse. Keep rh_magnus on CatBoost t+6.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. CatBoost **10/50**.

## Next (original process)

1. Stay isolated on **CatBoost**. Best 1h CatBoost is Exp78 Plain depth6 lr=0.03
2. Next: random_strength (wired) or return to 1h Exp78
3. Do not retry bagging_temperature / l2=10 / drop rh_magnus / Ordered / lr 0.01 / depth 4. Do not start MLP
