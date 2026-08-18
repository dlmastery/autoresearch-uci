# Autoresearch checkpoint — after Exp54 (1h still Exp30; t+6 recipe Exp47)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 47** LightGBM num_leaves **31** + **month_sin** · test **55.059** · val **58.138**
- vs persist-6 **61.83** skill **+10.9%** (1h-file lag6). Causal horizon6 `pm25_lag1` persist RMSE **63.16**.
- data: `features_horizon6.csv`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 (loses to persist-1 107.80)
- **Exp47 new slices:** 76.3% of hours closer to climatological mean 98 than persist is. need+100 n=286 predicted increment **+21 vs needed +146**. cbwd_NE skill only +5.9%.
- **Exp53 residual recon:** corr 0.990 with Exp47, need+100 still +21.9, tail 102.20 vs persist 99.10
- **Exp54 Tweedie:** test 54.79 (better) val 58.67 (miss). Tail **worse**: actual≥200 **105.44**, need+100 increment **+16.5**

## This fire
- **Exp53 DISCARD** persist-6 residual target. Val 58.684 test 55.044. Axis closed: redundant with persist as a feature.
- **Exp54 DISCARD** Tweedie objective. Val 58.672 test 54.790. Axis closed: helped clean hours, hurt haze tail.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6, persist-6 residual target, Tweedie (no poisson/gamma nearby)

## Process
LightGBM **28/50**. Isolation holds. 1h champion unchanged. t+6 target/loss rethinks stalled.

## Next pasteable
Stay on **Exp47**. Snapshot `lightgbm_t6` or add causal issue-time **Iws_delta** (Iws[t-6]−Iws[t-7]). Do not retry residual/Tweedie/poisson/lr/ff. Do not shave 1h HPs. Do not start CatBoost/MLP until LGB 50 or snapshot.
