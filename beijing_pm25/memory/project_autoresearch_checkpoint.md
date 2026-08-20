# Autoresearch checkpoint — after Exp139 (1h still Exp97; t+6 recipe Exp76)

**Updated:** 2026-08-19
**Split:** `uci381-calendar-2010_2012-train-2013-val-2014-test-purge24h`
**test_hash:** `efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc`

## 1h champion
- **Exp 97** CatBoost Plain · composite **−22.167** · 2014 test RMSE **20.735** · 2013 val **22.167**
- skill vs persist-1 **+7.09%** · 1h noise floor val ±0.08
- Features: inversion+delta + rh_magnus + dewp_delta + is_heating · depth 6 · lr 0.03 · l2=3 · Plain SymmetricTree

## Best 2014 test (not champion)
- **Exp 135** MLP batch 16 + log_iws + month_sin + pm25_accel · test **20.417** · val **22.350**

## MLP val recipe (not 1h champion)
- **Exp 136** MLP batch 16 + wd=1e-4 + log_iws + month_sin + pm25_accel + vent_index · val **22.259** · test **20.509** · January **30.96**

## t+6 side ladder (do not mix composites)
- **Exp 76** LightGBM extra_trees + linear_tree + ff=1.0 + linear_lambda=1 + month_sin + pres_delta + dewp_delta + cbwd_prev_NW + rh_magnus · test **54.312** · val **57.161**

## Residual (this fire)
- **NEW:** weekday hours 18-21 n=939 RMSE **29.66** vs CB **28.77** vs persist **31.31**, need **+5.43** pred_d **+2.67** (24.7% of Exp136 SSE). Hour 18-21 overall 28.1% SSE, pred_d **+2.53** vs need **+4.87**.
- **Exp139 DISCARD** evening_peak. Val **22.425** missed Exp136 22.259. Test 20.501. Weekday 18-21 29.66→**29.68** flat; pred_d +2.67→**+4.42**. Hour 20 32.19 stayed. 2013 val inverted.

## This fire
- **Exp139 DISCARD** 1h vs Exp97. Evening dummy moved 2014 pred_d toward need but RMSE and 2013 val did not. MLP recipe remains Exp136. MLP **15/50**.

## Exhausted / closed
- CatBoost 50/50 as prior
- MLP dropout=0.3 (do not retry 0.4/0.5)
- MLP hidden 128-64-32 (do not retry 64-32-16 or another nearby shrink)
- MLP Adam lr=1e-4 (do not retry 5e-5 or another nearby shrink)
- MLP epochs=80 (do not retry 60/100 or another nearby cosine budget)
- MLP patience=5 (do not retry 3 or another nearby shrink)
- MLP pm25_roll6max (do not retry roll3mean)
- MLP pres_delta (do not retry temp_delta or rh_delta)
- MLP evening_peak (do not retry is_morning or heating_night)

## Process
LightGBM **50/50 complete**. CatBoost **50/50 complete**. MLP **15/50**. Isolation holds. 1h champion unchanged (Exp97). t+6 recipe remains Exp76.

## Next pasteable
Stay isolated on **MLP Exp136 recipe** (batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, lr 3e-4, log_iws, month_sin, pm25_accel, vent_index). Change another unused **feature** next (e.g. se_iws). Do not retry rolling PM stats, nearby weather derivatives, nearby hour bins, nearby products, nearby second-diff, month Fourier, log-Iws, nearby patience, nearby epochs, batch 8, dropout 0.4, wd 1e-3, nearby lr shrink, or width shrink. Do not mix CatBoost HPs. 1h champion remains Exp97 until MLP composite beats −22.167.
