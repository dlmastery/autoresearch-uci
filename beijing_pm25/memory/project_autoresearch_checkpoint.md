# Autoresearch checkpoint — after Exp52 (1h still Exp30; t+6 recipe Exp47)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 47** LightGBM num_leaves **31** + **month_sin** · test **55.059** · val **58.138**
- vs persist-6 **61.83** skill **+10.9%**
- data: `features_horizon6.csv`

## Residual (this fire, Exp47)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **t+6 mean-reversion:** low-actual bias **+30.3** (pred 51 vs act 21); high-actual bias **−34.0**
- **actual≥200 n=944:** model RMSE **101.22 LOSES to persist-6 97.12** (bias −66.6)
- lag6≥150 n=1627 skill **+15%**, bias ≈ 0 (OK once episode is on)
- Night 00–05 55.81 vs day 10–16 52.52 · H20 64.46 · Jan 85.53 vs JJA 36.70

## This fire
- **Exp51 DISCARD** t+6 lr 0.02. Val 58.302 test 55.154. Tail RMSE still 101.35. Axis closed for faster eta.
- **Exp52 DISCARD** t+6 feature_fraction 0.6. Val 58.323 test 55.053. Axis closed for ff 0.6.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: delta6, month_cos, stagn_index, path_smooth=1, lr 0.02, feature_fraction 0.6

## Process
LightGBM **26/50**. Isolation holds. 1h champion unchanged. t+6 local HPs are stalling.

## Next pasteable
Stay on **Exp47**. Rethink: persist-6 residual target, or snapshot `lightgbm_t6` and keep filling the 50. Do not retry lr/ff nearby. Do not shave 1h HPs. Do not start CatBoost/MLP until LGB 50 or snapshot.
