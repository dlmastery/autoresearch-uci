# Autoresearch checkpoint — after Exp214 DISCARD (1h remains Exp192; FT 40/50; t+6 Exp76)

**Updated:** 2026-08-24
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 192** FT-Transformer Pre-LN +cbwd_prev_NW +rh_iws · composite **−21.948** · 2014 test RMSE **20.453** · 2013 val **21.948**
- skill vs persist-1 **+8.35%** · 1h noise floor val ±0.08
- Recipe: Exp167 features + cbwd_prev_NW + rh_iws · d_model 64 · n_heads 4 · n_layers 3 · dropout 0.1 · lr 1e-4 · batch 32 · weight_decay 1e-5 · warmup 10 · epochs 100 · patience 15 · norm_first true
- First FT KEEP versus Exp167. First FT-Transformer to hold the frozen 2014 composite.

## Best 2014 test (not the champion)
- **Exp 167** residual MLP · test **20.072** · val **21.972** · composite **−21.972** (now second)
- Best non-champion 2014 test: Exp172 stagn_onset **20.018** (val 21.9995 DISCARD near-miss)
- Best prior FT test: Exp187 +heating_night **20.350** (val 22.221 DISCARD)
- Prior FT val recipe: Exp186 Pre-LN +cbwd_prev_NW **22.066** / test **20.483** (now superseded by Exp192)

## MLP val recipe
- **Exp 167** residual MLP · val **21.972** · test **20.072**. Isolated; do not mix MLP HPs into FT.

## FT val recipe (now the 1h champion)
- **Exp 192** Pre-LN + cbwd_prev_NW + rh_iws · dropout 0.1 · n_layers 3 · d_model 64 · batch 32 · lr 1e-4 · weight_decay 1e-5 · warmup 10 · val **21.948** · test **20.453**
- Beat Exp167 val 21.972 / composite −21.972 (Δ composite +0.024). Test 20.453 missed Exp167 20.072 but beat Exp186 20.483.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- Champion slices (Exp192, computed): January 33.22 vs persist 33.58 · JJA 14.12 vs persist 14.83 · hour 20 32.69 vs persist 33.24 · onset n=83 RMSE 110.79 vs persist 107.80 (need +87.40 pred_d −1.54). Val 21.948 vs test 20.453 is still the bottleneck.
- **NEW:** hour23 persist>=80 n=162 RMSE **25.95** vs persist **25.41** (3.28% of SSE; need **+2.64** pred_d **−0.06**). Midnight dirty hours have the wrong sign and lose to persist; Exp167 was 23.27 / +1.89 and beats persist.
- **Exp214 DISCARD** FT Pre-LN final_ln=true on Exp192. Val **22.685** missed 21.948 (outside 21.70–22.40). Test **22.877** missed 20.453 (outside 20.20–21.20). hour23 persist>=80 pred_d −0.06→**−1.18** RMSE 25.95→**31.62**. Typical 7.54→**10.03**. January 33.22→**41.32**. Global bias −0.07→**−1.04**. Final LN over-cleaned more.

## This fire
- **Exp214 DISCARD** FT Pre-LN final_ln=true (isolated cycle 40/50). 1h champion remains Exp192. FT **40/50**. FT val recipe remains Exp192.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP 50/50 complete as prior (do not retry mixup, onset_underpred, nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50)
- FT Post-LN depth {1,2,3} closed (do not retry n_layers=4/6 or revert Post-LN)
- FT paper-default d_model 32/96 / n_heads 2/8 as a persist fix closed
- FT n_heads=1 (do not retry 3/16). Keep 4 heads
- FT Pre-LN dropout={0, 0.2} (do not retry nearby 0.05/0.15/0.3)
- FT Pre-LN batch_size=64 (do not retry nearby 48/128)
- FT Pre-LN weight_decay=1e-4 (do not retry nearby 5e-5/2e-4/0)
- FT Pre-LN lr=3e-4 (do not retry nearby 2e-4/5e-4)
- FT Pre-LN warmup=0 (do not retry nearby 2/5)
- FT Pre-LN warmup=20 (do not retry nearby 15/25). Warmup axis closed {0,20}; recipe 10 stays.
- FT heating_night token (do not retry heating_build)
- FT pres_delta token (do not retry temp_delta/rh_delta)
- FT is_morning token (do not retry evening_peak)
- FT pm25_roll3mean (do not retry pm25_roll6max)
- FT iws_clip100 (do not retry other Iws clips)
- FT se_iws (do not retry nw_iws/se_pm25)
- FT is_severe (do not retry other lag1 thresholds)
- FT pm25_delta6 (do not retry another 6h PM statistic)
- Extra tokens after Exp192 KEEP closed after 3 DISCARDs (se_iws, is_severe, pm25_delta6) — do not add another unused column
- FT drop pm25_accel (do not drop pm25_delta1)
- FT drop is_weekend (do not drop dow)
- FT drop inversion_spread (do not drop rh_magnus/TEMP/DEWP)
- Collinear drops closed after 3 DISCARDs (pm25_accel, is_weekend, inversion_spread) — do not drop another derived column
- FT patience=8 (do not retry 5/10/12)
- FT patience=25 (do not retry 20/30). Patience both sides of 15 DISCARD — do not retry early-stop
- FT batch_size=16 (do not retry 8/24). Keep batch 32
- FT lr=5e-5 (do not retry 3e-5/7e-5). lr both sides of 1e-4 DISCARD — do not retry nearby lr
- FT ff_factor=4 (do not retry 3/6/8). Keep default 2d FFN
- FT weight_decay=1e-6 (do not retry 5e-6/2e-6). wd both sides of 1e-5 DISCARD — do not retry nearby wd
- FT num_embedding=periodic (do not retry n_frequencies 8/32). Keep linear tokenizer
- FT pooling=mean (do not retry pooling=max/sum). Keep CLS pooling
- FT feature_tokenizer=per_feature (do not retry per-column Linear variants). Keep shared Linear(1,d)
- FT activation=relu (do not retry silu/relu6). Keep GELU
- FT layer_scale=0.1 (do not retry 0.01/0.05/1e-4). Keep unscaled Pre-LN residuals
- FT drop_path=0.1 (do not retry 0.05/0.2/0.3). Keep all 3 Pre-LN blocks
- FT sam_rho=0.05 (do not retry nearby 0.01/0.1/0.2). Keep AdamW
- FT loss=mse (do not retry nearby Huber beta 0.5/2/5/10 or MAE). Keep smooth_l1 beta=1
- FT final_ln=true (do not retry nearby RMSNorm or extra head-LN). Keep Pre-LN without a final LN
- Do not drop rh_iws or cbwd_prev_NW from Exp192

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **50/50 complete**. FT-Transformer **40/50**. Isolation holds. 1h champion is **Exp192 FT Pre-LN +rh_iws**. t+6 recipe remains Exp76.

## Next pasteable
Isolate **FT-Transformer** (40/50) from the Exp192 Pre-LN + cbwd_prev_NW + rh_iws recipe. Do not retry final_ln or nearby RMSNorm/head-LN. Keep Pre-LN without a final LN. Do not retry loss=mse or nearby Huber beta 0.5/2/5/10 or MAE. Keep smooth_l1 beta=1. Do not retry sam_rho 0.05/0.01/0.1/0.2. Keep AdamW. Do not retry n_heads=1/3/16 (2/8 already closed as persist fix). Keep 4 heads. Do not retry drop_path 0.1/0.05/0.2/0.3. Keep all 3 Pre-LN blocks. Do not retry layer_scale 0.1/0.01/0.05/1e-4. Keep unscaled Pre-LN residuals. Do not retry activation=relu/silu/relu6. Keep GELU. Do not retry feature_tokenizer=per_feature or per-column Linear variants. Keep shared Linear(1,d). Do not retry pooling=mean/max/sum. Keep CLS pooling. Do not retry num_embedding=periodic or n_frequencies 8/32. Keep linear tokenizer. Do not retry wd 1e-6/5e-6/2e-6 or 5e-5/2e-4/0/1e-4. Keep wd 1e-5. Do not retry ff_factor 3/4/6/8. Keep 2d FFN. Do not retry lr 5e-5/3e-5/7e-5 or 2e-4/3e-4/5e-4. Keep lr 1e-4. Do not retry batch 16/8/24 or 48/64/128. Do not retry patience {5,8,10,12,20,25,30}. Keep batch 32, patience=15, inversion_spread, is_weekend, pm25_accel. Do not drop another derived column. Do not add another unused extra column. Do not retry drop-inv/drop-weekend/drop-accel/pm25_delta6/is_severe/se_iws. Do not retry heating_night/pres_delta/is_morning/evening_peak/pm25_roll3mean/iws_clip100. Do not retry warmup 15/25. Do not retry dropout 0/0.2. Do not revert Post-LN. Do not mix MLP HPs. Next fire must diagnose a NEW slice and pick a legal unused axis (GEGLU FFN), not another final-LN/loss/SAM/n_heads/drop_path/LayerScale/activation/tokenizer/pooling/periodic/wd/FFN-widen/lr/batch/patience/drop/extra-token. 1h champion remains Exp192 until composite beats −21.948.
