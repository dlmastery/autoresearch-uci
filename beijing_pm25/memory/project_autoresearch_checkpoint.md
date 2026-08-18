# Autoresearch checkpoint — after Exp46 (1h still Exp30; t+6 recipe Exp46)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%**
- recipe: num_leaves 63, lr 0.01, ff 0.8, bag 0.6, bagging_freq 0, seed 0
- features: base + `pm25_delta1` + `inversion_spread`

## t+6 side ladder (do not mix composites)
- **Exp 46** LightGBM num_leaves **31** · test **55.337** · val **58.365**
- vs persist-6 **61.83** skill **+10.5%**
- vs Exp39 (63 leaves): val 58.724→**58.365** (side KEEP), test flat 55.32→55.34
- data: `features_horizon6.csv` (same 37596 rows / 7950 test timestamps)

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · val bottleneck
- **t+6 Exp39 slices:** 6h onsets n=978 RMSE 92.99, **bias −72.8** · calm Iws@t-6 skill **+7.1%** vs windy **+14.6%** · Jan 85.24 vs JJA 36.33 · H20 64.23
- 1h noise floor still val ±0.08

## This fire
- **Exp45 DISCARD** t+6 + pm25_delta6. Test 55.486 val 58.710. Redundant. Axis closed for 6h diffs.
- **Exp46 1h-DISCARD / t+6 side-KEEP** num_leaves 31. Val 58.365 test 55.337.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin=127, roll6max, bagging_freq=1, seed, treating t+6 RMSE as a 1h KEEP
- t+6: pm25_delta6 / nearby 6h diffs

## Process
LightGBM **20/50**. Isolation holds. 1h champion unchanged.
`live_exp.py --data-path` now composes with `--add-feature`.

## Next pasteable
Hillclimb t+6 from **Exp46** (31 leaves) vs persist-6. Do not shave 1h HPs inside val ±0.08. Do not start CatBoost/MLP.
