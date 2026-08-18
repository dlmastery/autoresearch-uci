# Autoresearch checkpoint — after Exp40 (still Exp30)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## Champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persistence **+6.15%**
- recipe: num_leaves 63, lr 0.01, feature_fraction 0.8, bagging_fraction 0.6, L2 gbdt, 1h nowcast
- features: base + `pm25_delta1` + `inversion_spread`

## Residual (this fire: haze / rain / persist-6)
- Haze actual≥150: n=1638 **model 35.50 vs persist-1 35.31** (zero 1h episode skill)
- Rain n=260 model 23.26 vs persist-1 27.27 (meteorology helps)
- Onset n=83 model 110.05 vs persist-1 107.80
- January 33.07 vs JJA 14.03 · Hour 20 31.93
- Val is the 1h bottleneck (22.397 vs test 20.945)
- **Persist-6** on the same 7950 rows: RMSE **61.83** (Jan 95.60, JJA 40.26)

## This fire
- **Exp39 DISCARD** (1h gate) / **t+6 success**: as-of-t-6 features, same y/split. Test **55.32** vs persist-6 **61.83** (skill **+10.5%**). Val 58.72. January 85.24 vs p6 95.60. Do not mix with 1h composite.
- **Exp40 DISCARD** vent_index=Iws×inversion. Test 20.939 (tiny win) val 22.439. Redundant.

## Exhausted / closed
- Do not retry depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}
- Axis closed: GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, pm25_accel, vent_index, treating t+6 RMSE as a 1h KEEP

## Process
LightGBM **14/50**. Isolation holds. Champion unchanged.
Side ladder: `data/features_horizon6.csv` (same 37596 rows). live_exp now accepts `--data-path`.

## Next pasteable
Hillclimb **t+6** from the Exp39 recipe as a separate composite (vs persist-6 61.83), or stop 1h shaving. Do not start CatBoost/MLP. Do not retry vent_index / accel / linear_tree.
