# Autoresearch checkpoint — after Exp125 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 125** MLP default · test **20.648** · val **22.623** · January **31.02** (beats persist 33.58)

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** typical |need|<=10 n=5117 RMSE **8.35** vs persist **5.08** (trees over-adjust). |need|>=30 n=689 beats persist 59.01 vs 67.57. persist>=q67 is **67.1%** of SSE. corr(|need|,|err|)=**0.866**.
- **Exp125 DISCARD** MLP default. Val **22.623** test **20.648**. Typical 8.35→**7.28**. January 34.84→**31.02**. Onset 110.06→109.53.

## This fire
- Snapshot `code_versions/catboost_final`.
- **Exp125 DISCARD** MLP 256-128-64 dropout 0.2. Test-win val-loss. MLP **1/50**.

## Exhausted / closed
- 1h tree HPs and CatBoost 50/50 as in prior checkpoint
- Do not retry CatBoost products/regularizers on the MLP cycle

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **1/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp125 recipe** (not the 1h champion). Regularize 2013 val (dropout / width / weight_decay / epochs). Do not mix CatBoost HPs. Do not retry tree features. 1h champion remains Exp97 until MLP composite beats −22.167.
