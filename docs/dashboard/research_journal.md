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

25 DISCARDs. Notable near-miss: LightGBM Exp25 test **20.905** — DISCARD because val 22.711 lost to the then-champion.

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, L1/L2, CatBoost defaults, `is_heating`, GOSS, DART (no early stop, test 24.57), default Huber (test 81.46): no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Onset n=95 RMSE 103.35. January 33.07. Hour 20 31.93. Spike F1@75 = 0.941.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp33–34)

**Exp33 DISCARD** Rashmi & Gilad-Bachrach 2015 DART. Composite −25.869 (val 25.869, test 24.569). LightGBM cannot early-stop DART, so all 2000 trees ran and blurred lag-1 persistence. Axis closed for default DART / drop_rate / max_drop.

**Exp34 DISCARD** Ke 2017 Huber (default alpha 0.9). Composite −81.561 (val 80.885, test 81.461). Default Huber threshold is ~100× too small on µg/m³ PM2.5. Axis closed for default huber/mae/tweedie/quantile without an explicit scale.

Champion unchanged: Exp30.

## Next (original process)

1. LightGBM Geurts extra_trees=True on Exp30 (keep L2 + gbdt)
2. Or Ke 2017 `min_data_in_leaf=100` (not 10/50 — those 1h HP values are exhausted)
3. Onset/collapse features only after remaining paper knobs, or t+6 on the same timestamps
4. Do not start CatBoost/MLP until LightGBM hits 50 or is snapshotted as `lightgbm_final`
