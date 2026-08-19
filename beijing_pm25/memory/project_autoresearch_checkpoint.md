# Autoresearch checkpoint — after Exp92 (1h still Exp30; t+6 recipe Exp76)

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
- **NEW Exp78:** PRES<1010 persist>=150 n=273 RMSE **31.25** vs Exp30 **27.53** / persist **30.51**. Hour-22 persist>=100 **30.49** vs **26.42**.
- **Exp91 rh_magnus:** val **22.449** (best CatBoost val, 0.052 from Exp30). Low-PRES dirty **29.82**. Test 21.045.
- **Exp92 RH+l2=10:** val **22.596** worse; test **20.822** beat Exp30; low-PRES **28.20**.

## This fire
- **Exp91 DISCARD** (NEAR-MISS) rh_magnus. Val 22.449 beat Exp78 22.472, missed Exp30 22.397. Bomb HIT. New CatBoost val recipe.
- **Exp92 DISCARD** RH+l2=10. Val 22.596 test 20.822. Axis closed: l2 on RH recipe.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **18/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76. Best CatBoost 1h val is **Exp91** rh_magnus (22.449).

## Next pasteable
Stay isolated on **CatBoost Exp91** (Plain + rh_magnus). Do not retry l2=10 / month_sin / accel / Lossguide. Next: a different unused CatBoost knob (border_count / rsm need wrapper) or leave the 0.052 NEAR-MISS. Do not start MLP.
