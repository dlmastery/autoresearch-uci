# Autoresearch checkpoint — after Exp183 DISCARD (1h remains Exp167 residual MLP; FT 9/50 Pre-LN val recipe Exp178; t+6 recipe Exp76)

**Updated:** 2026-08-21
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 167** MLP residual skips · composite **−21.972** · 2014 test RMSE **20.072** · 2013 val **21.972**
- skill vs persist-1 **+10.06%** · 1h noise floor val ±0.08
- Recipe: Exp136 features + hidden 512-256-128 + residual projection shortcuts · batch 16 · dropout 0.2 · wd=1e-4 · lr 3e-4 · clip=1.0 · layer_norm off · huber_beta=1 · persist_residual off · underpred_weight off
- First 1h KEEP since Exp97. First MLP to beat CatBoost on the frozen 2014 composite.

## Best 2014 test (now the champion)
- **Exp 167** residual MLP · test **20.072** · val **21.972**
- Best non-champion 2014 test: Exp172 stagn_onset **20.018** (val 21.9995 DISCARD near-miss)
- Best FT test: Exp179 dropout=0 **20.509** (val 22.200 DISCARD)
- Best FT val: Exp178 Pre-LN dropout 0.1 batch 32 **22.140** / test **20.674**
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## FT val recipe (isolated, not champion)
- **Exp 178** Pre-LN (norm_first=true) · dropout 0.1 · n_layers 3 · d_model 64 · batch 32 · lr 1e-4 · weight_decay 1e-5 · val **22.140** · test **20.674**
- Exp182 wd=1e-4: val 22.400 / test 20.746 worse. Exp183 lr=3e-4: val 22.477 / test 20.952 worse. Recipe stays Exp178.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp167, computed): January 31.22 vs persist 33.58 · JJA 13.87 vs persist 14.83 · hour 20 32.68 vs persist 33.24 (11.10% of SSE) · onset n=83 RMSE 110.28 vs persist 107.80 (31.51% of SSE; need +87.40 pred_d −0.60). Val 21.972 vs test 20.072 is the bottleneck.
- **NEW:** Ir>0 persist>=50 n=179 RMSE **28.75** vs persist **32.21** (4.62% of SSE; need **−9.08** pred_d **−3.36**). Rain washout under-moves; Exp178 pred_d −1.48 worse.
- **Exp183 DISCARD** FT Pre-LN lr=3e-4. Val **22.477** missed 21.972 and Exp178 22.140 (inside 21.70–22.90). Test **20.952**. Ir>0 persist>=50 pred_d −3.36→**−3.67** vs Exp178 −1.48 (mean toward need) but RMSE 28.75→**29.74**. Typical 7.14→**7.79**. January 31.22→**34.34** loses persist 33.58. Global bias **−2.54**. 3x lr pulled predictions down.

## This fire
- **Exp183 DISCARD** FT Pre-LN lr=3e-4 (isolated cycle 9/50). 1h champion remains Exp167. FT **9/50**. FT val recipe remains Exp178.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT Post-LN depth {1,2,3} closed (do not retry n_layers=4/6 or revert Post-LN)
- FT paper-default d_model 32/96 / n_heads 2/8 as a persist fix closed
- FT Pre-LN dropout={0, 0.2} (do not retry nearby 0.05/0.15/0.3)
- FT Pre-LN batch_size=64 (do not retry nearby 48/128)
- FT Pre-LN weight_decay=1e-4 (do not retry nearby 5e-5/2e-4/0)
- FT Pre-LN lr=3e-4 (do not retry nearby 2e-4/5e-4)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **9/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. FT val recipe is Exp178 Pre-LN dropout 0.1 batch 32 wd 1e-5 lr 1e-4. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (9/50) from the Exp178 Pre-LN recipe (norm_first=true, dropout 0.1, n_layers=3, batch 32, weight_decay=1e-5, lr=1e-4). Next try **warmup=0**. Do not retry lr 2e-4/5e-4. Do not retry wd 5e-5/2e-4/0. Do not retry batch 48/64/128. Do not retry dropout 0/0.2. Do not revert Post-LN. Do not mix MLP HPs. 1h champion remains Exp167 until composite beats −21.972.
