# Per-backbone campaign tracker (original Autoresearch mandate)

Source: `generalized_ml_autoresearch/templates/CLAUDE_template.md` § Per-Backbone N-Experiment Mandate
and `skills/ml-autoresearch-setup/SKILL.md` Step 8–11.

**Honest audit after Exp105:** this project did **not** follow the original skill through Exp31; isolation resumed at Exp32. LightGBM cycle is 50/50. Isolated CatBoost is 31/50. **1h champion remains Exp97 CatBoost.**

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
| lightgbm | 20, 25, 29–76 (50) | Ke 2017; Zheng 2015 KDD; Huang 2014 Nature; Chen 2016; Tang 2016 ACP; Geurts 2006; Shi 2018; Tie 2017 Sci Rep | Yes |
| catboost | 21, 26, 77–105 (31) | Prokhorenkova 2018; Chen 2016 early_stop inert; Ke 2017; Zheng 2015; Huang 2014 | No |
| mlp / linear / ridge | 0 | — | No |
| ft_transformer / tabnet / tabtransformer / saint | 0 | — | No |
| lstm | 0 | — | No |

## Recovery (from Exp32; after Exp76)

Isolation: LightGBM cycle is **50/50 complete**. Isolated CatBoost is **31/50** (**1h champion Exp97 CatBoost**; t+6 recipe Exp76). Snapshot `code_versions/catboost_start/`.
Do not start MLP / FT-Transformer until CatBoost is snapshotted.

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
28. ~~t+6 cbwd_prev_NW~~ Exp59 **side-KEEP** (val 57.60 / test 54.42)
29. ~~t+6 rain_mass~~ Exp60 DISCARD (Ir×persist redundant)
30. ~~t+6 bagging_freq=1~~ Exp61 DISCARD (val 57.74; late-dirty still +31)
31. ~~t+6 drop lag13-24~~ Exp62 DISCARD (test 53.84, val 58.05)
32. ~~t+6 regression_l1 MAE~~ Exp63 DISCARD (val 58.80; typical RMSE 32.50)
33. ~~t+6 doy_sin~~ Exp64 DISCARD (val 58.05; Jan onset still +21)
34. ~~t+6 heating_night~~ Exp65 DISCARD (val 57.65; night-onset still −7.1)
35. ~~t+6 reg_alpha=1~~ Exp66 DISCARD (val 57.72; wrong-sign still −24)
36. ~~t+6 num_leaves 15~~ Exp67 DISCARD (val 57.92; typical P>=150 still −20)
37. ~~t+6 extra_trees~~ Exp68 **side-KEEP** (val 57.50 / test 54.48)
38. ~~t+6 extra_trees min_data=50~~ Exp69 DISCARD (val 57.62; Feb typical still −41)
39. ~~t+6 extra_trees feature_fraction 1.0~~ Exp70 **side-KEEP** (val 57.44 / test 54.62)
40. ~~t+6 anticyclone PRES>=1020~~ Exp71 DISCARD (val 57.52; high-PRES increment still −54)
41. ~~t+6 extra_trees linear_tree~~ Exp72 **side-KEEP** (val 57.43 / test 54.33) ← **current t+6 recipe**
42. ~~t+6 max_bin=127~~ Exp73 DISCARD (val 57.44; Feb typical still −42)
43. ~~t+6 bagging_freq=1 on extra_trees+linear~~ Exp74 DISCARD (val 57.50; moist onset still −9)
44. ~~t+6 rh_magnus Magnus RH~~ Exp75 **side-KEEP** (val 57.19 / test 54.73; hour-6 blow-up 872)
45. ~~t+6 linear_lambda=1~~ Exp76 **side-KEEP** (val 57.16 / test 54.31; hour-6 53.55, blow-up 132) ← **current t+6 recipe**
46. ~~LightGBM 50/50 complete. Snapshot `lightgbm_final`. Isolated CatBoost start~~
47. ~~CatBoost Ordered on Exp30 features~~ Exp77 DISCARD (val 23.19; h20 Jan 31.30)
48. ~~CatBoost Plain on Exp30 features~~ Exp78 DISCARD / NEAR-MISS (val 22.472; h20 Jan 25.59) ← **current CatBoost recipe**
49. ~~CatBoost Plain lr=0.01~~ Exp79 DISCARD (val 22.587; Jan typical still −11)
50. ~~CatBoost Plain depth=4~~ Exp80 DISCARD (val 22.795; Jan typical −9.6, JJA tax)
51. ~~CatBoost Plain t+6 on Exp76 features~~ Exp81 DISCARD (val 57.86; test **53.93** beat Exp76)
52. ~~CatBoost t+6 l2_leaf_reg=10~~ Exp82 DISCARD (val 58.16; Sat typical flat)
53. ~~CatBoost t+6 bagging_temperature=2~~ Exp83 DISCARD (bit-identical to Exp81; inert)
54. ~~CatBoost t+6 drop rh_magnus~~ Exp84 DISCARD (val 58.07; RH<40 worse)
55. ~~CatBoost Ordered t+6~~ Exp85 DISCARD (val **57.66** closest CatBoost t+6, still miss)
56. ~~CatBoost Ordered t+6 random_strength=2~~ Exp86 DISCARD (val 57.68; test 54.25)
57. ~~CatBoost 1h Lossguide~~ Exp87 DISCARD (val 22.476; hour-10 worse)
58. ~~CatBoost 1h l2_leaf_reg=10~~ Exp88 DISCARD (val 22.488; **test 20.80** beat Exp30; hour-10 HIT)
59. ~~CatBoost 1h month_sin~~ Exp89 DISCARD (val 22.708; Jan cv flat; JJA tax)
60. ~~CatBoost 1h pm25_accel~~ Exp90 DISCARD (val 22.467; Jan cv worse)
61. ~~CatBoost 1h rh_magnus~~ Exp91 DISCARD / NEAR-MISS (val **22.449** best CatBoost val)
62. ~~CatBoost RH+l2=10~~ Exp92 DISCARD (val 22.596; test 20.82 beat Exp30)
63. ~~CatBoost 1h rsm=0.8 on Exp91~~ Exp93 DISCARD (val 22.569; test ties Exp30)
64. ~~CatBoost 1h cbwd_prev_NW on Exp91~~ Exp94 DISCARD (val 22.528; no-NW stagnant flat)
65. ~~CatBoost 1h random_strength=2 on Exp91~~ Exp95 DISCARD (val 22.451 inert vs Exp91 22.449)
66. **CatBoost 1h dewp_delta on Exp91** Exp96 **KEEP** (val 22.357 / test 20.881). New 1h champion.
67. **CatBoost 1h is_heating on Exp96** Exp97 **KEEP** (val 22.167 / test 20.735). New 1h champion.
68. ~~CatBoost 1h heating_night on Exp97~~ Exp98 DISCARD (val 22.343; Iws<2 worse)
69. ~~CatBoost 1h bagging_temperature=2 on Exp97~~ Exp99 DISCARD (bit-identical)
70. ~~CatBoost 1h rh_iws on Exp97~~ Exp100 DISCARD (val 22.178; Jan rh_iws q3 worse)
71. ~~CatBoost 1h heating_build on Exp97~~ Exp101 DISCARD (val 22.322; building-dirty worse)
72. ~~CatBoost 1h grow_policy=Depthwise on Exp97~~ Exp102 DISCARD (val 22.322; shard 68.80→77.22)
73. ~~CatBoost 1h pres_delta on Exp97~~ Exp103 DISCARD (val 22.352; onset dPRES>=1 158.68→157.78)
74. ~~CatBoost 1h min_data_in_leaf=20 on Exp97~~ Exp104 DISCARD (bit-identical)
75. ~~CatBoost 1h early_stopping_rounds=50 on Exp97~~ Exp105 DISCARD (bit-identical)
76. ~~CatBoost 1h drop dow on Exp97~~ Exp117 DISCARD (val 22.212 near-miss; Thursday worse)
77. ~~CatBoost 1h model_size_reg=1.0 on Exp97~~ Exp118 DISCARD (bit-identical)
78. ~~CatBoost 1h Bernoulli subsample=0.8 on Exp97~~ Exp119 DISCARD (val 22.231; Jan hour-1 74.63→74.97)
79. ~~CatBoost 1h border_count=128 on Exp97~~ Exp120 DISCARD (val 22.264; test 21.139; Jan PRES 36.25→38.85)
80. ~~CatBoost 1h nw_iws on Exp97~~ Exp121 DISCARD (val 22.240; H20 NW 18.55→17.49; val rose)
81. ~~CatBoost 1h is_morning on Exp97~~ Exp122 DISCARD (val 22.346; hour 8-9 18.16→18.00; val rose)
82. ~~CatBoost 1h dow_sin on Exp97~~ Exp123 DISCARD (val 22.360; Thursday 20.85→21.31)
83. ~~CatBoost 1h cv_inv on Exp97~~ Exp124 DISCARD (val 22.250; cv persist>=150 28.95→29.44)
84. ~~MLP default 256-128-64 on Exp97 features~~ Exp125 DISCARD (val 22.623; test 20.648; Jan 31.02)
85. ~~MLP dropout=0.3 on Exp125 recipe~~ Exp126 DISCARD (val 22.729; test **20.483** best 2014)
86. ~~MLP weight_decay=1e-4 on Exp125 recipe~~ Exp127 DISCARD 1h / MLP-val KEEP (val 22.528; test 20.773)
87. **Stay on MLP Exp127 recipe. Shrink width next. Do not retry dropout 0.4 or wd 1e-3. 1h champion Exp97.** ← **next**

Then isolated cycles: finish CatBoost 50 → MLP 50 → FT-Transformer 50 → TabNet if time.
