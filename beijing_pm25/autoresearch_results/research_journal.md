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

29 DISCARDs. Notable near-misses: LightGBM Exp25 test **20.905** (val lost); Exp38 pm25_accel val **22.426** vs champion 22.397.

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, L1/L2, CatBoost defaults, `is_heating`, GOSS, DART, default Huber, extra_trees, min_data_in_leaf 100, linear_tree (val 22.79), pm25_accel: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp37–38)

New slices: onset n=83 **model 110.05 vs persistence 107.80** (champion loses on jumps). |delta1|≥20 is 16.8% of hours and 44.8% of SSE.

**Exp37 DISCARD** Shi 2018 linear_tree. Composite −22.793 (val 22.793, test 21.198). Intra-leaf slopes overfit. Axis closed for linear_tree. Third leaf-architecture miss (after extra_trees, min_data).

**Exp38 DISCARD / NEAR-MISS** pm25_accel second difference. Composite −22.426 (val 22.426, test 20.987). Almost redundant with delta1. Axis closed for nearby diffs.

Champion unchanged: Exp30.

## Next (original process)

1. **t+6** on the same frozen 2014 timestamps (1h nowcast paper knobs have stalled)
2. Or a non-diff domain feature (not is_heating / weather lags / raw hour / accel)
3. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
