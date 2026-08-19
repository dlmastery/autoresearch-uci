# Autoresearch checkpoint — after Exp99 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW Exp97:** Jan RH>=70 all have Ir=0. Jan RH>=70 Iws<2 n=45 RMSE **42.65** vs persist **22.94** (skill −85.9%). Jan RH>=70 hours 0-5 n=37 RMSE **38.33** vs persist **18.85** (skill −103.4%). JJA RH>=70 Ir=0 is fine (14.93 vs persist 15.75).
- **Exp98 heating_night:** hours 0-5 38.33→37.60; Iws<2 worsened 42.65→44.31.
- **Exp99 bagging_temperature=2:** bit-identical to Exp97.

## This fire
- **Exp98 DISCARD** heating_night. Val 22.343. Axis closed: winter-night product.
- **Exp99 DISCARD** bagging_temperature=2. Bit-identical. Axis closed: T=2 inert on 1h Plain.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4, Lossguide, month_sin, pm25_accel, l2=10 on RH, rsm=0.8, cbwd_prev_NW, random_strength=2, heating_night, bagging_temperature=2 (inert)
- is_heating is IN the champion
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76

## Process
LightGBM **50/50 complete**. CatBoost **25/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost Exp97**. Do not retry heating_day / bagging_temperature=5 / month_sin / rsm / l2 / wind dummy. January RH>=70 Iws<2 leftover (42.65 vs persist 22.94) needs a non-clock non-bootstrap rethink. Do not start MLP.
