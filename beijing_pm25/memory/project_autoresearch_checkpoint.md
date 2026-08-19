# Autoresearch checkpoint — after Exp96 KEEP (1h now Exp96 CatBoost; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 96** CatBoost Plain · composite **−22.357** · 2014 test RMSE **20.881** · 2013 val **22.357**
- skill vs persist-1 **+6.43%** · 1h noise floor val ±0.08
- Features: Exp30 inversion+delta + rh_magnus + dewp_delta · depth 6 · lr 0.03 · l2=3 · Plain
- Prior champion Exp30 LightGBM: test 20.945 · val 22.397 · composite −22.397

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW Exp96:** Jan 34.94 vs persist 33.58 (still loses). Hour-1 29.82 vs persist 28.19. Hour 20 32.51 vs persist 33.24 (beats persist, worse than Exp30 31.93). Onset n=83 RMSE 110.32 vs persist 107.80. Friday 24.03 now beats persist 24.13 (Exp91 lost 24.81). dewp-rise persist>=150 36.47 vs persist 35.88 (tiny). Val still the bottleneck (22.357 vs test 20.881).

## This fire
- **Exp96 KEEP** dewp_delta on Exp91. Val 22.357 test 20.881 composite −22.357. First 1h KEEP since Exp30. New 1h champion is CatBoost.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h (pre-KEEP): Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **22/50**. Isolation holds. **1h champion is now Exp96 CatBoost.** t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp96**. Diagnose January / hour-1 leftovers. Do not retry rsm=0.6 / l2=10 / month_sin / accel / Lossguide / cbwd_prev_SE / random_strength=5. Do not start MLP.
