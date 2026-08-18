# Autoresearch checkpoint — after Exp36 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, boosting_type gbdt, L2, min_data_in_leaf 20, extra_trees off
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (this fire: wind / Iws / January clock)
- Onset actual−lag1>50: n=83 RMSE **110.05** (pred 171 vs actual 259)
- January RMSE 33.07 vs JJA 14.03
- **January evening 18–21:** n=116 RMSE **42.61** vs January day 10–16 RMSE 23.57
- SE-wind onsets: 38/83, RMSE **131.89** (worst sector)
- Windy Iws tercile onsets: n=19 RMSE **163.64**; calm onsets n=38 RMSE 77.09
- Hour 20 RMSE 31.93
- Val is the composite bottleneck (22.397 vs test 20.945)

## This fire
- **Exp35 DISCARD** Geurts extra_trees=True. Val 22.989 test 21.238. Random thresholds hurt 2013.
- **Exp36 DISCARD** Ke min_data_in_leaf=100. Val 22.662 test 21.127. Larger leaves underfit.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART, default Huber/mae/tweedie/quantile, `is_heating`, extra_trees, min_data_in_leaf=100

## Process
LightGBM **10/50**. Isolation holds. Champion unchanged.

## Next pasteable
Stay on LightGBM L2 + gbdt + greedy splits. One paper change: Shi `linear_tree=True`. If that DISCARDs, rethink to a new onset feature (not is_heating / weather lags / raw hour) or t+6. Do not start CatBoost/MLP.
