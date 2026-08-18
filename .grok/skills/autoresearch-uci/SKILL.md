---
name: autoresearch-uci
description: >
  Original Autoresearch hillclimb + github.io artifact pack for
  dlmastery/autoresearch-uci (UCI 381 Beijing PM2.5). Use when the user
  mentions hillclimb, backbones, SOTA catalog, research publications,
  dashboard, github.io, audit, forensic, KEEP ladder, or this repo.
  Also trigger on /autoresearch-uci and "continue" / "keep going" in this project.
---

# AutoResearch-UCI — original process + Pages pack

You are the outer-loop researcher. Do not invent a thinner process.

## Two things this skill forbids

1. **Thin hillclimb.** Do not treat XGBoost HP knobs as "the campaign." The source mandate is **50 isolated experiments per backbone** and **many papers inside each backbone**.
2. **Thin dashboard.** A table + champion box is a regression against `https://dlmastery.github.io/autoresearch/` and `.../clustering_olivetti/`. Ship the full pack every time results change.

## Hillclimb (verbatim source)

Read, do not paraphrase away:

- `generalized_ml_autoresearch/templates/CLAUDE_template.md` § Per-Backbone N-Experiment Mandate and § Per-Backbone Code Snapshots
- `generalized_ml_autoresearch/skills/ml-autoresearch-setup/SKILL.md` Steps 8–11
- `generalized_ml_autoresearch/templates/sota_catalog.yaml`
- repo `beijing_pm25/BACKBONE_CAMPAIGN.md` (live counts)

Rules:

- Isolation: finish one backbone, snapshot `code_versions/<bb>_start/` and `_final/`, then the next. Never interleave.
- XGBoost, LightGBM, CatBoost are **three** backbones.
- Tier 1 (linear/ridge/MLP Gu-Kelly-Xiu 2020) and Tier 2 (FT-Transformer, TabTransformer, TabNet, SAINT) are required cycles, not optional extras.
- Inside a backbone: one **paper recipe** per experiment (GOSS, DART, Huber/Tweedie/quantile, extra-trees, linear trees, domain papers). Not another `num_leaves` grid after 3 DISCARDs on that axis.
- 7-step every run: diagnose → cite → hypothesize → predict numeric range → one change → analyze vs prediction → checkpoint.
- Frozen 2014 test hash must not move. Composite fingerprint must not be rewritten.

Current recovery (do not jump): champion is LightGBM Exp30. Stay on LightGBM until 50 or `lightgbm_final/` is snapshotted. Next unused paper: Ke et al. 2017 GOSS.

## Pages pack (mandatory after any result change)

Match Olivetti/FX github.io, domain-swapped:

| Must exist under `docs/` | What it contains |
|---|---|
| `dashboard/index.html` | Links bar, literature ceiling, KEEP ladder SVG, 50-exp backbone bars, residual month/hour charts, persistence, frozen split + full hashes, sortable/filterable log, detail tabs (reasoning / metrics / config / CSV) |
| `dashboard/forensic_report.md` | Integrity + process checklist with PASS/WARN |
| `dashboard/audit_report.md` | All 14 `winner_archive.AUDIT_SECTIONS` |
| `dashboard/autoresearch_report.md` | Headline, protocol, ladder, remaining error |
| `dashboard/experiment_summary.md` | KEEP table + full log |
| `dashboard/research_journal.md` | 7-field narrative per KEEP |
| `FEATURES_AND_DATA.md` | Every column + citation |
| `dashboard/champion_diagnostics.json` | Month / hour / onset / spike-F1 from predictions |
| `dashboard/BACKBONE_CAMPAIGN.md` | Mandate vs actual counts |

Rebuild command (cwd repo):

```
python beijing_pm25/build_public_artifacts.py
python beijing_pm25/sync_dashboard.py
```

Never claim the dashboard is updated until those two commands have been run in this session and `docs/dashboard/index.html` contains the links bar + residual charts + backbone bars.

Source of residual numbers: `exp30_predictions.csv` joined to `data/times.csv`. Do not invent onset counts.

## Session start

1. Read `beijing_pm25/memory/project_autoresearch_checkpoint.md`, log tail, `best_config.json`.
2. Read `BACKBONE_CAMPAIGN.md` — which backbone cycle is open.
3. If Pages artifacts are missing or thinner than this skill's table, rebuild them **before** calling the work done.
4. Then run **one** paper-recipe experiment on the open backbone.

## Anti-patterns

- Pre-planned `hillclimb.py` sweeps
- Copying XGBoost config keys onto LightGBM/CatBoost
- Declaring a backbone done after 2–5 runs
- Publishing a dashboard without forensic/audit/FEATURES/residuals
- Comparing Guo & Lin 24.79 as if it used this test hash
