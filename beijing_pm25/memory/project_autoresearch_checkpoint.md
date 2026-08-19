# Autoresearch checkpoint — after Exp82 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- vs persist-6 **61.83** skill **+12.2%**
- CatBoost t+6 Exp81 test **53.929** / val **57.857** (test win, val miss)
- snapshot: `code_versions/lightgbm_t6/` and `code_versions/lightgbm_final/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val bottleneck
- **NEW Exp76:** Saturday typical n=830 RMSE **39.80** vs persist-6 **24.07** (skill **−65.4%**), need +3.3, pred +5.6. Hour 22 worst **64.43**.
- **Exp81:** Sat typical **36.78**; February **71.69** beat 78.50; test **53.929** beat 54.312; val **57.857** miss
- **Exp82:** Sat typical **36.85** flat; val **58.159** worse

## This fire
- **Exp81 DISCARD** CatBoost Plain t+6. Val 57.857 test 53.929. Side-MISS. Saturday RMSE improved.
- **Exp82 DISCARD** CatBoost t+6 l2_leaf_reg=10. Val 58.159 test 53.895. Axis closed: t+6 leaf L2=10.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4
- CatBoost t+6: l2_leaf_reg=10
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **8/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost**. Best 1h CatBoost is Exp78 Plain depth6 lr=0.03 (NEAR-MISS). CatBoost t+6 wins 2014 test and loses 2013 val. Next: **bagging_temperature** or a t+6 feature rethink, not another leaf L2 / 1h lr / depth / Ordered. Do not start MLP. Do not mix t+6 val with the 1h composite.
