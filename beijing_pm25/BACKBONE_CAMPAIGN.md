# Per-backbone campaign tracker (original Autoresearch mandate)

Source: `generalized_ml_autoresearch/templates/CLAUDE_template.md` § Per-Backbone N-Experiment Mandate
and `skills/ml-autoresearch-setup/SKILL.md` Step 8–11.

**Honest audit after Exp36:** this project did **not** follow the original skill through Exp31; isolation resumed at Exp32.

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
| lightgbm | 20, 25, 29–36 (10) | Ke 2017; Rashmi 2015; Geurts 2006 | No |
| catboost | 21, 26 (2) | Prokhorenkova 2018 defaults only | No |
| mlp / linear / ridge | 0 | — | No |
| ft_transformer / tabnet / tabtransformer / saint | 0 | — | No |
| lstm | 0 | — | No |

## Recovery (from Exp32; after Exp36)

Isolation: **stay on LightGBM** (current champion Exp30) until 50 LGB experiments.
Do not start CatBoost / MLP / FT-Transformer until that cycle is snapshotted to `code_versions/lightgbm_final/`.

Within LightGBM, paper queue (one publication / one change per experiment):

1. ~~Ke et al. 2017 §3.2 GOSS (`boosting_type=goss`)~~ Exp32 DISCARD
2. ~~Rashmi & Gilad-Bachrach 2015 DART~~ Exp33 DISCARD (no early stop; do not retune drop_rate)
3. ~~Huber default alpha 0.9~~ Exp34 DISCARD (do not retry mae/tweedie/quantile without scale)
4. ~~Geurts extra-trees~~ Exp35 DISCARD
5. ~~Ke min_data_in_leaf=100~~ Exp36 DISCARD (do not retry 50/200)
6. Shi et al. linear trees ← **next**
7. Domain papers (onset/collapse, t+6) only as LightGBM feature changes
8. Multi-seed variance on the LGB champion

Then isolated cycles: CatBoost 50 → MLP 50 → FT-Transformer 50 → TabNet if time.
