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

## This fire (2026-08-19, Exp124)

New diagnosis: cv persist>=150 n=505 is **12.4% of 2014 SSE**, RMSE **28.95 vs persist 27.68**, need +1.28 pred_d **−0.01**. 2013 val cv-dirty persist RMSE **37.95** vs 2014 **27.68**, 2013 need **−0.09** vs 2014 **+1.28**. Mean inversion 6.36.

**Exp124 DISCARD** cv_inv. Val **22.250** test **20.754**. cv persist>=150 28.95→**29.44**, pred_d −0.01→**−0.38**. Calm times inversion over-cleaned.

1h champion unchanged: Exp97. **CatBoost 50/50 complete.** t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp125)

Snapshot `code_versions/catboost_final`. New diagnosis: typical |need|<=10 n=5117 RMSE **8.35 vs persist 5.08** (trees over-adjust). |need|>=30 beats persist 59.01 vs 67.57. persist>=q67 is **67.1% of SSE**. corr(|need|,|err|)=**0.866**.

**Exp125 DISCARD** MLP default 256-128-64. Val **22.623** (gate). Test **20.648** beat Exp97 20.735 (best 2014). January 34.84→**31.02** (now beats persist 33.58). Typical 8.35→**7.28**. Onset 110.06→109.53.

1h champion unchanged: Exp97. MLP **1/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp126)

New diagnosis: MLP val-test gap **1.975** vs CatBoost **1.432**. February 24.09→25.56 and April 27.06→28.86 ate Exp125's January win (34.84→31.02). 2013 February persist **38.30** vs 2014 **26.01**.

**Exp126 DISCARD** dropout=0.3. Val **22.729** worse than Exp125 22.623. Test **20.483** (new best 2014). April 28.86→**26.61**. February still 25.47 vs Exp97 24.09. Hypothesis inverted.

1h champion unchanged: Exp97. MLP **2/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp127)

New diagnosis: collapse n=162 MLP **78.82 vs CatBoost 74.05** vs persist 97.87, pred_d **−22.24** vs CB **−24.95** vs need **−86.31**. December 21.58 vs CB 21.02. Hour 1 27.90 beats persist 28.19.

**Exp127 DISCARD** 1h (composite −22.528 vs Exp97 −22.167). Val **22.528** beat Exp125 22.623 (new MLP val recipe). Test 20.773. Collapse 78.82→**81.47**. January 31.02→**30.82**.

1h champion unchanged: Exp97. MLP **3/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp128)

New diagnosis: hour 21 persist>=150 n=65 RMSE **58.72 vs CatBoost 50.21** vs persist **56.30**, need +1.72 pred_d **+5.15**. |need|>=80 n=82 is **46.5% of Exp127 SSE** vs 41.3% of Exp97, RMSE **139.40 vs CB 131.19**, pred_d **−16.53 vs CB −27.85**. April 29.24 vs CB 27.06.

**Exp128 DISCARD** hidden 128-64-32. Val **23.080** missed Exp127 22.528. Test **21.344**. Hour-21 persist>=150 58.72→**64.79**. |need|>=80 139.40→**143.33**. Typical 7.03→**7.81**. Hypothesis inverted.

1h champion unchanged: Exp97. MLP **4/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp129)

New diagnosis: Iws q3 n=1836 (Iws 5.34–17.88) is **37.34% of Exp127 SSE** vs 33.64% of Exp97, RMSE **26.41 vs CatBoost 25.03** vs persist 28.64. April Iws q3 **52.7 loses persist 52.1**. persist>=300 pred_d **−3.39 vs need −6.23**.

**Exp129 DISCARD** Adam lr=1e-4. Val **23.069** missed Exp127 22.528. Test **21.349**. Iws q3 26.41→**27.03**. April Iws q3 52.7→**54.95**. persist>=300 40.54→**43.57**. Hypothesis inverted (underfit).

1h champion unchanged: Exp97. MLP **5/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp130)

New diagnosis: SE wind n=2937 is 36.9% of hours but **43.6% of Exp127 SSE** vs 41.1% of Exp97, RMSE **22.56 vs CatBoost 21.87** vs persist 23.27, need +2.51 pred_d **+0.77**. SE persist>=150 n=562 **32.65 vs CB 30.59**. Rain Ir>0 n=260 **24.89 vs CB 21.51**.

**Exp130 DISCARD** 1h (val **22.527** vs Exp97 22.167). Test **20.457** new 2014 best. SE 22.56→**21.92**. SE persist>=150 32.65→**30.37** (beats CB). Val tied Exp127 22.528. Promote Exp130 as MLP recipe.

1h champion unchanged: Exp97. MLP **6/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp131)

New diagnosis: hour 18 persist>=100 n=103 RMSE **32.58 vs CatBoost 27.03** vs persist 36.50, need −1.04 pred_d **+1.82**. Hour 18 overall **26.99 vs CB 24.68** is **7.27% of Exp130 SSE** vs 5.91% of Exp97. February hour 18 **50.6 vs CB 37.5**. Val-test gap **2.07** vs CB 1.432.

**Exp131 DISCARD** epochs=80. Val **22.545** missed Exp130 22.527. Test **20.607**. Hour-18 persist>=100 32.58→**32.23**. Hour 18 26.99→**26.76**. Hypothesis barely moved the tail.

1h champion unchanged: Exp97. MLP **7/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp132)

New diagnosis: hour 13 n=333 RMSE **17.98 vs CatBoost 16.22** vs persist 19.99, need −1.41 pred_d **−2.30** (over-cleans midday). January hour 13 **26.2 vs CB 20.4**. April hour 13 pred_d **−7.1 vs need −2.0**. JJA **14.15 vs CB 13.84**.

**Exp132 DISCARD** patience=5. Val **22.757** missed Exp130 22.527. Test **20.764**. Hour 13 17.98→**18.09**. Train 143s→73s. Hypothesis inverted (underfit).

1h champion unchanged: Exp97. MLP **8/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp133)

New diagnosis: rain Ir>0 n=260 RMSE **24.80 vs CatBoost 21.51** vs persist 27.27, 4.8% of Exp130 SSE vs 3.5% of Exp97. Rainy high-Iws n=87 (mean Iws 30.4) **30.77 vs CB 24.06**, need −11.29 pred_d **−3.89**. June rain n=28 need **−13.93** pred_d **−0.97**.

**Exp133 DISCARD** 1h (val **22.502** vs Exp97 22.167). Val beat Exp130 22.527 (new MLP val). Test **20.587**. Rain 24.80→**23.59**. Rainy high-Iws 30.77→**29.04**. Hypothesis held on rain slice.

1h champion unchanged: Exp97. MLP **9/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp134)

New diagnosis: February n=597 RMSE **25.67 vs CatBoost 24.09** vs persist 26.01, 11.7% of Exp133 SSE vs 10.1% of Exp97, need −0.12 pred_d **−3.96**. Residual corr with month_sin **−0.078**. is_heating aliases February with November.

**Exp134 DISCARD** 1h (val **22.432** vs Exp97 22.167). Val beat Exp133 22.502 (new MLP val). Test **20.450** new 2014 best. February 25.67→**25.52**, pred_d −3.96→**−3.26**. November 21.22→**20.74**. Hypothesis held.

1h champion unchanged: Exp97. MLP **10/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp135)

New diagnosis: accel-q4 n=1941 (mean second-diff +26.4) is **31.5% of Exp134 SSE**, RMSE **23.22 vs CatBoost 24.38** vs persist 25.11, need +1.11 pred_d **−0.02** (under-builds accelerating persist). Surprise onset accel<=0 n=35 **138.71 vs persist 133.37**.

**Exp135 DISCARD** 1h (val **22.350** vs Exp97 22.167). Val beat Exp134 22.432 (new MLP val). Test **20.417** new 2014 best. Accel-q4 23.22→**23.13**, pred_d −0.02→**+0.32**. Hypothesis held.

1h champion unchanged: Exp97. MLP **11/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp136)

New diagnosis: vent-q3 n=1985 (Iws 11.3, inversion 14.0) RMSE **19.71 vs CatBoost 19.00** vs persist 22.59, 23.3% of Exp135 SSE vs 21.0% of Exp97, need −0.80 pred_d **−2.54** (over-cleans moderate mixing).

**Exp136 DISCARD** 1h (val **22.259** vs Exp97 22.167). Val beat Exp135 22.350 (new MLP val, gap **0.092**). Test **20.509**. Vent-q3 19.71→**19.86**. Hypothesis held on 2013 val, missed 2014 vent-q3.

1h champion unchanged: Exp97. MLP **12/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp137)

New diagnosis: hours fallen >=80 from 6h lag peak n=620 RMSE **27.53 vs CatBoost 26.26** vs persist 32.91, need −8.11 pred_d **−9.03**. At-peak n=2685 need **+3.80** pred_d **+1.38** (43.8% of SSE).

**Exp137 DISCARD** roll6max. Val **22.451** missed Exp136 22.259. Test **20.478**. Drop>=80 27.37→**27.32**. Onset 110.39→**107.28** (beats persist) but 2013 val inverted.

1h champion unchanged: Exp97. MLP **13/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp138)

New diagnosis: collapse hours with dPRES>=1 n=51 RMSE **86.12 vs CatBoost 80.04** vs persist 107.64, need −91.41 pred_d **−24.29** (11.3% of Exp136 SSE vs 9.6% of Exp97). persist>=150 collapse n=35 RMSE **97.53 vs CB 88.82**.

**Exp138 DISCARD** pres_delta. Val **22.438** missed Exp136 22.259. Test **20.440**. Collapse dPRES>=1 86.12→**83.33**, pred_d −24.29→**−27.43** vs need −91.41. Hour 20 32.19→**31.62**. 2014 slice held; 2013 val inverted.

1h champion unchanged: Exp97. MLP **14/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp139)

New diagnosis: weekday hours 18-21 n=939 RMSE **29.66 vs CatBoost 28.77** vs persist 31.31, need +5.43 pred_d **+2.67** (24.7% of Exp136 SSE). Hour 18-21 overall 28.1% SSE, pred_d **+2.53** vs need **+4.87**.

**Exp139 DISCARD** evening_peak. Val **22.425** missed Exp136 22.259. Test **20.501**. Weekday 18-21 29.66→**29.68** flat; pred_d +2.67→**+4.42**. Hour 20 32.19 stayed. 2013 val inverted.

1h champion unchanged: Exp97. MLP **15/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp140)

New diagnosis: SE Iws>=10 n=1483 RMSE **24.43 vs CatBoost 23.63** vs persist 25.65, need +1.84 pred_d **−0.39** (26.5% of Exp136 SSE; wrong-sign over-clean).

**Exp140 DISCARD** se_iws. Val **22.439** missed Exp136 22.259. Test **20.519**. SE Iws>=10 24.43→**24.53**; pred_d −0.39→**+0.12**. Onset 110.39→108.52. 2013 val inverted.

1h champion unchanged: Exp97. MLP **16/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp141)

New diagnosis: delta6>20 n=2457 RMSE **25.92 vs CatBoost 26.91** vs persist 27.93, need +1.17 pred_d **−0.85** (49.4% of Exp136 SSE; mean-reverts a still-building 6h episode).

**Exp141 DISCARD** pm25_delta6. Val **22.356** missed Exp136 22.259. Test **20.274** new 2014 best. delta6>20 25.92→**25.60**; pred_d stayed **−0.87**. 2013 val inverted.

1h champion unchanged: Exp97. MLP **17/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp142)

New diagnosis: lag1>=250 still-rising n=276 RMSE **33.74 vs CatBoost 38.98** vs persist 29.76, need +21.38 pred_d **−1.96** (9.4% of Exp136 SSE; loses persist, wrong-sign drop).

**Exp142 DISCARD** is_severe. Val **22.438** missed Exp136 22.259. Test **20.469**. Rising-severe 33.74→**35.23**; pred_d −1.96→**−3.74**. Hypothesis inverted.

1h champion unchanged: Exp97. MLP **18/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp143)

New diagnosis: just-left-NW n=522 Iws mean **1.95** RMSE **20.07 vs persist 22.63**, need −3.70 pred_d **−1.03** (6.3% of Exp136 SSE; Iws reset forgets fetch). persist>=150 n=97 need **−13.98** pred_d **−5.32**.

**Exp143 DISCARD** cbwd_prev_NW. Val **22.381** missed Exp136 22.259. Test **20.383**. Just-left-NW 20.07→**19.52**; pred_d −1.03→**−2.78**. 2014 slice held; 2013 val inverted.

1h champion unchanged: Exp97. MLP **19/50**. t+6 recipe remains Exp76.

## This fire (2026-08-19, Exp144)

New diagnosis: February n=597 RMSE **25.74 vs CatBoost 24.09** vs persist 26.01, need −0.12 pred_d **−3.14** (11.8% of Exp136 SSE; over-cleans mean 166.7). Feb persist>=150 n=262 RMSE **34.20** loses persist **33.74**.

**Exp144 DISCARD** is_janfeb. Val **22.528** missed Exp136 22.259. Test **20.671**. February 25.74→**25.99**; pred_d −3.14→**−2.22**. Hypothesis inverted on RMSE.

1h champion unchanged: Exp97. MLP **20/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp145)

New diagnosis: Iws 5-20 persist>=150 n=373 RMSE **40.49 vs CatBoost 38.50** vs persist 47.43 (18.3% of Exp136 SSE). Test Iws median **4.92** std **41.64** p99 **232** so Iws=10 is +0.12 sigma after z-score.

**Exp145 DISCARD** iws_clip100. Val **22.473** missed Exp136 22.259. Test **20.494**. Iws 5-20 persist>=150 40.49→**40.33** inert. log_iws already compressed the tail.

1h champion unchanged: Exp97. MLP **21/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp146)

New diagnosis: Wednesday n=1149 RMSE **25.99 vs CatBoost 25.07** vs persist 27.60, need +1.25 pred_d **−1.09** (23.2% of Exp136 SSE; midweek over-clean, wrong sign).

**Exp146 DISCARD** dow_sin. Val **22.716** missed Exp136 22.259. Test **20.826**. Wednesday 25.99→**25.90**; pred_d −1.09→**+0.19**. Thursday 19.00→**19.89**. 2013 val inverted hard.

1h champion unchanged: Exp97. MLP **22/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp147)

New diagnosis: cv inversion>=q75 n=486 RMSE **19.55 vs CatBoost 19.03** vs persist 20.77, need +0.58 pred_d **−1.67** (5.6% of Exp136 SSE; dry-calm over-clean).

**Exp147 DISCARD** cv_inv. Val **22.327** missed Exp136 22.259 (close). Test **20.573**. cv inv>=q75 19.55→**19.74**; pred_d −1.67→**−0.90**. Extra-feature ladder on Exp136 exhausted.

1h champion unchanged: Exp97. MLP **23/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp148)

New diagnosis: evening 18-21 persist>=150 n=246 RMSE **39.89 vs CatBoost 38.09** vs persist 44.60, need +3.80 pred_d **+1.92** (11.7% of Exp136 SSE; 3-layer under-ramps nested evening haze). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp148 DISCARD** extra hidden 256-128-64-32. Val **23.289** missed Exp136 22.259 hard (above 22.90 miss line). Test **21.330**. Evening persist>=150 39.89→**43.24**; pred_d +1.92→**+7.38** versus need +3.80 (over-ramped). Typical 7.21→**7.80**. Collapse 76.83→**86.28**. Onset 110.39→**106.91** now beats persist 107.80. Extra depth inverted like Exp128 width shrink.

1h champion unchanged: Exp97. MLP **24/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp149)

New diagnosis: crash persist>=150 and need<-50 n=110 RMSE **86.06 vs CatBoost 81.81** vs persist 108.97, need −95.34 pred_d **−25.16** (24.4% of Exp136 SSE; homoscedastic Smooth-L1 captures 26% of the drop). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp149 DISCARD** hetero_loss. Val **22.771** missed Exp136 22.259. Test **21.104**. Crash 86.06→**92.61**; pred_d −25.16→**−19.41** versus need −95.34 (captured even less). Typical 7.21→**7.49**. Collapse 76.83→**81.72**. Onset 110.39→**110.09** still loses persist 107.80. Hypothesis inverted.

1h champion unchanged: Exp97. MLP **25/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp150)

New diagnosis: rain persist>=100 n=79 RMSE **38.52 vs CatBoost 33.16** vs persist 44.20, need −14.53 pred_d **−8.62** (3.5% of Exp136 SSE; clip=1.0 under-washes). Ir>0 24.06 vs CB 21.51. January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp150 DISCARD** grad_clip=0. Val **22.402** missed Exp136 22.259. Test **20.400** beat Exp136. Rain persist>=100 38.52→**39.15**; pred_d −8.62→**−8.69** flat. Crash 86.06→**80.40** now beats CB 81.81. Collapse 76.83→**72.68**. Typical 7.21→**7.50**. Unclipped steps helped crash but taxed rain and 2013 val.

1h champion unchanged: Exp97. MLP **26/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp151)

New diagnosis: build need>20 persist>=80 n=438 RMSE **51.59 vs CatBoost 51.10** vs persist 50.39, need +38.21 pred_d **+0.88** (34.9% of Exp136 SSE; 3e-4 persist-locked while haze still builds). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp151 DISCARD** Adam lr=1e-3. Val **22.449** missed Exp136 22.259. Test **20.516** tied Exp136. Build 51.59→**51.63**; pred_d +0.88→**+1.52** versus need +38.21 (more movement, no RMSE). Typical 7.21→**7.44**. January 30.96→**31.84**. Both Adam lr directions now closed (1e-4 underfit, 1e-3 inert).

1h champion unchanged: Exp97. MLP **27/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp152)

New diagnosis: Saturday n=1135 RMSE **20.98 vs CatBoost 20.35** vs persist 22.43, need +0.19 pred_d **−0.91** (14.9% of Exp136 SSE; p=0.2 over-cleans weekend). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp152 DISCARD** dropout=0.1. Val **22.290** missed Exp136 22.259 by 0.031 (close). Test **20.277** near Exp141 20.274 best 2014. Saturday 20.98→**20.80**; pred_d −0.91→**−0.08** versus need +0.19 (calibration held). Build 51.59→**50.79** now beats CB. January 30.96→**30.62**. Both dropout directions closed (0.3 taxed val, 0.1 close miss).

1h champion unchanged: Exp97. MLP **28/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp153)

New diagnosis: persist 80-150 n=2068 RMSE **22.91 vs CatBoost 22.65** vs persist 24.17, need +0.32 pred_d **−1.31** (32.5% of Exp136 SSE; batch-16 over-cleans moderate haze). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp153 DISCARD** batch_size=64. Val **22.638** missed Exp136 22.259. Test **20.744**. Persist 80-150 22.91→**22.81**; pred_d −1.31→**−0.89** versus need +0.32 (less over-clean, no val win). Typical 7.21→**7.30**. Quieter SGD helped the slice but taxed 2013 val.

1h champion unchanged: Exp97. MLP **29/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp154)

New diagnosis: stuck need>20 and |pred_d|<5 n=293 RMSE **50.33 vs CatBoost 50.03** vs persist 50.51, need +37.67 pred_d **+0.52** (22.2% of Exp136 SSE; L2 shrinks residual head to persist). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp154 DISCARD** weight_decay=0. Val **22.436** missed Exp136 22.259. Test **20.493** tied Exp136. Stuck 50.33→**50.08**; pred_d +0.52→**+1.23** versus need +37.67 (more movement, still persist-locked). Typical 7.21→**7.49**. MLP HP opposites (lr, dropout, batch, wd) now closed.

1h champion unchanged: Exp97. MLP **30/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp155)

New diagnosis: heating need>20 n=261 RMSE **55.12 vs CatBoost 55.19** vs persist 54.39, need +43.56 pred_d **+1.92** (23.7% of Exp136 SSE; winter builds persist-locked). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp155 DISCARD** heating_build. Val **22.518** missed Exp136 22.259. Test **20.963**. Heating need>20 55.12→**54.36** now beats persist; pred_d +1.92→**+2.79** versus need +43.56 (slice moved, overall val inverted). January 30.96→**31.26**. Onset 110.39→**108.41**.

1h champion unchanged: Exp97. MLP **31/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp156)

New diagnosis: collapse on rh>=q75 n=45 RMSE **71.72 vs CatBoost 65.80** vs persist 81.61, need −75.71 pred_d **−11.02** (6.9% of Exp136 SSE; humid crashes capture 15% of the drop). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp156 DISCARD** rh_iws. Val **22.430** missed Exp136 22.259. Test **20.399** beat Exp136. Humid collapse 71.72→**73.39**; pred_d −11.02→**−9.12** versus need −75.71 (captured even less). Extra features including heating_build and rh_iws exhausted.

1h champion unchanged: Exp97. MLP **32/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp157)

New diagnosis: Iws>=50 n=746 RMSE **10.46 vs CatBoost 9.92** vs persist 12.61 (2.4% of Exp136 SSE; linear storm tail collinear with log_iws; Iws median 4.92 std 41.64 p99 232). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp157 DISCARD** drop Iws keep log_iws. Val **22.336** missed Exp136 22.259. Test **20.425**. Iws>=50 10.46→**10.51**; pred_d −0.36→**+0.27**. Iws 5-20 persist>=150 40.49→**39.59**. Raw Iws still useful on 2013 val.

1h champion unchanged: Exp97. MLP **33/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp158)

New diagnosis: Is>0 n=35 RMSE **15.32 vs CatBoost 12.05** vs persist 18.17 (0.25% of Exp136 SSE; test Is 99.56% zero, mean 0.037 std 0.74 p99 0 max 23 maps to ~25-sigma after z-score; snow pred_d **−6.66** vs need −2.57). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp158 DISCARD** drop Is keep Iws. Val **22.394** missed Exp136 22.259. Test **20.395**. Is>0 15.32→**14.56**; pred_d −6.66→**−3.67** versus need −2.57 (slice less over-clean). Typical 7.21→**7.25**. 2013 val has 65 snow hours vs 35 on 2014. Ir>0 n=260 RMSE 24.06 vs CB 21.51, need −6.30 pred_d −4.29 (do not drop Ir).

1h champion unchanged: Exp97. MLP **34/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp159)

New diagnosis: PRES>=1025 persist>=150 n=413 RMSE **38.33 vs CatBoost 42.89** vs persist 40.56 (18.2% of Exp136 SSE; need −3.20 pred_d **−8.47**; PRES–TEMP corr −0.84). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp159 DISCARD** drop PRES keep TEMP. Val **22.437** missed Exp136 22.259. Test **20.354**. Dirty anticyclone 38.33→**37.60**; pred_d −8.47→**−7.66** versus need −3.20 (slice less over-clean). Typical 7.21→**7.20**. January 30.96→**30.51**. Onset 110.39→**109.08** still loses persist 107.80. Drop-raw-weather now three DISCARDs (Iws, Is, PRES).

1h champion unchanged: Exp97. MLP **35/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp160)

New diagnosis: Sat persist>=150 n=284 RMSE **34.51 vs CatBoost 32.94** (need −2.94 pred_d **−4.25** over-clean) vs Sun persist>=150 n=227 RMSE **31.83 vs 33.48** (need −10.70 pred_d **−8.52** under-clean). is_weekend is a deterministic function of dow 5–6 (corr 0.79). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp160 DISCARD** drop is_weekend keep dow. Val **22.492** missed Exp136 22.259. Test **20.428**. Sat dirty 34.51→**34.38**; pred_d −4.25→**−3.97**. Sun dirty 31.83→**32.44**; pred_d −8.52→**−7.25** (more under-clean). Typical 7.21→**7.22**. January 30.96→**30.70**. Onset 110.39→**109.08** still loses persist 107.80.

1h champion unchanged: Exp97. MLP **36/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp161)

New diagnosis: inversion_spread equals TEMP−DEWP exactly; corr with rh_magnus **−0.954**. inv q4 n=2220 RMSE **22.17 vs CatBoost 22.39** (32.6% of Exp136 SSE; need −0.87 pred_d **−2.42** dry well-mixed over-clean). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp161 DISCARD** drop inversion_spread keep TEMP/DEWP. Val **22.487** missed Exp136 22.259. Test **20.455**. inv q4 22.17→**21.64**; pred_d −2.42→**−2.40** (over-clean barely moved). Saturated inv<=2 16.93→**17.38**. Typical 7.21→**7.27**. January 30.96→**31.13**. Onset 110.39→**111.13** still loses persist 107.80.

1h champion unchanged: Exp97. MLP **37/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp162)

New diagnosis: Feb persist>=150 n=262 RMSE **34.20 vs CatBoost 31.39** vs persist 33.74 (need −2.03 pred_d **−7.89**; is_heating–month_sin corr only 0.20; is_heating–TEMP −0.77). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp162 DISCARD** drop is_heating keep month_sin. Val **22.426** missed Exp136 22.259. Test **20.333**. Feb dirty 34.20→**33.66**; pred_d −7.89→**−5.75**. Jan dirty pred_d −10.16→**−12.23**. Typical 7.21→**7.39**. January 30.96→**30.60**. Onset 110.39→**109.49** still loses persist 107.80. Collinear-derived drops now three DISCARDs (is_weekend, inversion_spread, is_heating).

1h champion unchanged: Exp97. MLP **38/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp163)

New diagnosis: cbwd one-hots sum to 1.0 exactly. cv persist>=150 n=505 RMSE **26.40 vs CatBoost 28.95** vs persist 27.68 (10.5% of SSE; need +1.28 pred_d **−0.76** dirty calm under-build; cv Iws median 1.78 vs non-cv 8.94). January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp163 DISCARD** drop cbwd_cv keep directed winds. Val **22.350** missed Exp136 22.259. Test **20.556**. cv dirty RMSE stayed 26.40; pred_d −0.76→**−0.09**. cv overall pred_d +0.62→**+1.36** versus need +2.42. Typical 7.21→**7.34**. January 30.96→**31.27**. Onset 110.39→**110.22** still loses persist 107.80.

1h champion unchanged: Exp97. MLP **39/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp164)

New diagnosis: need>=30 build n=309 RMSE **65.12 vs persist 64.39** vs CB 64.51 (39.2% of Exp136 SSE; need +50.54 pred_d **+1.23** persist-locked jumps). Typical |need|<=10 already beats CB 7.21 vs 8.35. January 30.96 vs JJA 13.96. Onset 110.39 vs persist 107.80. Hour 20 32.19. Val 22.259 vs test 20.509 is the bottleneck.

**Exp164 DISCARD** vs Exp97 (val **22.180** vs 22.167, Δ0.013 near-miss). Test **20.201** new 2014 best. Beats Exp136 val 22.259 and test 20.509. Builds 65.12→**65.98**; pred_d +1.23→**+0.97** (hypothesis inverted on the slice). |need|>=80 135.18→**128.15** beats CB 131.19. Typical 7.21→**7.53**. January 30.96→**31.90**. Onset 110.39→**111.26** still loses persist 107.80. MLP recipe updates to Exp164 hidden 512-256-128.

1h champion unchanged: Exp97. MLP **40/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp165)

New diagnosis: need>=30 and accel<=0 n=121 RMSE **81.91 vs persist 78.35** vs CB 81.09 (25.0% of Exp164 SSE; need +55.19 pred_d **−1.98** second-diff sign-flip at inflection onsets). January 31.90 vs JJA 13.98. Onset 111.26 vs persist 107.80. Hour 20 32.40. Val 22.180 vs test 20.201; 0.013 shy of Exp97.

**Exp165 DISCARD** drop pm25_accel. Val **22.448** missed Exp164 22.180. Test **20.467**. Contra-accel 81.91→**79.90**; pred_d −1.98→**+0.68**. Builds 65.98→**63.55** beat persist. Onset 111.26→**107.97**. |need|>=80 128.15→**134.07**. Typical 7.53→**7.36**. January 31.90→**31.03**. Keep accel. Recipe remains Exp164.

1h champion unchanged: Exp97. MLP **41/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp166)

New diagnosis: typical |pred_d|>=8 n=669 RMSE **15.37 vs persist 5.90** vs Exp136 13.25 (4.87% of Exp164 SSE; mean |d| **13.51** on hours that need ~4). January 31.90 vs JJA 13.98. Onset 111.26 vs persist 107.80. Hour 20 32.40. Val 22.180 vs test 20.201; 0.013 shy of Exp97.

**Exp166 DISCARD** LayerNorm. Val **22.442** missed Exp164 22.180. Test **21.338**. Typical |d|>=8 15.37→**18.56**. Typical 7.53→**9.03**. January 31.90→**36.70** loses persist 33.58. Onset 111.26→**112.18**. Keep LayerNorm off. Recipe remains Exp164.

1h champion unchanged: Exp97. MLP **42/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp167)

New diagnosis: dirty-stable persist>=150 |need|<=10 n=654 RMSE **13.13 vs persist 5.95** vs Exp136 12.40 (3.47% of Exp164 SSE; pred_d **−3.91** vs need +0.34; 512-wide trunk overwrites lag-1). January 31.90 vs JJA 13.98. Onset 111.26 vs persist 107.80. Hour 20 32.40. Val 22.180 vs test 20.201; 0.013 shy of Exp97.

**Exp167 KEEP** residual skips. Val **21.972** beat Exp97 22.167 and Exp164 22.180. Test **20.072** new 2014 best. Dirty-stable 13.13→**11.99**; pred_d −3.91→**−1.78**. Typical 7.53→**7.14**. January 31.90→**31.22**. Onset 111.26→**110.28** still loses persist 107.80. Skill vs persist-1 **+10.06%**. First 1h KEEP since Exp97. Champion is now Exp167 residual MLP.

MLP **43/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp168)

New diagnosis: onset need>50 n=83 RMSE **110.28 vs persist 107.80** (31.51% of Exp167 SSE; need **+87.40** pred_d **−0.60**; 84% of onsets have pred_d<10 and 40% predict below lag-1). Smooth-L1 beta=1 is MAE at MAE 11.06 so 5117 typical hours drown 83 onsets with equal unit gradients. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Val 21.972 vs test 20.072 is the bottleneck.

**Exp168 DISCARD** huber_beta=20. Val **22.581** missed Exp167 21.972. Test **20.752**. Onset 110.28→**110.64**; pred_d −0.60→**−1.06** versus need +87.40 (hypothesis inverted). Typical 7.14→**8.38**. Dirty-stable 11.99→**12.71**; pred_d −1.78→**−4.39**. Quadratic loss taxed the residual identity path instead of unlocking jumps.

1h champion unchanged: Exp167. MLP **44/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp169)

New diagnosis: onset plus SE persist 50-150 n=21 RMSE **157.60 vs persist 156.55** (16.29% of Exp167 SSE; need **+115.48** pred_d **+2.09**; pred 96.8 vs actual 210.1). se_iws already failed as a speed product. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp169 DISCARD** se_pm25. Val **22.117** missed Exp167 21.972. Test **20.133**. Onset 110.28→**108.75**; pred_d −0.60→**+1.30**. Onset SE persist 50-150 157.60→**156.58**; pred_d +2.09→**+3.88** versus need +115.48 (still persist-locked). Typical 7.14→**7.27**. January 31.22→**30.87**. Local lag1×SE is not the upwind plume payload.

1h champion unchanged: Exp167. MLP **45/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp170)

New diagnosis: January onset n=18 RMSE **139.25 vs persist 127.93** (10.90% of Exp167 SSE; need **+107.72** pred_d **−9.78** so the 128-d head subtracts ~10 µg on hours that jump +108). Typical |need|<=10 n=5117 RMSE **7.14 vs persist 5.08**. Hidden residual did not pin the OUTPUT to lag-1. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24 (11.10% of SSE). Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp170 DISCARD** persist_residual ŷ=lag1+Δ. Val **22.072** missed Exp167 21.972. Test **20.144**. Typical 7.14→**6.80** (closer to persist 5.08). Dirty-stable 11.99→**10.85**; pred_d −1.78→**−0.03**. January onset 139.25→**139.34**; pred_d −9.78→**−9.10** versus need +107.72 (anti-jump survived). Collapse 73.22→**74.72**. JJA 13.87→**14.11**. Output identity helped calm hours; the delta head still subtracts ~9 µg on January jumps and collapse/JJA paid the val tax.

1h champion unchanged: Exp167. MLP **46/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp171)

New diagnosis: January onset pred_d<0 n=9 RMSE **168.63 vs persist 141.36** (7.99% of Exp167 SSE; need **+113.78** pred_d **−32.46**). Collapse NW n=71 RMSE 74.80 beats persist 102.50, but January onset NW n=6 RMSE **116.14 vs persist 100.07** with pred_d **−19.26** versus need +89.50 (71-to-6 NW vote teaches cleanout). January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp171 DISCARD** underpred_weight=2. Val **22.643** missed Exp167 21.972. Test **20.677**. January onset 139.25→**128.85**; pred_d −9.78→**+3.29** (anti-jump flipped). Onset 110.28→**103.77** now beats persist 107.80. Typical 7.14→**7.97**; pred_d 0.94→**4.77**. Collapse 73.22→**82.71**. JJA 13.87→**14.92** loses persist 14.83. Global **+4.34** µg bias taxed val. Slice moved; global under-pred tax is the wrong tool.

1h champion unchanged: Exp167. MLP **47/50**. t+6 recipe remains Exp76.

## This fire (2026-08-20, Exp172–Exp173)

New diagnosis: onset NW RH<30 n=5 RMSE **120.73 vs persist 103.16** (2.28% of Exp167 SSE; need **+90.80** pred_d **−21.11**). January NW RH<30 persist>=80 n=26 RMSE 59.05, pred_d **−33.45** vs need −17.92 (dry NW over-cleaned). Collapse NW RH<30 already beats persist 114.25 at 70.77. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp172 DISCARD** stagn_onset (concurrent numbering collision; val **21.9995** near-miss Δ0.028, test **20.018** new 2014 best). Collapse 73.22→**71.71**. Typical 7.14→7.17. Onset NW RH<30 inert (dummy is zero on NW). January dirty dry NW 59.05→**60.88**. Predictions file lost in the collision.

**Exp173 DISCARD** nw_rh. Val **22.074** missed Exp167 21.972. Test **20.093**. Onset NW RH<30 120.73→**116.75**; pred_d −21.11→**−16.92**. January onset NW RH<30 147.42→**142.14**; pred_d −35.05→**−28.53**. Typical 7.14→**7.36**. JJA 13.87→**13.97**. Collapse 73.22→**74.58**. Slice moved a little; typical tax killed val.

**Exp174 DISCARD** onset_underpred_weight=2 (concurrent). Val **22.057**. Test **20.068**. Onset 110.28→**109.34**; pred_d −0.60→**+0.79**. January onset pred_d −9.78→**−6.78**. Typical 7.14→**7.24**. Localized onset weight was nearly inert versus Exp171 global weight. **MLP 50/50 complete.**

A concurrent mixup_alpha=0.2 also logged as Exp174 DISCARD (val **22.014**, test **20.113**). 1h champion unchanged: Exp167. MLP **50/50**. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp175)

New diagnosis: hour-20 SE persist>=80 n=74 RMSE **60.62 vs persist 61.42** (8.49% of Exp167 SSE; need **+14.47** pred_d **+5.69**). The 16 hour-20 SE persist>=80 need>20 hours hold 8.26% of SSE at 128.62 vs persist 129.94 with pred_d only **+10.29** versus need **+64.31**. Residual GELU cannot route hour×SE×dirty-lag. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp175 DISCARD** FT-Transformer Gorishniy 2021 paper default (d_model 64, n_heads 4, n_layers 3, batch 32, lr 1e-4). Val **22.698** missed Exp167 21.972 (inside 21.70–24.50). Test **23.130** missed 20.072 and persist **22.316** (inside 19.8–23.6; skill negative). Hour-20 SE persist>=80 60.62→**61.66**; pred_d 5.69→**3.72** versus need +14.47 (attention under-jumped). Typical 7.14→**10.22**. Dirty-stable 11.99→**24.29**; pred_d −1.78→**−4.20**. January 31.22→**42.85** loses persist 33.58. Onset 110.28→**119.59**; pred_d −0.60→**−6.95**. CLS readout without lag-1 identity overwrote persistence.

1h champion unchanged: Exp167. FT **1/50**. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp176)

New diagnosis: heating dirty-stable persist>=150 |need|<=10 n=269 RMSE **15.66 vs persist 6.19** (2.06% of Exp167 SSE; need **−0.09** pred_d **−4.08**). Residual MLP already over-cleans stagnant heating hours; Exp175 three-layer FT made dirty-stable 11.99→24.29 and typical 7.14→10.22. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp176 DISCARD** FT n_layers=1. Val **25.443** missed Exp167 21.972 and fell outside 21.80–24.20. Test **25.954** missed persist **22.316** and Exp175 23.130 (outside 20.2–23.4). Heating dirty-stable 15.66→**44.22** vs Exp175 35.80; pred_d −4.08→**−14.08**. Typical 7.14→**12.12**. Dirty-stable 11.99→**30.31**. January 31.22→**48.70**. Onset pred_d −0.60→**−14.70**. One layer underfit and buried lag-1 more, not less.

1h champion unchanged: Exp167. FT **2/50**. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp177)

New diagnosis: typical |need|<=10 and |pred_d|>=5 n=1514 RMSE **10.54 vs persist 5.48** (5.26% of Exp167 SSE; need **+0.89** pred_d **+0.93**). Residual MLP already over-moves 1514 calm hours. Exp175 n_layers=3 typical 10.22; Exp176 n_layers=1 typical 12.12. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp177 DISCARD** FT n_layers=2. Val **23.222** missed Exp167 21.972 (inside 22.10–25.20) and missed Exp175 22.698 so two layers did not beat both prior depths. Test **23.513** missed persist 22.316 (inside 21.4–25.4). Typical |pred_d|>=5 10.54→**16.72** vs Exp175 16.48. Typical 7.14→**10.41**. Dirty-stable 11.99→**25.05**. January 31.22→**42.05**. Onset pred_d −0.60→**−7.61**. Middle depth interpolated 1 and 3; persist stayed buried. **FT depth axis closed (3 DISCARDs).**

1h champion unchanged: Exp167. FT **3/50**. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp178)

New diagnosis: dirty-stable NW persist>=150 |need|<=10 n=156 RMSE **17.54 vs persist 6.18** (1.50% of Exp167 SSE; need **−0.08** pred_d **−9.17**). Residual MLP subtracts 9 µg on already-dirty NW hours; Post-LN FT buried lag-1 further (dirty-stable 11.99→24.29). January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck. FT depth {1,2,3} closed — rethink architecture.

**Exp178 DISCARD** FT Pre-LN (norm_first=true) on paper-default 3-layer. Val **22.140** missed Exp167 21.972 (Δ0.168; inside 21.80–24.40) but beat Exp175 Post-LN 22.698. Test **20.674** beat persist **22.316** and Exp175 23.130 (inside 20.4–24.2). Dirty-stable NW 17.54→**20.63** vs Post-LN 33.82; pred_d −9.17→**−9.41** vs Post-LN −14.17. Typical 7.14→**7.96** vs Post-LN 10.22. January 31.22→**34.77** vs Post-LN 42.85. Onset pred_d −0.60→**−0.94** vs Post-LN −6.95. Pre-LN restored lag-1 versus Post-LN; did not beat residual MLP. **Best isolated FT.**

1h champion unchanged: Exp167. FT **4/50**. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp179)

New diagnosis: JJA typical |need|<=10 n=1327 RMSE **5.78 vs persist 5.22** (1.38% of Exp167 SSE; need **+0.53** pred_d **+1.44**). Residual MLP already over-moves easy summer hours; Exp178 Pre-LN JJA 13.87→14.15 and typical 7.14→7.96 with encoder dropout 0.1. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp179 DISCARD** FT Pre-LN dropout=0. Val **22.200** missed Exp167 21.972 and Exp178 22.140 (inside 21.70–22.80). Test **20.509** beat Exp178 20.674 (inside 20.20–21.40). JJA typical 5.78→**5.89** vs Exp178 6.18; pred_d +1.44→**+1.40** vs Exp178 +2.28 (slice moved). Typical 7.14→**7.61** vs Exp178 7.96. Hour 20 32.68→**33.22** vs Exp178 32.56. Dropout-off helped 2014 and JJA typical but taxed 2013 val, the composite bottleneck.

1h champion unchanged: Exp167. FT **5/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp180)

New diagnosis: weekend typical |need|<=10 n=1435 RMSE **8.10 vs persist 5.19** (2.94% of Exp167 SSE; need **+0.49** pred_d **+0.92**). Weekday typical 6.73 vs persist 5.03. Weekend calm hours are the extra identity leak. Exp179 dropout=0 taxed 2013 val 22.200. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp180 DISCARD** FT Pre-LN dropout=0.2. Val **22.568** missed Exp167 21.972 and Exp178 22.140 (inside 21.70–22.90). Test **21.486** missed Exp178 20.674 (inside 20.40–21.80). Weekend typical 8.10→**7.62** vs Exp178 8.18 (slice moved, beat MLP on that slice) but typical 7.14→**8.18** and dirty-stable 11.99→**17.03**. January 31.22→**36.83**. Stronger dropout damped weekend calm and over-regularized January/dirty-stable.

1h champion unchanged: Exp167. FT **6/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp181)

New diagnosis: hour-9 persist>=80 n=166 RMSE **19.48 vs persist 18.55** (1.97% of Exp167 SSE; need **−1.52** pred_d **−2.89**). Morning dirty hours over-clean; batch-32 SGD noise can shove lag-1. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp181 DISCARD** FT Pre-LN batch_size=64. Val **23.039** missed Exp167 21.972 and Exp178 22.140 (outside 21.70–22.80). Test **21.597**. Hour-9 persist>=80 19.48→**20.19**; pred_d −2.89→**+0.96** (over-clean flipped to over-dirty). Typical 7.14→**8.15**; pred_d +0.94→**+2.60**. Dirty-stable pred_d −1.81→**+3.53**. Global bias **+1.98**. Larger batch biased predictions up, not quieter identity.

1h champion unchanged: Exp167. FT **7/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp182)

New diagnosis: DJF persist>=150 |need|<=10 n=207 RMSE **16.68 vs persist 6.07** (1.80% of Exp167 SSE; need **−0.07** pred_d **−5.60**). Winter dirty-stable over-cleans lag-1; Exp178 is worse at 23.55 with pred_d −4.92. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp182 DISCARD** FT Pre-LN weight_decay=1e-4. Val **22.400** missed Exp167 21.972 and Exp178 22.140 (inside 21.70–22.80). Test **20.746** missed Exp167 20.072 and Exp178 20.674 (inside 20.30–21.40). Prediction HIT. DJF persist>=150 |need|<=10 16.68→**24.75** vs Exp178 23.55; pred_d −5.60→**−7.47** versus need −0.07 (over-clean worsened). Typical 7.14→**7.90** vs Exp178 7.96. January 31.22→**34.27** loses persist 33.58. Onset pred_d −0.60→**−3.44**. Global bias **−1.72**. 10x AdamW decay pulled predictions down, not toward identity. **FT Pre-LN wd=1e-4 closed.**

1h champion unchanged: Exp167. FT **8/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp183)

New diagnosis: Ir>0 persist>=50 n=179 RMSE **28.75 vs persist 32.21** (4.62% of Exp167 SSE; need **−9.08** pred_d **−3.36**). Rain washout under-moves; Exp178 pred_d −1.48 worse. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp183 DISCARD** FT Pre-LN lr=3e-4. Val **22.477** missed Exp167 21.972 and Exp178 22.140 (inside 21.70–22.90). Test **20.952** missed Exp167 20.072 and Exp178 20.674 (inside 20.20–21.50). Prediction HIT. Ir>0 persist>=50 pred_d −3.36→**−3.67** vs Exp178 −1.48 (mean toward need −9.08) but RMSE 28.75→**29.74**. Typical 7.14→**7.79**. January 31.22→**34.34** loses persist 33.58. Onset pred_d −0.60→**−2.49**. Global bias **−2.54**. 3x lr pulled predictions down; rain RMSE did not fall. **FT Pre-LN lr=3e-4 closed.**

1h champion unchanged: Exp167. FT **9/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp184)

New diagnosis: hour2-4 persist>=80 n=521 RMSE **26.68 vs persist 30.40** (11.58% of Exp167 SSE; need **−5.20** pred_d **−6.13**). Nocturnal dirty hours; Exp178 28.83 pred_d −4.66. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp184 DISCARD** FT Pre-LN warmup=0. Val **22.892** missed Exp167 21.972 and Exp178 22.140 (outside 21.70–22.80). Test **21.312** missed Exp167 20.072 and Exp178 20.674 (inside 20.30–21.40). Prediction MISS on val/composite. Hour2-4 persist>=80 26.68→**29.01** vs Exp178 28.83; pred_d −6.13→**−7.81** versus need −5.20 (over-clean worsened). Typical 7.14→**8.42**. January 31.22→**34.90** loses persist 33.58. Onset pred_d −0.60→**−3.25**. Global bias **−3.78**. No-warmup pulled predictions down; nocturnal RMSE did not fall. **FT Pre-LN warmup=0 closed.**

1h champion unchanged: Exp167. FT **10/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-21, Exp185)

New diagnosis: cbwd_cv persist>=100 |need|<=10 n=392 RMSE **9.26 vs persist 5.88** (1.05% of Exp167 SSE; need **+0.72** pred_d **+2.30**). Calm-wind dirty-stable over-moves; Exp178 13.52 pred_d +2.74. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp185 DISCARD** FT Pre-LN warmup=20. Val **23.134** missed Exp167 21.972 and Exp178 22.140 (outside 21.70–22.90). Test **21.536** missed Exp167 20.072 and Exp178 20.674 (outside 20.30–21.50). Prediction MISS. cbwd_cv persist>=100 |need|<=10 9.26→**12.96** vs Exp178 13.52; pred_d +2.30→**−3.05** versus need +0.72 (over-move flipped to over-clean). Typical 7.14→**8.51**. January 31.22→**36.57** loses persist 33.58. Onset pred_d −0.60→**−6.24**. Global bias **−4.58**. Longer warmup pulled predictions down. **FT Pre-LN warmup axis closed {0,20}.** Schedule family three DISCARDs — rethink feature.

1h champion unchanged: Exp167. FT **11/50**. FT val recipe remains Exp178. t+6 recipe remains Exp76.

## This fire (2026-08-22, Exp186)

New diagnosis: prevNW then cv persist>=80 n=114 RMSE **29.35 vs persist 31.68** (3.07% of Exp167 SSE; need **−8.12** pred_d **−2.25**). Last-hour NW then calm under-cleans; Exp178 31.35 pred_d −2.43. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp186 DISCARD vs Exp167** FT Pre-LN add cbwd_prev_NW. Val **22.066** missed Exp167 21.972 (Δ0.094 NEAR-MISS) but beat Exp178 22.140 (inside 21.70–22.80). Test **20.483** missed Exp167 20.072 but beat Exp178 20.674 and Exp179 20.509 (inside 20.20–21.40). Prediction HIT. prevNW-then-cv pred_d −2.25→**−8.70** versus need −8.12 (mean matched); RMSE 29.35→**30.40** vs Exp178 31.35. Typical 7.14→**7.51** vs Exp178 7.96. January 31.22→**33.86**. Global bias **−2.04**. Token stepped washout. **New FT val recipe Exp186.** Feature axis open.

1h champion unchanged: Exp167. FT **12/50**. FT val recipe now Exp186. t+6 recipe remains Exp76.

## This fire (2026-08-22, Exp187)

New diagnosis: heating_night persist>=150 |need|<=10 n=166 RMSE **17.25 vs persist 6.09** (1.54% of Exp167 SSE; need **+0.23** pred_d **−4.23**). Stagnant heating nights over-clean; Exp186 22.35 pred_d −5.23. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp187 DISCARD** FT Pre-LN add heating_night on Exp186. Val **22.221** missed Exp167 21.972 and Exp186 22.066 (inside 21.70–22.50). Test **20.350** missed Exp167 20.072 but beat Exp186 20.483 (new best FT test; inside 20.20–21.30). Prediction HIT. heating_night persist>=150 |need|<=10 pred_d −4.23→**−3.33** vs Exp186 −5.23 (mean toward need +0.23) but RMSE 17.25→**22.41**. Typical 7.14→**7.52**. January 31.22→**32.51** beats persist 33.58. Onset 110.28→**109.07** pred_d −0.60→**+0.55**. Global bias **+0.37**. Token damped over-clean mean; 2013 val rose. **FT heating_night closed.** Recipe stays Exp186.

1h champion unchanged: Exp167. FT **13/50**. FT val recipe remains Exp186. t+6 recipe remains Exp76.

## This fire (2026-08-22, Exp188)

New diagnosis: rising P persist>=80 need<-20 n=128 RMSE **54.57 vs persist 72.02** (11.90% of Exp167 SSE; need **−54.38** pred_d **−15.93**). Rising-pressure dirty hours under-collapse; Exp186 50.36 pred_d −17.52. January 31.22 vs JJA 13.87. Hour 20 32.68 vs persist 33.24. Onset 110.28 vs persist 107.80. Val 21.972 vs test 20.072 is the bottleneck.

**Exp188 DISCARD** FT Pre-LN add pres_delta on Exp186. Val **22.539** missed Exp167 21.972 and Exp186 22.066 (outside 21.70–22.40). Test **20.913** missed Exp167 20.072 and Exp186 20.483 (inside 20.15–21.20). Prediction MISS on val/composite. rising P persist>=80 need<-20 54.57→**53.89** vs Exp186 50.36; pred_d −15.93→**−16.41** vs Exp186 −17.52 versus need −54.38 (did not step). Typical 7.14→**7.92**. January 31.22→**33.77**. Global bias **−2.69**. Token did not help synoptic collapse. **FT pres_delta closed.** Recipe stays Exp186.

1h champion unchanged: Exp167. FT **14/50**. FT val recipe remains Exp186. t+6 recipe remains Exp76.

## Next (original process)

1. Isolate **FT-Transformer** (14/50) from Exp186 Pre-LN + cbwd_prev_NW. Feature axis open. Next try **add is_morning**. Do not drop cbwd_prev_NW. Do not retry heating_night/pres_delta. Do not retry warmup 15/25. Do not retry lr 2e-4/5e-4. Do not retry wd 5e-5/2e-4/0. Do not retry batch 48/64/128. Do not retry dropout 0/0.2. Do not revert Post-LN. Do not mix MLP HPs into FT.
2. Do not retry n_layers=4/6 or d_model 32/96 as a persist fix. Do not retry nw_rh, stagn_onset, persist_residual, se_pm25, huber_beta 10/40/50.
3. 1h champion remains Exp167 until composite beats −21.972.









