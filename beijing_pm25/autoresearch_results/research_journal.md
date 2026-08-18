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

33 DISCARDs. Notable near-misses: LightGBM Exp25 test **20.905** (val lost); Exp38 pm25_accel val **22.426**; Exp40 vent_index test **20.939**.

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, L1/L2, CatBoost defaults, `is_heating`, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, pm25_accel, vent_index, max_bin 127, roll6max: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp41–42)

New slices: haze streaks ≥6h n=1069 **model 29.31 vs persist-1 28.94**. High-PRES tercile skill only **+3.7%** (low-PRES +7.8%).

**Exp41 DISCARD** Ke 2017 max_bin=127. Composite −22.738 (val 22.738, test 21.368). Coarser histograms hurt. Axis closed for max_bin.

**Exp42 DISCARD** pm25_roll6max. Composite −22.515 (val 22.515, test 20.956). Redundant with lag1–6. Axis closed for roll6 pools.

Champion unchanged: Exp30. 1h regularizers and episode pools have stalled.

## Next (original process)

1. Hillclimb **t+6** from Exp39 vs persist-6 (separate composite; do not mix with 1h)
2. Or multi-seed variance on Exp30
3. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
