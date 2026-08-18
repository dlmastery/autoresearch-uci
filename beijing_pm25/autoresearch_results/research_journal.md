# Research journal — 28-experiment hill-climb

Karpathy rule: modify one thing, keep if the composite rose, otherwise revert. Test year 2014 never moved.

## The ladder

persistence (2014) test RMSE 22.316

**Exp1 KEEP** C&G 2016 XGBoost → 21.768. First floor. Skill +2.5%. Residuals: spike hours RMSE 37, hour 20 RMSE 32.

**Exp2 KEEP** max_depth 4. Test 21.996 (worse) but val 23.205 (better). Composite rose because val was the min(). Gate working.

**Exp4 KEEP** lr 0.01. More shrinkage on the depth-4 tree.

**Exp8 KEEP** subsample 0.6. Stochastic rows.

**Exp14 KEEP** inversion_spread = TEMP−DEWP (Liang 2015 ventilation). First real test-RMSE drop (21.823).

**Exp15 KEEP** pm25_delta1 = lag1−lag2. Onset momentum. Test 21.290.

**Exp22 KEEP** stack inversion onto delta. Champion. Test **21.122**, val **22.470**, skill **+5.4%**.

## What was thrown away

21 DISCARDs. Notable near-miss: LightGBM Exp25 test **20.905** — best raw test in the campaign — DISCARD because val 22.711 lost to Exp22 val 22.470.

Depth 8/5/3, lr 0.05/0.005, weather lags, raw hour, extra trees, L1/L2, CatBoost: no composite gain.

## Next

1-hour HP surface is locally flat. Next axis: t+6 on the same frozen 2014 timestamps.
