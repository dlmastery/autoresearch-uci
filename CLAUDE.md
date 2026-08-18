# AGENTS.md — Project Rules for grok-autoresearch (Beijing PM2.5 nowcast)

> Verbatim protocol from `dlmastery/autoresearch` + `environment_stats_talk/docs/autoresearch_protocol.md`.
> The only substitution: **Grok Build is the outer loop** (was Claude Code). Nothing else is relaxed.

## On Session Start (ALWAYS do this first)

You ARE the autoresearch loop. Grok Build is the outer loop — there is no separate Python agent.

1. Read `benchmarks/beijing_pm25/memory/project_autoresearch_checkpoint.md`.
2. Tail `benchmarks/beijing_pm25/autoresearch_results/experiment_log.jsonl` (last 3) and read `best_config.json`.
3. Resume the 7-step process (diagnose → cite → hypothesize → predict → run ONE experiment → analyze → checkpoint).
4. Start the dashboard once per session:
   `python -m http.server 8765 --directory C:/Users/abhir/grok-autoresearch/benchmarks/beijing_pm25/autoresearch_results`
   Tell the user: Dashboard at http://localhost:8765/dashboard.html
5. Run experiments via:
   `python C:/Users/abhir/grok-autoresearch/benchmarks/beijing_pm25/run_exp.py --config C:/Users/abhir/grok-autoresearch/benchmarks/beijing_pm25/config_expN.yaml --description "..."`
   Timeout 600 s.
6. If the user says "continue" or "keep going" — resume. Do not ask what to do.

## Hardware

- GPU: CPU is enough for XGBoost nowcast. Torch is CPU-only on this machine.
- Pin: runner calls `_pin_to_safe_cores` when `hardware.cpu_affinity` is set. Default 4 threads.
- Time budget: 600 s per experiment.
- 60-second cooldown after each experiment.

## Crash-Recovery Checkpointing (MANDATORY)

Checkpoint AFTER EVERY experiment and every 5 minutes of reasoning. A fresh Grok session reading ONLY this file + the checkpoint must resume.

Save to `benchmarks/beijing_pm25/memory/project_autoresearch_checkpoint.md`: champion, per-window RMSE, last KEEP/DISCARD, pasteable next command, diagnosis+cite+hypothesis, exhausted axes, full history table.

## Mindset

You are a top-tier researcher in **urban air-quality nowcasting**. Never guess. Never grid-search. Trace one sample from raw hour → lags → split → loss before you change anything. Measure, never assume.

## Hard Rules (NEVER violate)

### Reward Hacking

The chronological test set is FROZEN. Never shrink, shift, filter, or reshuffle test rows. If `len(test_idx)` or the test time range changes, the result is INVALID. Recency hypotheses may only drop early **train** rows via `min_train_idx`.

### Data Integrity

- Time-ordered data. **Random / stratified k-fold is forbidden.** Bergmeir, Hyndman & Koo 2018 IJF (arXiv:1905.11744). This rule was added after fraud_ecommerce showed a 0.27 AUC gap (stratified 0.7738 vs chronological 0.5098) on the same model.
- Zero train/val/test index overlap. `validate_no_overlap()` before every run.
- Features are causal: no `pm25[t]` or later in the feature row that predicts `pm25[t]`. Contemporaneous meteorology at t is allowed (nowcast contract, Exp07).
- Cache the UCI CSV. Never re-download mid-run.
- Load features once. Split once. Reuse.

### Evaluation Protocol

**holdout / order=time.** Last 20% of the time-sorted rows = test. Preceding 15% = val. Remainder = train.

Composite (frozen fingerprint):

```
composite = min(-val_RMSE, -test_RMSE) - 0.1 * n_windows_with_RMSE > 40
higher_is_better internally; KEEP iff composite_new > composite_champion
```

Primary metric: RMSE (µg/m³), lower better. Also log MAE and spike-F1 (PM2.5 > 75 µg/m³, China 24h Grade II / operational exceedance-ish hourly proxy).

ONE config change per experiment. Epoch/iteration-bound training, not wall-clock-bound.

## Autoresearch Agent Protocol (Karpathy-adapted)

1. Always start from the current best config. Modify ONE thing. Keep if composite improves. Revert if not.
2. Consecutive discards → stop and rethink the diagnosis, do not stop researching.
3. Mostly local tweaks; occasional radical change to escape a local optimum.
4. Cite every experiment. Not "let me try X."
5. The agent never stops. If out of ideas, read literature.
6. Checkpoint every few minutes.
7. Deep per-window failure analysis every iteration (calm vs haze-episode residuals).
8. Code changes are allowed with a principled reason. Snapshot to `code_versions/`.

## Research-Driven Experiment Selection (STRICT)

**Step 1 — Diagnose** the champion's weakness (episode spikes? night inversions? windy days?).
**Step 2 — Search the literature** (ventilation/PBL, GBM nowcast, lag structure).
**Step 3 — Hypothesize** with a mechanism and a numeric prediction range.
**Step 4 — Run ONE experiment.**
**Step 5 — Analyze against prediction.**
**Step 6 — Document** (JSON + journal + summary).
**Step 7 — Checkpoint.**

## Monotonic Quality Progression

Never run an unjustified experiment. 3+ DISCARDs ⇒ structural change, not another lr. Do not rewrite the composite, the split, or the primary metric mid-project without a `RULE_CHANGE` in the checkpoint.

Holistic DS (do not declare a ceiling early): 3 architectures (XGBoost + LightGBM + CatBoost or MLP), 5 feature directions (lags, wind/ventilation, calendar, interactions, episode flags), 2 data-level interventions, 1 calibration step. "Axis closed" requires 5+ distinct hypotheses within ±0.5 µg/m³ of the baseline.

## Citation Rigor + Reasoning Blob

Runner **refuses to launch** without a pre-run entry in `reasoning_annotations.json` that passes `core/reasoning.py`:

- diagnosis ≥ 60 words
- hypothesis ≥ 50 words and contains mechanism / because / per
- prediction ≥ 25 words and a numeric range (`A to B`)
- citations: year + venue token + arXiv or quoted title + relevance clause + ≥ 40 words

After the run, write verdict (KEEP / DISCARD / NEAR-MISS, ≥ 30 words) and learning (axis open/closed/next try, ≥ 40 words). Rewrite any `TODO-REWRITE` runner fallback before the next experiment.

## Winner archive + github.io pack (MANDATORY — match original repos)

Global champion only. On KEEP, the runner writes `best_config.json`. Every session that touches results must leave the Pages pack at Olivetti/FX depth, not a thin table:

- `dashboard.html` with links bar, literature ceiling, KEEP ladder, backbone 50-exp bars, residual month/hour charts, sortable/filterable log, 7-field reasoning + metrics + config + CSV tabs
- `forensic_report.md`, `audit_report.md` (14 sections), `autoresearch_report.md`, `FEATURES_AND_DATA.md`, `experiment_summary.md`, `research_journal.md`, `BACKBONE_CAMPAIGN.md`, `champion_diagnostics.json`
- `python beijing_pm25/build_public_artifacts.py` then `python beijing_pm25/sync_dashboard.py` before claiming the dashboard is updated

A dashboard that only shows an experiment table is a regression against `dlmastery.github.io/autoresearch`.

## Common mistakes

- Using k-fold on this series.
- Peeking at test to pick lags.
- Changing the test window to "recent winters only."
- Bundling xgboost+lightgbm+catboost as one backbone.
- Rewriting composite after seeing results.
- Launching without a reasoning blob.
- Stopping a backbone after 2–5 experiments or one paper's HP knobs.

## Per-Backbone N-Experiment Mandate (MANDATORY)

Every backbone gets a full **50-experiment** cycle. Isolation: finish one backbone, snapshot `code_versions/<backbone>_final/`, then start the next. Never interleave. Never copy another backbone's config.

| Tier | Backbone | Paper (start recipe) | Status after Exp31 |
|---|---|---|---|
| 1 | linear / ridge | Hoerl & Kennard 1970 | **0 / 50 — not started** |
| 1 | mlp | Gu, Kelly & Xiu 2020 RFS arXiv:1802.09003 | **0 / 50 — not started** |
| 2 | ft_transformer | Gorishniy et al. 2021 NeurIPS arXiv:2106.11189 | **0 / 50 — not started** |
| 2 | tabtransformer | Huang et al. 2020 arXiv:2012.06678 | **0 / 50 — not started** |
| 2 | tabnet | Arik & Pfister 2021 AAAI arXiv:1908.07442 | **0 / 50 — not started** |
| 2 | saint | Somepalli et al. 2021 arXiv:2106.01342 | **0 / 50 — not started** |
| 3 | xgboost | Chen & Guestrin 2016 KDD arXiv:1603.02754 | 24 / 50, mostly one paper's knobs |
| 3 | lightgbm | Ke et al. 2017 NeurIPS | 5 / 50 — **current champion, isolate here** |
| 3 | catboost | Prokhorenkova et al. 2018 NeurIPS arXiv:1706.09516 | 2 / 50 drive-bys, not a campaign |

Within each backbone, try **many research publications**, not only HP of the originating paper (GOSS, DART, Huber/Tweedie/quantile objectives, extra-trees, linear trees, domain papers). A backbone is done only after 50 experiments.

## Key constants

| Name | Value |
|---|---|
| Dataset | UCI 381 Beijing PM2.5 2010-01-01–2014-12-31 |
| Target | `pm25` µg/m³ at hour t (nowcast) |
| Split | chronological holdout 65/15/20 |
| Primary | RMSE |
| Composite | `min(-val,-test) - 0.1 * n_RMSE>40` |
| First backbone | xgboost (Chen & Guestrin 2016 KDD, arXiv:1603.02754) |
| Framework | `C:\Users\abhir\dlmastery-github\autoresearch\generalized_ml_autoresearch` |
