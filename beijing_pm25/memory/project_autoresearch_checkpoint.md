# Autoresearch checkpoint — after Exp34 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, boosting_type gbdt, L2
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (recomputed this fire from exp30_predictions.csv)
- Onset actual−lag1>50: n=83 RMSE **110.05** (pred 171 vs actual 259, bias −87)
- Collapse: n=162 RMSE 74.59 (pred 198 vs actual 135)
- Onset+collapse = 3% of hours, **54.7% of SSE**
- January RMSE 33.07 (8.7% of hours, 21.6% of SSE) · JJA RMSE 14.03
- Hour 20 RMSE 31.93; **non-onset hour 20 RMSE 14.67** (7 onset hours RMSE 196)
- Worst row: 2014-04-09 20:00 actual 580 pred 83 lag1 80
- Val is the composite bottleneck (22.397 vs test 20.945)

## This fire
- **Exp33 DISCARD** Rashmi 2015 DART (`boosting_type=dart`). Val 25.869 test 24.569. Early stopping unavailable; all 2000 trees ran. Worse than predicted failure band.
- **Exp34 DISCARD** Huber (`lgb_objective=huber`, default alpha 0.9). Val 80.885 test 81.461. Default alpha is ~100× too small on µg/m³ scale.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART (incl. drop_rate/max_drop/skip_drop), default Huber/mae/tweedie/quantile without explicit scale, `is_heating`

## Process
LightGBM **8/50**. Isolation holds. Champion unchanged.

## Next pasteable
Stay on LightGBM L2 + gbdt. One paper change: Geurts extra_trees=True, **or** Ke `min_data_in_leaf=100`. Do not start CatBoost/MLP. Do not retune DART/Huber nearby HPs.
