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

31 DISCARDs. Notable near-misses: LightGBM Exp25 test **20.905** (val lost); Exp38 pm25_accel val **22.426**; Exp40 vent_index test **20.939** (val 22.439 lost).

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, L1/L2, CatBoost defaults, `is_heating`, GOSS, DART, default Huber, extra_trees, min_data_in_leaf 100, linear_tree (val 22.79), pm25_accel: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp39–40)

New 1h slices: haze ≥150 n=1638 **model 35.50 vs persist-1 35.31** (zero episode skill). Rain n=260 model 23.26 vs persist-1 27.27. Persist-6 on the same 7950 rows = **61.83**.

**Exp39 DISCARD** on the 1h gate (composite −58.824) but **t+6 skill +10.5%**: test 55.32 vs persist-6 61.83. January 85.24 vs p6 95.60. Same timestamps, as-of-t-6 features. Snapshot as a side ladder; do not mix composites.

**Exp40 DISCARD** vent_index = Iws×inversion. Test 20.939 (tiny win) val 22.439. Product redundant with the two parents.

Champion unchanged: Exp30.

## Next (original process)

1. Hillclimb **t+6** from Exp39 vs persist-6 (separate composite)
2. Stop shaving 1h nowcast HPs
3. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
