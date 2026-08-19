# Autoresearch checkpoint — after Exp127 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 126** MLP dropout 0.3 · test **20.483** · val **22.729**

## MLP val recipe (not 1h champion)
- **Exp 127** MLP wd=1e-4 · val **22.528** · test **20.773** · January **30.82**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** collapse n=162 MLP 78.82 vs CatBoost 74.05 vs persist 97.87, pred_d **−22.24** vs CB **−24.95** vs need **−86.31**. December 21.58 vs CB 21.02. Hour 1 27.90 beats persist 28.19.
- **Exp127 DISCARD** (1h gate) wd=1e-4. Val **22.528** beat Exp125 22.623. Test 20.773. Collapse 78.82→**81.47**. January 31.02→**30.82**.

## This fire
- **Exp127 DISCARD** 1h vs Exp97. MLP-side val KEEP vs Exp125. MLP **3/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **3/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp127 recipe** (dropout 0.2, weight_decay 1e-4). Shrink **width** next (not dropout 0.4, not wd 1e-3). Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
