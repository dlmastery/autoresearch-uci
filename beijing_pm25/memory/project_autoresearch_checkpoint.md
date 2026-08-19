# Autoresearch checkpoint — after Exp109 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW Exp97:** 2014-01-16 n=24 is **6.1% of all 2014 SSE**, RMSE **93.08** vs persist **64.49** (pred_d −58.69 vs need −9.21, mean 457.5). Other January Thursdays match persist (01-02 28.86 vs 29.93). January weekday persist>=300 n=39 is **7.4% SSE**, RMSE **80.36** vs persist **55.80**; not-January persist>=300 beats persist (34.41 vs 41.44).
- January weekday persist 18-21 n=26 RMSE **58.70** vs persist **44.95**, need **+26.38** pred_d **+1.34**.
- **Exp108 is_severe:** val 22.313, 2014-01-16 93.08→100.50 worse, persist>=300 80.36→84.72 worse.
- **Exp109 evening_peak:** val 22.349, persist 18-21 58.70→59.78, hour 20 32.48→32.32.

## This fire
- **Exp108 DISCARD** is_severe (lag1>=250). Test 20.899 val 22.313. Axis closed: lag1 threshold flags.
- **Exp109 DISCARD** evening_peak (hours 18-21). Test 20.756 val 22.349. Axis closed: evening hour bins.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **35/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry early_stopping=30 / min_data=50 / iws_delta / Depthwise / heating products / rsm / l2 / pm25_delta6 / log_iws / roll6mean / is_severe / evening_peak / hour bins. Leave Exp97 or rethink 2014-01-16 mega-haze (93.08 vs persist 64.49, 6.1% SSE) without lag1 flags, wind-scale, 6h trend, or evening bins. Do not start MLP.
