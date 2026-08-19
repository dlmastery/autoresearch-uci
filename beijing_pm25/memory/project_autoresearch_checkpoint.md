# Autoresearch checkpoint — after Exp88 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- Best CatBoost t+6 val: Exp85 Ordered test 53.940 / val 57.658 (side-MISS)

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val bottleneck
- **NEW Exp78:** hour-10 persist>=150 n=70 RMSE **48.03** vs Exp30 **38.25** / persist **40.22**. Hour-10 collapses n=6 pred **+2.2** vs need **−113.7**. Hour-10 Iws>=5 **33.13** vs **26.19**.
- **Exp87 Lossguide:** hour-10 persist>=150 **52.60** worse; collapse pred **+9.4**.
- **Exp88 l2=10:** hour-10 persist>=150 **39.21** (bomb HIT); collapse pred **−14.3**; test **20.802** beat Exp30; val **22.488** miss.

## This fire
- **Exp87 DISCARD** grow_policy=Lossguide. Val 22.476 test 21.188. Axis closed: Lossguide on 1h.
- **Exp88 DISCARD** l2_leaf_reg=10. Val 22.488 test **20.802**. Bomb HIT. Best CatBoost 1h test. Val still gate. Best CatBoost val remains Exp78 22.472.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **14/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost**. Best 1h CatBoost val is Exp78 (22.472 NEAR-MISS). Best 1h CatBoost test is Exp88 l2=10 (20.80). Next: **do not retry l2=20 / Lossguide**. Feature rethink on Exp78 or leave the NEAR-MISS. Do not start MLP.
