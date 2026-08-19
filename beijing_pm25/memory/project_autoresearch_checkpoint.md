# Autoresearch checkpoint — after Exp97 KEEP (1h now Exp97 CatBoost; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain
- Prior: Exp96 −22.357 / Exp30 −22.397

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW Exp96:** Jan RH>=70 n=84 RMSE **38.25** vs persist **23.94** (skill −59.8%). Jan Iws<2 **34.91** vs persist **29.42**. Jan hour-1 **76.95** vs persist **69.40** (need +8.32 pred_d −5.35). Hour-1 outside January **20.63 ≈ persist 20.60**.
- **Exp97 is_heating:** Jan RH>=70 **36.68** (missed 24–32). Jan **34.84** still vs persist **33.58**. Jan hour-1 **74.63**. JJA **13.84** (improved, no summer tax). Val still bottleneck (22.167 vs test 20.735).

## This fire
- **Exp97 KEEP** is_heating on Exp96. Val 22.167 test 20.735 composite −22.167. New 1h champion.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h (pre-KEEP): Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2
- is_heating is now IN the champion (LGB 1h try is closed; CatBoost KEEP)
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **23/50**. Isolation holds. **1h champion is Exp97 CatBoost.** t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Diagnose January RH>=70 leftover (36.68 vs persist 23.94). Do not retry month_sin / rsm / l2 / wind dummy / random_strength=5. Do not start MLP.
