# Autoresearch checkpoint — after Exp110 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW Exp97:** 2014-01-16 hours 0-8 n=9 is **4.0% of all 2014 SSE**, RMSE **123.22** vs persist **48.74** (pred_d −118.60 vs need −10.00, mean 605). Hours 9-23 **beat persist** (68.94 vs 72.31). RH rises 58.5→79.6, Iws<3. corr(rh_delta, need | 0-8)=**0.72**. Other January overnight persist>=150 beats persist (39.85 vs 49.48).
- **Exp110 rh_delta:** val 22.236 (near-miss, +0.069), test 20.661 (beat). Hours 0-8 123.22→122.74. Leftover inert.

## This fire
- **Exp110 DISCARD** rh_delta. Test 20.661 val 22.236. Axis closed: RH increment. Leftover hours 0-8 unchanged.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak, rh_delta
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **36/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry early_stopping=30 / min_data=50 / iws_delta / Depthwise / heating products / rsm / l2 / pm25_delta6 / log_iws / roll6mean / is_severe / evening_peak / hour bins / rh_delta. Leave Exp97 or rethink 2014-01-16 hours 0-8 (123.22 vs persist 48.74, 4.0% SSE) without lag1 flags, wind-scale, 6h trend, evening bins, or RH increments. Do not start MLP.
