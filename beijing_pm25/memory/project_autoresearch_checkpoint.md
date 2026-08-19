# Autoresearch checkpoint — after Exp93 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val bottleneck
- **NEW Exp91:** hour 10 RMSE **23.95** vs Exp30 **21.40** / persist **22.86**. Hour 22 **20.95** vs persist **20.19**. January cv **32.53** vs persist **26.72**.
- **Exp93 rsm=0.8:** hour 10 **23.27**; test **20.945** ties Exp30; val **22.569** worse than Exp91 22.449.

## This fire
- **Exp93 DISCARD** rsm=0.8. Val 22.569 test 20.945 (tie Exp30). Axis closed: rsm=0.8. Best CatBoost val remains Exp91 22.449.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH, rsm=0.8
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **19/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76. Best CatBoost 1h val is **Exp91** rh_magnus (22.449).

## Next pasteable
Stay isolated on **CatBoost Exp91**. Do not retry rsm=0.6 / l2=10 / month_sin / accel / Lossguide. Leave the 0.052 NEAR-MISS or a non-subsample rethink. Do not start MLP.
