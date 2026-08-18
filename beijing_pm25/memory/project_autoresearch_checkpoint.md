# Autoresearch checkpoint — after Exp38 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, boosting_type gbdt, L2, constant leaves
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (this fire: vs persistence and |delta1|)
- Onset actual−lag1>50: n=83 **model RMSE 110.05 vs persistence 107.80** (champion loses on jumps; bias −87)
- Collapse n=162 RMSE 74.59 vs persistence 97.87 (model helps drops)
- |delta1|≥20: 16.8% of hours, **44.8% of SSE**, RMSE 34.25
- |error| corr |delta1| = 0.35
- Post-onset hour n=73 RMSE 62.50, overshoot +13.3
- January RMSE 33.07 vs JJA 14.03 · Hour 20 RMSE 31.93 · Hour 1 RMSE 28.65
- Val is the composite bottleneck (22.397 vs test 20.945)

## This fire
- **Exp37 DISCARD** Shi linear_tree=True. Val 22.793 test 21.198. Intra-leaf slopes overfit.
- **Exp38 DISCARD / NEAR-MISS** add pm25_accel. Val 22.426 test 20.987. Almost redundant with delta1.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART, default Huber, is_heating, extra_trees, min_data_in_leaf=100, linear_tree, pm25_accel / nearby diffs

## Process
LightGBM **12/50**. Isolation holds. Champion unchanged. `features_full.csv` now also contains unused `pm25_accel` (not in champion).

## Next pasteable
1h L2 gbdt paper knobs and nearby diffs have stalled. Next: **t+6 on the same frozen 2014 timestamps**, or a non-diff domain feature. Do not start CatBoost/MLP. Do not retry linear_tree or accel variants.
