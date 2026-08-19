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

**Exp30 KEEP** num_leaves 31→63. Test 20.945 (slightly worse) but val 22.397 (better). Skill +6.15%. Held the 1h crown until Exp96.

**Exp96 KEEP** CatBoost Plain + rh_magnus + dewp_delta (Tie 2017). Test **20.881** · val **22.357** · composite **−22.357**. Skill +6.43%. First 1h KEEP since Exp30.

**Exp97 KEEP** is_heating on Exp96 (Huang 2014). Test **20.735** · val **22.167** · composite **−22.167**. **Current 1h champion.** Skill +7.09%.

## What was thrown away

86 DISCARDs then **Exp96 KEEP**. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp91 rh_magnus was the 0.052 NEAR-MISS that dewp_delta promoted.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Exp97 onset / month / hour slices after this KEEP. Skill +7.09%. January RH>=70 leftover still 36.68 vs persist 23.94.

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

1h champion was still Exp30 after Exp94–95. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp96 KEEP)

New Exp91 slices: Friday n=1119 RMSE **24.81 vs persist 24.13 / Exp30 23.59**. Hour-1 **29.71 vs persist 28.19**. dewp-rise persist>=150 n=378 RMSE **36.61 vs persist 35.88**, over-clean pred_d **−4.25 vs need +0.51**. dewp_delta corr with 1h increment **0.16**.

**Exp96 KEEP** dewp_delta. Val **22.357** beat Exp30 22.397. Test **20.881** beat 20.945. Composite **−22.357**. Friday 24.81→**24.03** (now beats persist). dewp-rise dirty only 36.61→36.47. **New 1h champion is CatBoost Exp96.**

CatBoost **22/50**. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp97 KEEP)

New Exp96 slices: January RH>=70 n=84 RMSE **38.25 vs persist 23.94 / Exp30 29.59** (skill −59.8%). January Iws<2 **34.91 vs persist 29.42**. January hour-1 **76.95 vs persist 69.40** (need +8.32 pred_d −5.35). Hour-1 outside January **20.63 ≈ persist 20.60**.

**Exp97 KEEP** is_heating. Val **22.167** beat Exp96 22.357. Test **20.735** beat 20.881. Composite **−22.167**. Skill **+7.09%**. January RH>=70 38.25→36.68 (missed 24–32). JJA 14.05→**13.84** (no month_sin summer tax). **New 1h champion is CatBoost Exp97.**

CatBoost **23/50**. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp98–Exp99)

New Exp97 slices: January RH>=70 is **all Ir=0**. January RH>=70 Iws<2 n=45 RMSE **42.65 vs persist 22.94** (skill −85.9%). January RH>=70 hours 0-5 n=37 RMSE **38.33 vs persist 18.85** (skill −103.4%). JJA RH>=70 Ir=0 is fine (14.93 vs persist 15.75).

**Exp98 DISCARD** heating_night. Val 22.343. Hours 0-5 38.33→37.60; Iws<2 42.65→**44.31** worse.

**Exp99 DISCARD** bagging_temperature=2. **Bit-identical** to Exp97.

1h champion unchanged: Exp97. CatBoost **25/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp100)

New Exp97 slices: January RH>=70 Iws<2 persist>=150 n=17 RMSE **68.74 vs persist 36.22**. January RH>=70 Iws<2 dewp_rise n=12 RMSE **51.75 vs persist 9.02**. January rh_iws q3 n=156 RMSE **39.39 vs persist 28.71**.

**Exp100 DISCARD** rh_iws. Val 22.178 (0.012 above Exp97). Test 20.726. January rh_iws q3 39.39→**40.03** worse. Ratio redundant with rh_magnus plus Iws.

1h champion unchanged: Exp97. CatBoost **26/50**. t+6 recipe remains Exp76.

## Next (original process)

1. Stay isolated on **CatBoost Exp97** (Plain + rh_magnus + dewp_delta + is_heating, val 22.167)
2. Do not retry stagn_index / heating_day / T=5 / month_sin / rsm / l2
3. January moist-calm persist leftover needs a non-ratio rethink. Do not start MLP
