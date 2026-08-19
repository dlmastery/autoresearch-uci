# Autoresearch checkpoint — after Exp126 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 126** MLP dropout 0.3 · test **20.483** · val **22.729**
- MLP val recipe remains **Exp 125** · test 20.648 · val **22.623** · January 31.02

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** MLP val-test gap **1.975** vs CatBoost **1.432**. February 24.09→25.56 and April 27.06→28.86 ate Exp125's January win (34.84→31.02). 2013 February persist **38.30** vs 2014 **26.01**.
- **Exp126 DISCARD** dropout=0.3. Val **22.729** (worse). Test **20.483** (best 2014). April 28.86→**26.61**. February 25.56→25.47 still vs Exp97 24.09.

## This fire
- **Exp126 DISCARD** MLP dropout 0.3. Test-win val-loss worse. Axis closed: dropout 0.3/0.4. MLP **2/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **2/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp125 recipe** (dropout 0.2). Regularize 2013 val with **width or weight_decay**, not another dropout. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
