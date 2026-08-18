# Per-backbone campaign tracker (original Autoresearch mandate)

Source: `generalized_ml_autoresearch/templates/CLAUDE_template.md` § Per-Backbone N-Experiment Mandate
and `skills/ml-autoresearch-setup/SKILL.md` Step 8–11.

**Honest audit after Exp67:** this project did **not** follow the original skill through Exp31; isolation resumed at Exp32.

## Mandate vs what happened

| Rule | Required | What Exp1–31 actually did |
|---|---|---|
| Many backbones | Tier 1 + Tier 2 + GBM trio, isolated | Almost only XGBoost, then jumped |
| Isolation | Finish 50 on one backbone, snapshot, then next | Interleaved XGB/LGB/CatBoost |
| N per backbone | 50, no early stop | XGB 24, LGB 5, CatBoost 2, others 0 |
| Many papers per backbone | Latest SOTA + variants, each cited | Mostly Chen & Guestrin 2016 HP knobs |
| Snapshot | `code_versions/<backbone>_start/` before each | Only `v1_original/` existed |
| Never copy configs | Each backbone has its own recipe | LGB/Cat copied XGB-ish knobs |

## Experiment counts by backbone (Exp1–31)

| Backbone | Exps | Distinct publications used | Cycle complete? |
|---|---:|---|---|
| xgboost | 1–19, 22–24, 27–28 (24) | Chen & Guestrin 2016; Liang 2015 (inversion feature) | No |
| lightgbm | 20, 25, 29–67 (41) | Ke 2017; Zheng 2015 KDD; Huang 2014 Nature; Chen 2016; Tang 2016 ACP | No |
| catboost | 21, 26 (2) | Prokhorenkova 2018 defaults only | No |
| mlp / linear / ridge | 0 | — | No |
| ft_transformer / tabnet / tabtransformer / saint | 0 | — | No |
| lstm | 0 | — | No |

## Recovery (from Exp32; after Exp67)

Isolation: **stay on LightGBM** (1h champion Exp30; t+6 side ladder Exp39) until 50 LGB experiments.
Do not start CatBoost / MLP / FT-Transformer until that cycle is snapshotted to `code_versions/lightgbm_final/`.

Within LightGBM, paper queue (one publication / one change per experiment):

1. ~~Ke et al. 2017 §3.2 GOSS (`boosting_type=goss`)~~ Exp32 DISCARD
2. ~~Rashmi & Gilad-Bachrach 2015 DART~~ Exp33 DISCARD
3. ~~Huber default alpha 0.9~~ Exp34 DISCARD
4. ~~Geurts extra-trees~~ Exp35 DISCARD
5. ~~Ke min_data_in_leaf=100~~ Exp36 DISCARD
6. ~~Shi et al. linear trees~~ Exp37 DISCARD
7. ~~pm25_accel second difference~~ Exp38 NEAR-MISS DISCARD
8. ~~t+6 as-of-t-6 on same timestamps~~ Exp39 DISCARD on 1h gate, **skill +10.5% vs persist-6** (test 55.32 / 61.83)
9. ~~vent_index = Iws×inversion~~ Exp40 DISCARD
10. ~~Ke max_bin=127~~ Exp41 DISCARD
11. ~~pm25_roll6max~~ Exp42 DISCARD
12. ~~bagging_freq=1~~ Exp43 DISCARD (test 20.807, val 22.498)
13. ~~seed=1 noise floor~~ Exp44 DISCARD (val ±0.08)
14. ~~t+6 pm25_delta6~~ Exp45 DISCARD (redundant)
15. ~~t+6 num_leaves 31~~ Exp46 **side-KEEP** (val 58.37; 1h DISCARD)
16. ~~t+6 month_sin~~ Exp47 **side-KEEP** (val 58.14 / test 55.06)
17. ~~t+6 month_cos~~ Exp48 side-MISS (test 54.65, val 58.36)
18. ~~t+6 stagn_index~~ Exp49 DISCARD
19. ~~t+6 path_smooth=1~~ Exp50 DISCARD
20. ~~t+6 lr 0.02~~ Exp51 DISCARD
21. ~~t+6 feature_fraction 0.6~~ Exp52 DISCARD
22. ~~t+6 persist-6 residual target~~ Exp53 DISCARD (redundant with persist feature)
23. ~~t+6 Tweedie objective~~ Exp54 DISCARD (test 54.79, val 58.67; tail worse)
24. ~~t+6 pres_delta~~ Exp55 **side-KEEP** (val 58.04 / test 54.75)
25. ~~t+6 dewp_delta~~ Exp56 **side-KEEP** (val 57.66 / test 54.49)
26. ~~t+6 haze_hours6~~ Exp57 DISCARD (redundant with six lags)
27. ~~t+6 reg_lambda=1~~ Exp58 DISCARD (val 57.70)
28. ~~t+6 cbwd_prev_NW~~ Exp59 **side-KEEP** (val 57.60 / test 54.42) ← **current t+6 recipe**; snapshotted `lightgbm_t6`
29. ~~t+6 rain_mass~~ Exp60 DISCARD (Ir×persist redundant)
30. ~~t+6 bagging_freq=1~~ Exp61 DISCARD (val 57.74; late-dirty still +31)
31. ~~t+6 drop lag13-24~~ Exp62 DISCARD (test 53.84, val 58.05)
32. ~~t+6 regression_l1 MAE~~ Exp63 DISCARD (val 58.80; typical RMSE 32.50)
33. ~~t+6 doy_sin~~ Exp64 DISCARD (val 58.05; Jan onset still +21)
34. ~~t+6 heating_night~~ Exp65 DISCARD (val 57.65; night-onset still −7.1)
35. ~~t+6 reg_alpha=1~~ Exp66 DISCARD (val 57.72; wrong-sign still −24)
36. ~~t+6 num_leaves 15~~ Exp67 DISCARD (val 57.92; typical P>=150 still −20)
37. **Stay on Exp59; do not retry leaves<31; fill remaining LGB 9** ← **next**

Then isolated cycles: CatBoost 50 → MLP 50 → FT-Transformer 50 → TabNet if time.
