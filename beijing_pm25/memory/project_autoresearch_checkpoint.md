# Autoresearch checkpoint — after Exp58 (1h still Exp30; t+6 recipe Exp56)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 56** LightGBM num_leaves **31** + **month_sin** + **pres_delta** + **dewp_delta** · test **54.487** · val **57.658**
- vs persist-6 **61.83** skill **+11.9%**
- data: `features_horizon6.csv`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 (loses to persist-1 107.80)
- **Exp56 new slices:** dur6 increment already calibrated (−42.20 vs −41.94). dur3-5 under-cleans (−10.77 vs −23.53). Late 21–23 RMSE 64.57. Sunday need −9.01 pred +2.43. cv-onset n=290 RMSE 100.25. Val gap 3.17.
- **Exp57:** dur3-5 increment unchanged (−10.75). Redundant with six lags.
- **Exp58:** val 57.704 test 54.540, gap not shrunk.

## This fire
- **Exp57 DISCARD** haze_hours6. Val 57.864 test 54.385. Axis closed: episode-count.
- **Exp58 DISCARD** reg_lambda=1. Val 57.704 test 54.540. Axis closed: L2=1.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual, Tweedie, Iws_delta, temp_delta, haze_hours6, reg_lambda=1

## Process
LightGBM **32/50**. Isolation holds. 1h champion unchanged. t+6 recipe remains Exp56.

## Next pasteable
Stay on **Exp56**. Snapshot `lightgbm_t6`. Do not retry haze-count / L2 / temp_delta / Iws_delta. Do not shave 1h HPs. Do not start CatBoost/MLP until LGB 50 or snapshot.
