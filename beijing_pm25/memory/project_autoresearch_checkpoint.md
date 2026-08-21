# Autoresearch checkpoint — after Exp175 DISCARD (1h remains Exp167 residual MLP; FT 1/50; t+6 recipe Exp76)

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
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp167, computed): January 31.22 vs persist 33.58 · JJA 13.87 vs persist 14.83 · hour 20 32.68 vs persist 33.24 (11.10% of SSE) · onset n=83 RMSE 110.28 vs persist 107.80 (31.51% of SSE; need +87.40 pred_d −0.60). Val 21.972 vs test 20.072 is the bottleneck.
- **NEW:** hour-20 SE persist>=80 n=74 RMSE **60.62** vs persist **61.42** (8.49% of SSE; need **+14.47** pred_d **+5.69**). The 16 hour-20 SE persist>=80 need>20 hours hold 8.26% of SSE at 128.62 vs persist 129.94 with pred_d only **+10.29** vs need **+64.31**.
- **Exp175 DISCARD** FT-Transformer Gorishniy 2021 paper default. Val **22.698** missed 21.972. Test **23.130** lost persist 22.316. Hour-20 SE persist>=80 60.62→**61.66**; pred_d 5.69→**3.72** (under-jumped). Typical 7.14→**10.22**. Dirty-stable 11.99→**24.29**. January 31.22→**42.85**. Onset 110.28→**119.59**; pred_d −0.60→**−6.95**. CLS buried lag-1.

## This fire
- **Exp175 DISCARD** FT-Transformer paper default (isolated cycle 1/50). 1h champion remains Exp167. FT **1/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT-Transformer Gorishniy 2021 paper default d_model=64 n_layers=3 batch=32 lr=1e-4 (do not retry nearby d_model 32/96 or n_heads 2/8 as a persist fix)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **1/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (1/50) on the Exp167 feature recipe. Next try **n_layers=1** (shallower so CLS cannot bury lag-1). Do not mix MLP HPs into FT. Do not retry paper-default d_model 32/96 or n_heads 2/8. 1h champion remains Exp167 until composite beats −21.972.
