# Autoresearch checkpoint — after Exp191 DISCARD (1h remains Exp167; FT val recipe Exp186 +cbwd_prev_NW; FT 17/50; t+6 Exp76)

**Updated:** 2026-08-22
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
- Best FT test: Exp187 +heating_night **20.350** (val 22.221 DISCARD; val worse than Exp186)
- Best FT val: Exp186 Pre-LN +cbwd_prev_NW **22.066** / test **20.483**
- Prior FT val: Exp178 **22.140** / **20.674** · prior FT test Exp179 **20.509**
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## FT val recipe (isolated, not champion)
- **Exp 186** Pre-LN + cbwd_prev_NW · dropout 0.1 · n_layers 3 · d_model 64 · batch 32 · lr 1e-4 · weight_decay 1e-5 · warmup 10 · val **22.066** · test **20.483**
- Beat Exp178 val 22.140 / test 20.674. Still DISCARD vs Exp167 val 21.972 (Δ0.094). Exp187–190 extra columns all worse val. Recipe stays Exp186.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp167, computed): January 31.22 vs persist 33.58 · JJA 13.87 vs persist 14.83 · hour 20 32.68 vs persist 33.24 (11.10% of SSE) · onset n=83 RMSE 110.28 vs persist 107.80 (31.51% of SSE; need +87.40 pred_d −0.60). Val 21.972 vs test 20.072 is the bottleneck.
- **NEW:** Iws>=100 n=323 RMSE **5.71** vs persist **5.40** (0.33% of SSE; need **−0.32** pred_d **+0.08**). Storm hours easy; Exp186 over-cleans pred_d −1.37.
- **Exp191 DISCARD** FT Pre-LN +iws_clip100 on Exp186. Val **22.354** missed 21.972 and Exp186 22.066 (inside 21.70–22.40). Test **20.946** missed Exp186 20.483. Iws>=100 pred_d +0.08→**−0.68** vs Exp186 −1.37 versus need −0.32 (over-clean damped) but RMSE 5.71→**5.58** vs Exp186 5.51. Typical 7.14→**7.64**. January 31.22→**34.50**. Global bias **+0.47**.

## This fire
- **Exp191 DISCARD** FT Pre-LN add iws_clip100 (isolated cycle 17/50). 1h champion remains Exp167. FT **17/50**. FT val recipe remains Exp186.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT Post-LN depth {1,2,3} closed (do not retry n_layers=4/6 or revert Post-LN)
- FT paper-default d_model 32/96 / n_heads 2/8 as a persist fix closed
- FT Pre-LN dropout={0, 0.2} (do not retry nearby 0.05/0.15/0.3)
- FT Pre-LN batch_size=64 (do not retry nearby 48/128)
- FT Pre-LN weight_decay=1e-4 (do not retry nearby 5e-5/2e-4/0)
- FT Pre-LN lr=3e-4 (do not retry nearby 2e-4/5e-4)
- FT Pre-LN warmup=0 (do not retry nearby 2/5)
- FT Pre-LN warmup=20 (do not retry nearby 15/25). Warmup axis closed {0,20}; recipe 10 stays.
- FT heating_night token (do not retry heating_build)
- FT pres_delta token (do not retry temp_delta/rh_delta)
- FT is_morning token (do not retry evening_peak). Three extra-token DISCARDs on Exp186 — rethink feature class.
- FT pm25_roll3mean (do not retry pm25_roll6max)
- FT iws_clip100 (do not retry other Iws clips)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **17/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. FT val recipe is Exp186 Pre-LN + cbwd_prev_NW. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (17/50) from the Exp186 Pre-LN + cbwd_prev_NW recipe. Next try **add rh_iws**. Do not drop cbwd_prev_NW. Do not retry heating_night/pres_delta/is_morning/evening_peak/pm25_roll3mean/iws_clip100. Do not retry warmup 15/25. Do not retry lr 2e-4/5e-4. Do not retry wd 5e-5/2e-4/0. Do not retry batch 48/64/128. Do not retry dropout 0/0.2. Do not revert Post-LN. Do not mix MLP HPs. 1h champion remains Exp167 until composite beats −21.972.
