# Autoresearch checkpoint — after Exp80 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- vs persist-6 **61.83** skill **+12.2%**
- snapshot: `code_versions/lightgbm_t6/` and `code_versions/lightgbm_final/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val is the bottleneck
- **NEW Exp78:** January persist>=150 typical n=149 RMSE **40.32** vs Exp30 **31.84** / persist **20.81**, pred **−13.0** vs need **−0.8**. Hour 10 RMSE **25.23** vs Exp30 **21.40**. January hour 22 **46.37** vs **34.49**.
- **Exp79 lr=0.01:** Jan typical 37.55 / pred −11.4 (right way); val **22.587** worse.
- **Exp80 depth=4:** Jan typical 36.10 / pred −9.6; onset 108.81 beat Exp30; val **22.795** worse (JJA tax).

## This fire
- **Exp79 DISCARD** CatBoost Plain lr=0.01. Val 22.587 test 21.040. Axis closed: shrink 0.01.
- **Exp80 DISCARD** CatBoost Plain depth=4. Val 22.795 test 21.057. Axis closed: depth 4. Best CatBoost remains Exp78 Plain depth6 lr0.03 (NEAR-MISS 22.472).

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4. Do not retry those.
- t+6: (unchanged closed list) · open recipe Exp76. persist>=250 typical still open.

## Process
LightGBM **50/50 complete**. CatBoost **6/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76.

## Next pasteable
Best CatBoost is still **Exp78 Plain depth6 lr=0.03**. Next: **l2_leaf_reg** or **CatBoost t+6** on Exp76 features. Do not retry Ordered / lr 0.01 / depth 4. Do not start MLP. Do not mix t+6 val with the 1h composite.
