# Autoresearch checkpoint — after Exp107 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW Exp97:** Jan Thursday persist>=150 n=47 is **6.8% SSE**, RMSE **70.42** vs persist **50.96** (pred_d −27.05 vs need −4.17). Mean Iws **4.13** vs **10.14** on other Jan weekday persist hours. Mean actual **343.8**.
- Jan weekday persist>=150 delta6>20 n=92 is **10.1% SSE**, RMSE **61.11** vs persist **43.87** (pred_d −17.76 vs need −1.91). Hours 18-21 persist n=26 need **+26.38** pred_d **+1.34**.
- **Exp106 pm25_delta6:** val 22.345, leftover 61.11→60.16, Thursday 70.42→72.21 worse.
- **Exp107 log_iws:** val 22.310, Thursday 70.42→72.35, Iws<5 persist 56.88→58.75 worse.

## This fire
- **Exp106 DISCARD** pm25_delta6. Test 20.671 (beat) val 22.345 (miss). Axis closed: 6h episode trend.
- **Exp107 DISCARD** log_iws. Test 20.783 val 22.310. Axis closed: Iws log-scale.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, Depthwise, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert), rh_iws, heating_build, pres_delta, min_data_in_leaf=20 (inert), early_stopping=50 (inert), pm25_delta6, log_iws
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **33/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry early_stopping=30 / min_data=50 / iws_delta / Depthwise / heating products / rsm / l2 / pm25_delta6 / log_iws / roll6mean. Leave Exp97 or rethink January Thursday persist>=150 (70.42 vs persist 50.96, Iws 4.13, mean 343.8) without another wind-scale or 6-hour trend. Do not start MLP.
