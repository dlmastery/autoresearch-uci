# Autoresearch checkpoint — after Exp111 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW Exp97:** 2014-01-16 hours 0-8 not-NW n=6 is **3.3% SSE**, RMSE **137.65** vs persist **42.70** (need +9.33 pred_d −120.74). cv subset n=3 RMSE **151.75** vs persist **52.38**. Other January overnight persist and cv persist>=300 hours 0-8 excluding Jan 16 **match or beat persist**. January onset n=18 is **10.3% SSE**, RMSE **139.91** vs persist **127.93**. Hour 20 need +7.65 pred_d +4.96.
- **Exp111 temp_delta:** val 22.357, hour 20 32.48→32.50, Jan16 hours 0-8 123.22→128.48 worse.

## This fire
- **Exp111 DISCARD** temp_delta. Test 20.715 val 22.357. Axis closed: extra weather increments (pres/rh/temp).

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak, rh_delta, temp_delta
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **37/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry early_stopping=30 / min_data=50 / iws_delta / Depthwise / heating products / rsm / l2 / pm25_delta6 / log_iws / roll6mean / is_severe / evening_peak / hour bins / rh_delta / temp_delta / extra weather increments. Leave Exp97 or rethink January onset (n=18, 10.3% SSE, RMSE 139.91 vs persist 127.93) without lag1 flags, wind-scale, 6h trend, evening bins, RH increments, or extra weather deltas. Do not start MLP.
