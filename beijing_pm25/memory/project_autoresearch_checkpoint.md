# Autoresearch checkpoint — after Exp50 (1h still Exp30; t+6 recipe Exp47)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 47** LightGBM num_leaves **31** + **month_sin** · test **55.059** · val **58.138**
- vs persist-6 **61.83** skill **+10.9%**
- data: `features_horizon6.csv` (same 37596 rows / 7950 test timestamps)

## Residual (this fire, Exp47)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **t+6:** Jan 85.53 · JJA 36.70 · H20 64.46 · onset6 n=978 RMSE 93.51 bias −73.3
- High-stagn tercile skill **+7.7%** (RMSE 60.92) vs ventilated **+16.1%** (48.54)
- **cv+onset6 n=286 RMSE 102.43** bias −80.4 (worst wind sector)
- Iws<1 onset6 n=193 bias −77.7 · val gap 3.08

## This fire
- **Exp49 DISCARD** t+6 stagn_index=inversion/(Iws+1). Test 55.065 val 58.626. Redundant. Axis closed for Iws-inversion ratios.
- **Exp50 DISCARD** t+6 path_smooth=1. Test 55.090 val 58.259. Did not shrink the val gap.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: pm25_delta6, month_cos, stagn_index / Iws-inversion ratios, path_smooth=1

## Process
LightGBM **24/50**. Isolation holds. 1h champion unchanged.

## Next pasteable
Stay on **Exp47**. Next t+6 change: lr 0.02 (not the exhausted 0.05/0.005) or accept calm-onset bias as 6h-hard. Do not retry stagn ratios or path_smooth. Do not shave 1h HPs. Do not start CatBoost/MLP.
