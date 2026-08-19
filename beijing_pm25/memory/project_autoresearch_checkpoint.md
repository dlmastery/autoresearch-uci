# Autoresearch checkpoint — after Exp86 (1h still Exp30; t+6 recipe Exp76)

**Updated:** 2026-08-18
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 30** LightGBM · composite **−22.397** · 2014 test RMSE **20.945** · 2013 val **22.397**
- skill vs persist-1 **+6.15%** · 1h noise floor val ±0.08

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**
- Best CatBoost t+6 val: **Exp85 Ordered** test **53.940** / val **57.658** (side-MISS, closest CatBoost val)
- snapshot: `code_versions/lightgbm_t6/` and `code_versions/lightgbm_final/`

## Residual (this fire)
- **1h Exp30:** Jan 33.07 vs JJA 14.03 · H20 31.93 · onset n=83 RMSE 110.05 · pred +0.2 vs need +87.4 · val bottleneck
- **NEW Exp81:** wrong-sign onsets (need>50 and pred<0) n=164 RMSE **129.01** vs persist-6 **100.47**, persist mean **204**, need **+91.5**, pred **−24.9**. Val-test gap **3.93** vs LGB **2.85**.
- **Exp85 Ordered:** val **57.658** (best CatBoost t+6 val); wrong-sign pred **−23.1**; n **172**.
- **Exp86 random_strength=2:** val **57.684** worse; test **54.254** lost to Exp76.

## This fire
- **Exp85 DISCARD** CatBoost Ordered t+6. Val 57.658 beat Exp81 57.857, missed Exp76 57.161. Test 53.940.
- **Exp86 DISCARD** Ordered random_strength=2. Val 57.684 test 54.254. Axis closed: random_strength=2.

## Exhausted / closed
- 1h: depth {3,5,8}, lr {0.05,0.005}, min_child {10,50}, weather lags, raw hour, subsample {0.5,1.0}, GOSS, DART, Huber, is_heating, extra_trees, min_data=100, linear_tree, accel, vent_index, max_bin, roll6max, bagging_freq=1, seed, t+6-as-1h-KEEP
- CatBoost 1h: Ordered, Plain lr=0.01, Plain depth=4
- CatBoost t+6: l2=10, bagging_temperature=2 (inert), drop rh_magnus, random_strength=2
- t+6 LGB recipe remains Exp76. CatBoost t+6 val leader Exp85 Ordered (still MISS).

## Process
LightGBM **50/50 complete**. CatBoost **12/50**. Isolation holds. 1h champion unchanged (Exp30). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **CatBoost**. Best 1h CatBoost is Exp78 Plain. Best CatBoost t+6 val is Exp85 Ordered (57.66, still MISS). Next: **return to 1h Exp78** with a new slice, not another t+6 randomness HP. Do not retry bagging_temperature / l2=10 / drop rh_magnus / random_strength=2 / 1h Ordered / lr 0.01 / depth 4. Do not start MLP.
