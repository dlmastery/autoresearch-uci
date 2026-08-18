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

27 DISCARDs. Notable near-miss: LightGBM Exp25 test **20.905** — DISCARD because val 22.711 lost to the then-champion.

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, L1/L2, CatBoost defaults, `is_heating`, GOSS, DART (test 24.57), default Huber (test 81.46), extra_trees (val 22.99), min_data_in_leaf 100 (val 22.66): no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp35–36)

New slices on Exp30: January evening 18–21 RMSE **42.61** (vs January day 23.57); SE-wind onsets RMSE **131.89** (38 of 83); windy-Iws onsets RMSE 163.64.

**Exp35 DISCARD** Geurts 2006 extra_trees. Composite −22.989 (val 22.989, test 21.238). Random Iws/cbwd thresholds hurt the 2013 bottleneck. Axis closed for extra_trees.

**Exp36 DISCARD** Ke 2017 min_data_in_leaf=100. Composite −22.662 (val 22.662, test 21.127). Larger leaves underfit. Axis closed for this leaf floor.

Champion unchanged: Exp30.

## Next (original process)

1. Shi et al. `linear_tree=True` on Exp30 (keep L2 + gbdt + greedy splits)
2. If that DISCARDs, rethink: new onset feature (not is_heating / weather lags / raw hour) or t+6
3. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
