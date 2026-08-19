# Autoresearch checkpoint — after Exp124 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW:** cv persist>=150 n=505 is **12.4%** of 2014 SSE, RMSE **28.95** vs persist **27.68**, need +1.28 pred_d **−0.01**. 2013 val cv-dirty persist RMSE **37.95** vs 2014 **27.68**, 2013 need **−0.09** vs 2014 **+1.28**. Mean inversion on that slice 6.36.
- **Exp124 DISCARD** cv_inv. Val **22.250** test **20.754**. cv persist>=150 28.95→**29.44**, pred_d −0.01→**−0.38**.

## This fire
- **Exp124 DISCARD** cv_inv. Test 20.754 val 22.250. Axis closed: calm×inversion. **CatBoost 50/50 complete.**

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws, is_severe, evening_peak, rh_delta, temp_delta, se_iws, pm25_roll3mean, is_janfeb, drop lag13-24, iws_clip100, drop dow, model_size_reg=1.0 (inert), Bernoulli subsample=0.8, border_count=128, nw_iws, is_morning, dow_sin, cv_inv
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
CatBoost **50/50 complete**. Snapshot `catboost_final` from Exp97. Isolate **MLP** (1/50) from Exp97 features on the frozen 2014 test year. Do not mix CatBoost HPs into MLP. Do not retry cv_inv / dow_sin / hour bins / wind×Iws / unused CatBoost regularizer HPs. 1h champion remains Exp97. t+6 recipe remains Exp76.
