# Autoresearch checkpoint — after Exp128 (1h still Exp97; t+6 recipe Exp76)

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
- **NEW:** hour 21 persist>=150 n=65 MLP **58.72** vs CatBoost **50.21** vs persist **56.30**, need **+1.72** pred_d **+5.15**. |need|>=80 n=82 is **46.5%** of Exp127 SSE vs 41.3% of Exp97, RMSE **139.40** vs CB **131.19**, pred_d **−16.53** vs CB **−27.85**. April 29.24 vs CB 27.06.
- **Exp128 DISCARD** hidden 128-64-32. Val **23.080** missed Exp127 22.528. Test 21.344. Hour-21 persist>=150 58.72→**64.79**. |need|>=80 139.40→**143.33**. Typical 7.03→**7.81**.

## This fire
- **Exp128 DISCARD** 1h vs Exp97. Width shrink inverted. MLP val recipe remains Exp127. MLP **4/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **4/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp127 recipe** (hidden 256-128-64, dropout 0.2, weight_decay 1e-4). Change an unused axis next (**Adam lr**, not dropout 0.4, not wd 1e-3, not another width shrink). Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
