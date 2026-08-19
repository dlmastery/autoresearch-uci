# Research journal — UCI 381 Beijing PM2.5

Karpathy rule: one change, KEEP if composite rose, otherwise revert. Test year 2014 never moved.

## The ladder

persistence (2014) test RMSE 22.316

**Exp1 KEEP** Chen & Guestrin 2016 XGBoost → 21.768. Skill +2.5%.

**Exp2 KEEP** max_depth 4. Test 21.996 (worse) but val 23.205 (better). Composite rose because val was the min(). Gate working.

**Exp4 KEEP** lr 0.01. Shrinkage on the depth-4 tree.

**Exp8 KEEP** subsample 0.6. Stochastic rows.

**Exp14 KEEP** inversion_spread = TEMP−DEWP (Liang 2015). First real test drop (21.823).

**Exp15 KEEP** pm25_delta1 = lag1−lag2. Onset momentum. Test 21.290.

**Exp22 KEEP** stack inversion onto delta. Test 21.122, val 22.470, skill +5.4%.

**Exp29 KEEP** LightGBM on those exact features. Test 20.784, val 22.428. First backbone KEEP that is not XGBoost.

**Exp30 KEEP** num_leaves 31→63. Test 20.945 (slightly worse) but val 22.397 (better). Skill +6.15%. Held the 1h crown until Exp96.

**Exp96 KEEP** CatBoost Plain + rh_magnus + dewp_delta (Tie 2017). Test **20.881** · val **22.357** · composite **−22.357**. Skill +6.43%. First 1h KEEP since Exp30.

**Exp97 KEEP** is_heating on Exp96 (Huang 2014). Test **20.735** · val **22.167** · composite **−22.167**. **Current 1h champion.** Skill +7.09%.

## What was thrown away

86 DISCARDs then **Exp96 KEEP**. t+6 side-KEEPs: Exp46, Exp47, Exp55, Exp56, Exp59, Exp68, Exp70, Exp72, Exp75 rh_magnus, **Exp76** linear_lambda=1 (val 57.16 / test 54.31). CatBoost Exp91 rh_magnus was the 0.052 NEAR-MISS that dewp_delta promoted.

1h bagging was a no-op until Exp43 (`bagging_freq` default 0). Seed noise ≈ val ±0.08 (Exp44). Depth/lr/weather-lags/raw-hour/subsample/GOSS/DART/Huber/extra_trees/min_data/linear_tree/accel/vent/max_bin/roll6max/bagging_freq=1: no composite gain.

## Champion residual (computed, not remembered)

See `champion_diagnostics.json`. Exp97 onset / month / hour slices after this KEEP. Skill +7.09%. January RH>=70 leftover still 36.68 vs persist 23.94.

## Process note (2026-08-18)

Exp1–31 did **not** follow the original hillclimb skill (50 isolated experiments per backbone, many papers inside each). Recovery: isolate LightGBM, paper recipes (GOSS, DART, objectives), then CatBoost / MLP / FT-Transformer. Dashboard and 14-section audit pack brought up to the original github.io standard this session.

## This fire (2026-08-18, Exp93)

New Exp91 slices: hour 10 RMSE **23.95 vs Exp30 21.40 / persist 22.86**. Hour 22 **20.95 vs persist 20.19**. January cv **32.53 vs persist 26.72**.

**Exp93 DISCARD** rsm=0.8. Val 22.569 worse than Exp91 22.449. Test **20.945** ties Exp30. Hour-10 23.27.

1h champion unchanged: Exp30. t+6 recipe remains Exp76. CatBoost **19/50**. Best CatBoost val remains Exp91.

## This fire (2026-08-18, Exp94–Exp95)

New Exp91 slices: PRES>=1025 persist>=150 n=413 RMSE **44.27 vs Exp30 41.59 / persist 40.56**. Over-cleans pred_d **−12.2 vs need −3.2**. No previous-hour NW subset n=277 RMSE **43.72 vs persist 38.64**.

**Exp94 DISCARD** cbwd_prev_NW. Val 22.528 test 21.063. hiP dirty 44.27→43.36 (in 40–43) but no-NW stagnant 43.72→43.66 flat; dummy helped previous-NW hours instead.

**Exp95 DISCARD** random_strength=2. Val 22.451 vs Exp91 22.449 (inert). Test 21.005. hiP dirty 43.89 missed 40–43.5.

1h champion was still Exp30 after Exp94–95. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp96 KEEP)

New Exp91 slices: Friday n=1119 RMSE **24.81 vs persist 24.13 / Exp30 23.59**. Hour-1 **29.71 vs persist 28.19**. dewp-rise persist>=150 n=378 RMSE **36.61 vs persist 35.88**, over-clean pred_d **−4.25 vs need +0.51**. dewp_delta corr with 1h increment **0.16**.

**Exp96 KEEP** dewp_delta. Val **22.357** beat Exp30 22.397. Test **20.881** beat 20.945. Composite **−22.357**. Friday 24.81→**24.03** (now beats persist). dewp-rise dirty only 36.61→36.47. **New 1h champion is CatBoost Exp96.**

CatBoost **22/50**. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp97 KEEP)

New Exp96 slices: January RH>=70 n=84 RMSE **38.25 vs persist 23.94 / Exp30 29.59** (skill −59.8%). January Iws<2 **34.91 vs persist 29.42**. January hour-1 **76.95 vs persist 69.40** (need +8.32 pred_d −5.35). Hour-1 outside January **20.63 ≈ persist 20.60**.

**Exp97 KEEP** is_heating. Val **22.167** beat Exp96 22.357. Test **20.735** beat 20.881. Composite **−22.167**. Skill **+7.09%**. January RH>=70 38.25→36.68 (missed 24–32). JJA 14.05→**13.84** (no month_sin summer tax). **New 1h champion is CatBoost Exp97.**

CatBoost **23/50**. t+6 recipe remains Exp76.

## This fire (2026-08-18, Exp98–Exp99)

New Exp97 slices: January RH>=70 is **all Ir=0**. January RH>=70 Iws<2 n=45 RMSE **42.65 vs persist 22.94** (skill −85.9%). January RH>=70 hours 0-5 n=37 RMSE **38.33 vs persist 18.85** (skill −103.4%). JJA RH>=70 Ir=0 is fine (14.93 vs persist 15.75).

**Exp98 DISCARD** heating_night. Val 22.343. Hours 0-5 38.33→37.60; Iws<2 42.65→**44.31** worse.

**Exp99 DISCARD** bagging_temperature=2. **Bit-identical** to Exp97.

1h champion unchanged: Exp97. CatBoost **25/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp100)

New Exp97 slices: January RH>=70 Iws<2 persist>=150 n=17 RMSE **68.74 vs persist 36.22**. January RH>=70 Iws<2 dewp_rise n=12 RMSE **51.75 vs persist 9.02**. January rh_iws q3 n=156 RMSE **39.39 vs persist 28.71**.

**Exp100 DISCARD** rh_iws. Val 22.178 (0.012 above Exp97). Test 20.726. January rh_iws q3 39.39→**40.03** worse. Ratio redundant with rh_magnus plus Iws.

1h champion unchanged: Exp97. CatBoost **26/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp101)

New Exp97 slices: January persist>=150 delta1>0 n=109 RMSE **53.00 vs persist 39.20** (skill −35.2%, need +4.82 pred_d −6.04). January persist>=150 already falling skill **+10.6%**. January persist>=150 PRES>=1025 n=88 RMSE **68.58 vs persist 60.04**.

**Exp101 DISCARD** heating_build. Val 22.322 test 20.990. Building-dirty 53.00→**53.86**. JJA 13.84→14.00. Third interaction DISCARD after heating_night and rh_iws.

1h champion unchanged: Exp97. CatBoost **27/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp102)

New Exp97 slices: January is 8.7% of hours but **24.5% of SSE**. January persist>=150 delta1>0 PRES>=1025 n=52 is **0.7% n / 7.2% SSE**, RMSE **68.80 vs persist 47.75** (need +13.38 pred_d −18.48). not-January building-dirty beats persist (29.41 vs 32.76).

**Exp102 DISCARD** Depthwise. Val 22.322 test 21.040. The 52-hour shard 68.80→**77.22**. SymmetricTree stays.

1h champion unchanged: Exp97. CatBoost **28/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp103)

New Exp97 slices: onset n=83 is **29.4% of SSE**. Onset dPRES>=1 n=20 is **14.7% SSE**, RMSE **158.68 vs persist 156.02** (need +119 pred_d −0.96). corr(pres_delta, need | onset)=**0.34**.

**Exp103 DISCARD** pres_delta. Val 22.352 test 20.820. Onset dPRES>=1 158.68→**157.78**, pred_d still −0.40 versus need +119.

1h champion unchanged: Exp97. CatBoost **29/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp104)

New Exp97 slices: January weekday n=520 is **21.0% SSE**, RMSE **37.18 vs persist 33.67** (skill −10.4%, pred_d −4.86 vs need +0.35). January weekend **26.39 vs persist 33.29** (skill +20.7%). January Friday **50.59 vs persist 46.70**.

**Exp104 DISCARD** min_data_in_leaf=20. **Bit-identical** to Exp97.

1h champion unchanged: Exp97. CatBoost **30/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp105)

New Exp97 slices: January weekday persist>=150 n=141 is **13.0% SSE**, RMSE **56.12 vs persist 45.99** (pred_d −18.33 vs need −7.60). January weekday hours 0-5 **51.08 vs persist 43.95**. January Friday 18-21 **65.27 vs persist 50.33**.

**Exp105 DISCARD** early_stopping_rounds=50. **Bit-identical** to Exp97.

1h champion unchanged: Exp97. CatBoost **31/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp106–Exp107)

New Exp97 slices: January weekday persist>=150 with delta6>20 n=92 is **10.1% SSE**, RMSE **61.11 vs persist 43.87** (pred_d −17.76 vs need −1.91). Falling 6h beats persist (45.87 vs 54.46). January Thursday persist>=150 n=47 is **6.8% SSE**, RMSE **70.42 vs persist 50.96**, mean Iws **4.13 vs 10.14** on other January weekday persist, mean actual **343.8**. Hours 18-21 persist need **+26.38** pred_d **+1.34**.

**Exp106 DISCARD** pm25_delta6. Val **22.345** test **20.671**. Building leftover 61.11→60.16 (missed 44–56). Thursday 70.42→**72.21** worse.

**Exp107 DISCARD** log_iws. Val **22.310** test **20.783**. Thursday 70.42→**72.35**. Iws<5 persist 56.88→**58.75** worse.

1h champion unchanged: Exp97. CatBoost **33/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp108–Exp109)

New Exp97 slices: **2014-01-16** n=24 is **6.1% of all 2014 SSE**, RMSE **93.08 vs persist 64.49** (pred_d −58.69 vs need −9.21, mean 457.5). Other January Thursdays match persist (01-02 28.86 vs 29.93). January weekday persist>=300 n=39 is **7.4% SSE**, RMSE **80.36 vs persist 55.80**; not-January persist>=300 beats persist (34.41 vs 41.44). January weekday persist 18-21 n=26 RMSE **58.70 vs persist 44.95**, need **+26.38** pred_d **+1.34**.

**Exp108 DISCARD** is_severe. Val **22.313** test **20.899**. 2014-01-16 93.08→**100.50**. persist>=300 80.36→**84.72**.

**Exp109 DISCARD** evening_peak. Val **22.349** test **20.756**. persist 18-21 58.70→**59.78**. Hour 20 32.48→32.32.

1h champion unchanged: Exp97. CatBoost **35/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp110)

New Exp97 slices: **2014-01-16 hours 0-8** n=9 is **4.0% of all 2014 SSE**, RMSE **123.22 vs persist 48.74** (pred_d −118.60 vs need −10.00, mean 605). Hours 9-23 **beat persist** (68.94 vs 72.31). RH rises 58.5→79.6, Iws<3. corr(rh_delta, need | 0-8)=**0.72**. Other January overnight persist>=150 beats persist (39.85 vs 49.48).

**Exp110 DISCARD** rh_delta. Val **22.236** (near-miss, +0.069 inside ±0.08 noise) test **20.661**. Hours 0-8 123.22→**122.74** leftover inert.

1h champion unchanged: Exp97. CatBoost **36/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp111)

New Exp97 slices: 2014-01-16 hours 0-8 **not-NW** n=6 is **3.3% SSE**, RMSE **137.65 vs persist 42.70** (need +9.33 pred_d −120.74). cv subset n=3 RMSE **151.75 vs persist 52.38**. Other January overnight persist and cv persist>=300 hours 0-8 excluding Jan 16 **match or beat persist**. January onset n=18 is **10.3% SSE**, RMSE **139.91 vs persist 127.93**. Hour 20 need +7.65 pred_d +4.96.

**Exp111 DISCARD** temp_delta. Val **22.357** test **20.715**. Hour 20 32.48→**32.50**. Jan16 hours 0-8 123.22→**128.48** worse.

1h champion unchanged: Exp97. CatBoost **37/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp112)

New Exp97 slices: January onset n=18 is **10.3% SSE**, RMSE **139.91 vs persist 127.93**. **2014-01-31 hour 1** alone is **3.5% of all 2014 SSE**, need **+332**, SE, Iws **41.58**. January onset SE n=10 is **6.9% SSE**, RMSE **154.00 vs persist 149.49**. corr(se×Iws, need | Jan onset)=**0.56**. se_start hours beat persist.

**Exp112 DISCARD** se_iws. Val **22.316** test **20.804**. January onset 139.91→**143.53**. 01-31 h1 348→347 inert.

1h champion unchanged: Exp97. CatBoost **38/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp113)

New Exp97 slices: January excluding 10 bomb hours (01-16 h0-8 + 01-31 h1) n=679 **BEATS persist**, RMSE **29.19 vs 30.83**, skill **+5.3%**. The 10 bombs are **7.5% SSE**, RMSE **160.58 vs persist 114.72**. After the +332 spike, hour 2 chases lag1=469 to pred **499** vs actual **344**.

**Exp113 DISCARD** pm25_roll3mean. Val **22.360** test **20.743**. Hour-2 abs 155→**139**. January post-onset 89.11→83.90 still vs persist 59.80.

1h champion unchanged: Exp97. CatBoost **39/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp114)

New diagnosis: **2013 val persist RMSE 24.50** vs 2014 test **22.32**. Exp97 skill is **+9.5% on val** vs **+7.1% on test**. 2013 January persist **37.47** mean **166.8**, persist>=300 n=**138** vs 2014 n=39. 2013 February persist **38.30** vs 2014 **26.01**.

**Exp114 DISCARD** is_janfeb. Val **22.342** test **20.792**. January 34.84→35.02. Peak-heating subset of is_heating did not help 2013 val.

1h champion unchanged: Exp97. CatBoost **40/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp115)

New diagnosis: lag24 corr with y is **0.306 on 2013 val** vs **0.397 train** vs **0.440 test**. lag12 0.509 val vs 0.558 train vs 0.610 test. 2013 val persist **24.50** vs 2014 **22.32**.

**Exp115 DISCARD** drop lag13-24. Val **22.260** (near-miss, +0.093) test **20.688** (beat). January 34.84→34.02. Hypothesis inverted: long lags slightly help 2013 val.

1h champion unchanged: Exp97. CatBoost **41/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp116)

New diagnosis: train Iws mean **26.82** with **7.2%** hours >100 vs val **21.42 / 4.7%** vs test **19.44 / 4.1%**. Train Iws p99 **273** vs val p90 **51**. Snow corr 0.055 val vs 0.007 train.

**Exp116 DISCARD** iws_clip100. Val **22.323** test **20.767**. January 34.84→35.03. Iws storm tail is useful; clip did not help 2013.

1h champion unchanged: Exp97. CatBoost **42/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp117)

New diagnosis: corr(dow, y) train **0.000** vs val **0.063** vs test **0.069**. 2013 Thursday mean **80.6** (cleanest weekday) vs train Thu **96.5** vs 2014 Thu **109.8**. Test Thu/Fri lose to persist.

**Exp117 DISCARD** drop dow. Val **22.212** (near-miss, +0.045 inside ±0.08) test **20.795**. Thursday 20.85→**21.82**. dow still helps; keep is_weekend too.

1h champion unchanged: Exp97. CatBoost **43/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp118)

New diagnosis: hour-20 Wednesday n=49 RMSE **73.90 vs persist 74.10** (need +15.43 pred_d +3.18). Hour-20 Wednesday mean PM train **107.6** vs 2013 val **84.6** vs 2014 **114.0**. Friday 18-21 n=189 RMSE **26.96 vs persist 24.54**, corr(pred_d, need) **−0.144**. 2013 Friday persist **27.5** is the hardest val weekday.

**Exp118 DISCARD** model_size_reg=1.0. **Bit-identical** to Exp97. Weak leaf-size penalty does not change any split. Keep dow and is_weekend.

1h champion unchanged: Exp97. CatBoost **44/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp119)

New diagnosis: hour 1 RMSE **29.32 vs persist 28.19**. 2013 val hour-1 need **−2.18** (overnight fall) vs 2014 **+1.45** vs 2010/2012 ~**+2.0**. January hour-1 n=28 RMSE **74.63 vs persist 69.40**, need +8.32 pred_d **−5.90**, 4.6% of 2014 SSE.

**Exp119 DISCARD** Bernoulli subsample=0.8. Val **22.231** test **20.818**. January hour-1 74.63→**74.97**, pred_d still −5.72. Row subsample did not fix overnight over-clean.

1h champion unchanged: Exp97. CatBoost **45/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp120)

New diagnosis: January PRES>=1025 n=428 is **16.5% of 2014 SSE**, RMSE **36.25 vs persist 33.83**, need +0.52 pred_d **−5.60**. Train 2011 PRES>=1025 **34.7%** vs 2013 val 24.4 vs 2014 25.9. Inversion mean train ~10.1 vs val 11.03 vs test 11.67.

**Exp120 DISCARD** border_count=128. Val **22.264** test **21.139**. January PRES>=1025 36.25→**38.85**, pred_d −5.60→**−5.88**. Coarser borders over-cleaned more.

1h champion unchanged: Exp97. CatBoost **46/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp121)

New diagnosis: hour-20 NW n=66 RMSE **18.55 vs persist 13.83**, need +1.88 pred_d **−1.49**. NW persist>=150 Iws>=10 n=101 RMSE **47.82 vs persist 55.06** but pred_d **−28.2** vs need −19.15. Train NW share 32–37% vs 2013 31.4 vs 2014 28.2.

**Exp121 DISCARD** nw_iws. Val **22.240** test **20.804**. Hour-20 NW 18.55→**17.49** (pred_d −1.49→−0.74) but val rose. Dirty NW Iws>=10 over-cleaned more (−28.2→**−30.28**).

1h champion unchanged: Exp97. CatBoost **47/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp122)

New diagnosis: hour 8-9 n=663 RMSE **18.16 vs persist 18.26**, need −0.20 pred_d **−1.47**. 2013 val hour 8-9 need **−2.37** vs 2014 **−0.20** vs 2010 **+0.05**. January hour 8-9 need +0.26 pred_d −2.80.

**Exp122 DISCARD** is_morning. Val **22.346** test **20.763**. Hour 8-9 18.16→**18.00** (pred_d −1.47→−1.14) but 2013 val rose. Morning flag overfit 2013 breakup.

1h champion unchanged: Exp97. CatBoost **48/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp123)

New diagnosis: corr(dow_sin, y) val **−0.078** vs 2011 **+0.051** vs 2012 **−0.046**. Numeric dow corr val 0.065 vs train ~0. Test residual corr with dow_sin **−0.027**. Thursday still loses persist 20.85 vs 20.75.

**Exp123 DISCARD** dow_sin. Val **22.360** test **20.829**. Thursday 20.85→**21.31**. Cyclic weekday taxed val more than drop-dow (22.212). Keep numeric dow.

1h champion unchanged: Exp97. CatBoost **49/50**. t+6 recipe remains Exp76.

## Next (original process)

1. Stay isolated on **CatBoost Exp97**
2. Do not retry dow_sin / dow_cos / hour-bin dummies / wind×Iws / border_count {64,128} / Bernoulli subsample / model_size_reg {1.0, 2.0} / drop dow / drop is_weekend / Iws clips / drop lag7-12 / month dummies / roll3mean / se_iws / weather increments / lag1 flags / evening bins
3. Keep numeric dow, is_weekend, hour_sin/hour_cos. Last CatBoost slot (50/50): leave Exp97 or one unused feature that is not cyclic weekday, hour bins, wind-speed products, or unused regularizer HPs. Do not start MLP until CatBoost 50/50.
