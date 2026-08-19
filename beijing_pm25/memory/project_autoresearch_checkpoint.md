# Autoresearch checkpoint — after Exp95 (1h still Exp30; t+6 recipe Exp76)

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
- **NEW Exp91:** PRES>=1025 persist>=150 n=413 RMSE **44.27** vs Exp30 **41.59** / persist **40.56** (skill −9.1%). Over-cleans pred_d **−12.2** vs need **−3.2**. No-NW subset n=277 RMSE **43.72** vs persist **38.64**.
- **Exp94 cbwd_prev_NW:** hiP dirty **43.36** (in 40–43); no-NW stagnant **43.66** flat vs 43.72. Dummy helped previous-NW hours 45.37→42.75 (wrong hours).
- **Exp95 random_strength=2:** hiP dirty **43.89** missed 40–43.5. Val **22.451** vs Exp91 **22.449** (inert).

## This fire
- **Exp94 DISCARD** cbwd_prev_NW. Val 22.528 test 21.063. Axis closed: previous-direction dummy.
- **Exp95 DISCARD** random_strength=2. Val 22.451 test 21.005. Axis closed: 1h split-score noise. Best CatBoost val remains Exp91 22.449.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **21/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76. Best CatBoost 1h val is **Exp91** rh_magnus (22.449).

## Next pasteable
Stay isolated on **CatBoost Exp91**. Do not retry rsm=0.6 / l2=10 / month_sin / accel / Lossguide / cbwd_prev_SE / random_strength=5. Leave the 0.052 NEAR-MISS or bagging_temperature on 1h (wired, t+6 inert). Do not start MLP.
