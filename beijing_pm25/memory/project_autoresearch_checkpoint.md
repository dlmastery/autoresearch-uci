# Autoresearch checkpoint — after Exp48 (1h still Exp30; t+6 recipe Exp47)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 47** LightGBM num_leaves **31** + **month_sin** · test **55.059** · val **58.138**
- vs persist-6 **61.83** skill **+10.9%**
- vs Exp46: val 58.365→58.138, test 55.337→55.059 (side KEEP)
- data: `features_horizon6.csv` (same 37596 rows / 7950 test timestamps)

## Residual (this fire, Exp46 then Exp47)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05
- **t+6 Exp46:** Jan 85.76 · JJA 36.55 · H20 64.72 · Jan eve 18–21 n=116 RMSE **100.90**
- 6h onsets n=978 RMSE 93.62 bias −73.8 · calm+onset6 n=408 bias −76.4
- Exp47 Jan eve still **101.69** (month_sin aliases Jan/May)

## This fire
- **Exp47 1h-DISCARD / t+6 side-KEEP** month_sin. Val 58.138 test 55.059.
- **Exp48 1h-DISCARD / t+6 side-MISS** month_cos. Test **54.648** (best t+6 test) val 58.359 (lost). Axis closed for month_cos.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- t+6: pm25_delta6, month_cos / extra calendar dummies

## Process
LightGBM **22/50**. Isolation holds. 1h champion unchanged.

## Next pasteable
Hillclimb t+6 from **Exp47** (31 leaves + month_sin). Attack **calm 6h-onsets** (n=408, bias −76), not another season column. Do not shave 1h HPs. Do not start CatBoost/MLP.
