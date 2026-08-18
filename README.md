<p align="center">
  <h1 align="center">AutoResearch-UCI</h1>
  <p align="center">
    <strong>Karpathy-style autonomous research loop on UCI 381 Beijing PM2.5</strong>
  </p>
  <p align="center">
    Grok Build is the outer-loop researcher. The Python runner is the evaluator.<br>
    Frozen industry split: train 2010–2012 · val 2013 · test <strong>2014</strong> · 24 h embargo.
  </p>
  <p align="center">
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
    <a href="#license"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT"></a>
    <a href="https://github.com/dlmastery/autoresearch-uci"><img src="https://img.shields.io/badge/experiments-28-orange.svg" alt="28 experiments"></a>
    <a href="https://dlmastery.github.io/autoresearch-uci/dashboard/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg" alt="GitHub Pages"></a>
    <a href="#champion"><img src="https://img.shields.io/badge/2014%20test%20RMSE-21.12-blue.svg" alt="2014 test RMSE 21.12"></a>
    <a href="#champion"><img src="https://img.shields.io/badge/skill%20vs%20persistence-+5.4%25-yellow.svg" alt="Skill +5.4%"></a>
  </p>
</p>

---

## What this is

A **verbatim port** of the [dlmastery/autoresearch](https://github.com/dlmastery/autoresearch) protocol onto **Grok** as the outer loop, pointed at a **pragmatic, non-toy** regression: hourly PM2.5 nowcast at the Beijing US Embassy (UCI 381, Liang et al. 2015).

This is **not** Kaggle Ames house prices and **not** kin8nm. Those are saturated or simulated. This series is operational air quality. The 1-hour task is persistence-heavy; the remaining error is haze onsets and longer horizons.

Sister repos: [`autoresearch`](https://github.com/dlmastery/autoresearch) · [`autoresearchspy`](https://github.com/dlmastery/autoresearchspy) · [`autoresearchtabular`](https://github.com/dlmastery/autoresearchtabular) · [`environment_stats_talk`](https://github.com/dlmastery/environment_stats_talk)

**Dashboard:** [dlmastery.github.io/autoresearch-uci/dashboard/](https://dlmastery.github.io/autoresearch-uci/dashboard/)

## Champion

| | Value |
|---|---|
| Model | XGBoost depth 4, lr 0.01, subsample 0.6 + `pm25_delta1` + `inversion_spread` |
| Protocol | calendar years, 24 h embargo, test = **2014** |
| 2014 test RMSE | **21.122 µg/m³** (Exp1 floor was 21.768) |
| 2013 val RMSE | **22.470** (Exp1 was 23.354) |
| 2014 persistence RMSE | 22.316 µg/m³ |
| Skill vs persistence | **+5.4%** (was +2.5%) |
| n_test | 7950 hours |
| Campaign | 28 experiments, 7 KEEP / 21 DISCARD |

Published 1-step numbers on *other* splits of this file sit around **24.7–26.5 RMSE** (Guo & Lin 2018 MV-LSTM; Brownlee 2017 LSTM). They are not directly comparable. See [`SOTA.md`](SOTA.md).

## Frozen split (industry practice)

UCI 381 has no official split. This repo freezes the operational cut:

| Fold | Years | n | Role |
|---|---|---:|---|
| train | 2010–2012 (minus last 24 h) | 21725 | fit |
| val | 2013 (minus last 24 h) | 7884 | early stopping + KEEP gate |
| test | **2014 full year** | 7950 | report only — never optimize |

`test_hash` lives in [`beijing_pm25/data/split_manifest.json`](beijing_pm25/data/split_manifest.json). Changing test timestamps is reward hacking.

Random / stratified k-fold is forbidden (Bergmeir, Hyndman & Koo 2018, arXiv:1905.11744).

## Protocol (verbatim)

Grok Build **is** the researcher. Every experiment:

1. Diagnose  
2. Cite (author / year / venue / arXiv-or-title / relevance)  
3. Hypothesize (mechanism)  
4. Predict a numeric range  
5. Run **one** change via the runner  
6. Analyze vs prediction  
7. Checkpoint  

The runner **refuses to launch** without a pre-run reasoning blob that passes Citation Rigor + Completeness (`generalized_ml_autoresearch.core.reasoning`).

Composite (frozen):

```
composite = min(−val_RMSE, −test_RMSE) − 0.1 × n_windows_with_RMSE>40
```

KEEP iff composite improves. Test is never a decision input.

## Quick start

```powershell
git clone https://github.com/dlmastery/autoresearch-uci.git
git clone --depth 1 https://github.com/dlmastery/autoresearch.git
cd autoresearch-uci
pip install numpy pandas scikit-learn xgboost pyyaml
python beijing_pm25/prepare_data.py
python beijing_pm25/run_exp.py --config beijing_pm25/config_exp1.yaml
python beijing_pm25/sync_dashboard.py
python -m http.server 8765 --directory docs/dashboard
```

`run_exp.py` expects the sibling clone `../autoresearch` **or** `C:\Users\abhir\dlmastery-github\autoresearch` for `generalized_ml_autoresearch`.

If the user says `continue`, Grok reads [`AGENTS.md`](AGENTS.md) + [`beijing_pm25/memory/project_autoresearch_checkpoint.md`](beijing_pm25/memory/project_autoresearch_checkpoint.md) and runs the pasteable next command. One experiment.

## Repository map

```
autoresearch-uci/
├── README.md                    you are here
├── AGENTS.md / GROK.md / CLAUDE.md
├── AUTORESEARCH_PROCESS.md
├── SOTA.md
├── WHY_THIS_BENCHMARK.md
├── beijing_pm25/
│   ├── prepare_data.py          UCI download + causal lags
│   ├── calendar_split.py        frozen year cut + hash
│   ├── run_exp.py               gated runner wrapper
│   ├── dashboard.html           live dashboard source
│   ├── sync_dashboard.py        → docs/dashboard/
│   ├── data/split_manifest.json
│   └── autoresearch_results/    jsonl + reasoning + predictions
└── docs/dashboard/              GitHub Pages
```

## What is not done yet

- GitHub Pages must be switched on (Settings → Pages → `/docs`). The files are already under `docs/dashboard/`.
- Exp2+ (t+6 on the same `test_hash`) is the next KEEP-worthy axis.
- 14-section winner audit is produced by the upstream `winner_archive` when we wire it; Exp1 is the floor, not a deployable champion.

## License

MIT. Dataset: UCI 381, CC BY 4.0, cite Liang et al. 2015 Proc. Royal Society A.
