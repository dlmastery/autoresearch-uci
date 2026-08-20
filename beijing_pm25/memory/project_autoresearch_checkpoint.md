# Autoresearch checkpoint — after Exp167 KEEP (1h now Exp167 residual MLP; t+6 recipe Exp76)

**Updated:** 2026-08-20
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 167** MLP residual skips · composite **−21.972** · 2014 test RMSE **20.072** · 2013 val **21.972**
- skill vs persist-1 **+10.06%** · 1h noise floor val ±0.08
- Recipe: Exp136 features + hidden 512-256-128 + residual projection shortcuts · batch 16 · dropout 0.2 · wd=1e-4 · lr 3e-4 · clip=1.0 · layer_norm off
- First 1h KEEP since Exp97. First MLP to beat CatBoost on the frozen 2014 composite.

## Best 2014 test (now the champion)
- **Exp 167** residual MLP · test **20.072** · val **21.972**
- Prior: Exp164 20.201 / 22.180 · Exp141 20.274 / 22.356 · Exp152 20.277 / 22.290

## MLP val recipe
- **Exp 167** is both 1h champion and MLP val recipe.

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** dirty-stable persist>=150 |need|<=10 n=654 RMSE **13.13** vs persist **5.95** vs Exp136 **12.40** (3.47% of Exp164 SSE; pred_d **−3.91** vs need +0.34; 512-wide trunk overwrites lag-1).
- **Exp167 KEEP** residual skips. Val **21.972** beat Exp97 22.167 and Exp164 22.180. Test **20.072**. Dirty-stable 13.13→**11.99**; pred_d −3.91→**−1.78**. Typical 7.53→**7.14**. January 31.90→**31.22**. Onset 111.26→**110.28** still loses persist 107.80.

## This fire
- **Exp167 KEEP** 1h champion. Residual identity path. MLP **43/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP dropout=0.1 (do not retry 0.05 or 0.15)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP extra hidden 256-128-64-32 (do not retry 5-layer or nearby 4th-layer width 16/64)
- MLP hidden 512-256-128 widen (do not retry nearby 384/768 or another 3-layer widen)
- MLP hetero_loss (do not retry another aleatoric-head or nearby heteroscedastic loss)
- MLP grad_clip=0 (do not retry nearby clip 0.1/5/10)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP Adam lr=1e-3 (do not retry 5e-4 or 2e-3)
- MLP batch_size=64 (do not retry nearby 48 or 128)
- MLP weight_decay=0 (do not retry nearby 1e-6)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)
- MLP LayerNorm (do not retry BatchNorm, RMSNorm, or input-only LN)
- MLP pm25_roll6max (do not retry roll3mean)
- MLP pres_delta (do not retry temp_delta or rh_delta)
- MLP evening_peak (do not retry is_morning or heating_night)
- MLP se_iws (do not retry nw_iws)
- MLP pm25_delta6 (do not retry another 6h PM slope)
- MLP is_severe (do not retry another lag1 threshold dummy)
- MLP cbwd_prev_NW (do not retry Iws_lag1 or another previous-direction dummy)
- MLP is_janfeb (do not retry another is_heating split)
- MLP iws_clip100 (do not retry another Iws transform)
- MLP dow_sin (do not retry dow_cos)
- MLP cv_inv (do not retry another calm or inversion product)
- MLP heating_build (do not retry heating_night or another heating product)
- MLP rh_iws (do not retry another RH/wind ratio)
- MLP drop Iws (do not retry dropping log_iws)
- MLP drop Is (do not retry drop Ir; rain under-cleans)
- MLP drop PRES (do not retry drop TEMP or DEWP)
- MLP drop is_weekend (do not retry drop dow)
- MLP drop inversion_spread (do not retry drop rh_magnus or vent_index)
- MLP drop is_heating (do not retry drop month_sin)
- MLP drop cbwd_cv (do not retry drop cbwd_NE/NW/SE)
- MLP drop pm25_accel (do not retry drop pm25_delta1)
- Exp136 extra-feature adds (137–147 plus heating_build, rh_iws) exhausted
- MLP extra depth (Exp148) exhausted
- MLP HP opposites (lr, dropout, batch, wd) exhausted
- Drop-raw-weather (Iws, Is, PRES) exhausted — rethink, not another weather drop
- Collinear-derived drops (is_weekend, inversion_spread, is_heating) exhausted — rethink, not another derived copy

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **43/50**. Isolation holds. 1h champion is **Exp167 residual MLP**. t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp167 recipe** (batch 16, hidden 512-256-128, residual true, dropout 0.2, weight_decay 1e-4, lr 3e-4, clip=1.0, log_iws, month_sin, pm25_accel, vent_index, layer_norm off). Next unused axis: diagnose Exp167 onset (110.28 vs persist 107.80) — **not** pre-activation residual or extra skip-to-head. Do not retry LayerNorm, BatchNorm, nearby 384/768, extra 4th layer, dropout 0.1, drop accel, drop cbwd_cv, extra features 137–147, nearby clip 0.1/5/10, rolling PM stats, 6h PM slopes, lag1 thresholds, previous-direction memory, calendar splits of is_heating, Iws transforms, cyclic weekday encodings, nearby weather derivatives, nearby hour bins, nearby wind products, nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8/48/64/128, dropout 0.4/0.05/0.15, wd 1e-3/0/1e-6, nearby lr shrink/raise, heating products, drop log_iws, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp167 until composite beats −21.972.
