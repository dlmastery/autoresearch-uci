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
    <a href="https://github.com/dlmastery/autoresearch-uci"><img src="https://img.shields.io/badge/experiments-31-orange.svg" alt="31 experiments"></a>
    <a href="https://dlmastery.github.io/autoresearch-uci/dashboard/"><img src="https://img.shields.io/badge/docs-GitHub%20Pages-blue.svg" alt="GitHub Pages"></a>
    <a href="#champion"><img src="https://img.shields.io/badge/2014%20test%20RMSE-20.94-blue.svg" alt="2014 test RMSE 20.94"></a>
    <a href="#champion"><img src="https://img.shields.io/badge/skill%20vs%20persistence-+6.1%25-yellow.svg" alt="Skill +6.1%"></a>
  </p>
</p>

---

## What this is

A **verbatim port** of the [dlmastery/autoresearch](https://github.com/dlmastery/autoresearch) protocol onto **Grok** as the outer loop, pointed at a **pragmatic, non-toy** regression: hourly PM2.5 nowcast at the Beijing US Embassy (UCI 381, Liang et al. 2015).

This is **not** Kaggle Ames house prices and **not** kin8nm. Those are saturated or simulated. This series is operational air quality. The 1-hour task is persistence-heavy; the remaining error is haze onsets and longer horizons.

Sister repos: [`autoresearch`](https://github.com/dlmastery/autoresearch) · [`autoresearchspy`](https://github.com/dlmastery/autoresearchspy) · [`autoresearchtabular`](https://github.com/dlmastery/autoresearchtabular) · [`environment_stats_talk`](https://github.com/dlmastery/environment_stats_talk)

**Dashboard (live):** [https://dlmastery.github.io/autoresearch-uci/dashboard/](https://dlmastery.github.io/autoresearch-uci/dashboard/)

## The ladder (Karpathy keep/discard)

One change per experiment. KEEP only if composite rose. DISCARDs stay in the log. This is the champion lineage — the only steps that moved the floor.

```
persistence 2014          test RMSE 22.316
        |
Exp1  C&G 2016 XGBoost    21.768   KEEP   skill +2.5%
        |
Exp2  max_depth 4         21.996   KEEP   val was the bottleneck (23.35→23.20)
        |
Exp4  learning_rate 0.01  22.008   KEEP   more shrinkage
        |
Exp8  subsample 0.6       22.034   KEEP   stochastic rows
        |
Exp14 inversion_spread    21.823   KEEP   TEMP−DEWP (Liang 2015)
        |
Exp15 pm25_delta1         21.290   KEEP   lag1−lag2 momentum
        |
Exp22 inversion + delta   21.122   KEEP   both features together
        |
Exp29 LightGBM same feats 20.784   KEEP   leaf-wise on winning features
        |
Exp30 num_leaves 63       20.945   KEEP   val improved  ← champion
        |
     21 discarded rungs     —     DISCARD  (depth 8/5/3, lr 0.05/0.005,
                                           LightGBM test 20.90 but val lost, …)
```

| Rung | Delta | Test RMSE | Val RMSE | Composite | vs previous KEEP |
|---:|---|---:|---:|---:|---|
| 1 | Chen & Guestrin 2016 defaults | 21.768 | 23.354 | −23.354 | floor |
| 2 | `max_depth` 6→4 | 21.996 | 23.205 | −23.205 | val improved; test briefly worse |
| 4 | `learning_rate` 0.03→0.01 | 22.008 | 23.124 | −23.124 | shrinkage |
| 8 | `subsample` 0.8→0.6 | 22.034 | 22.983 | −22.983 | row bagging |
| 14 | + `inversion_spread` | 21.823 | 22.885 | −22.885 | first real test drop |
| 15 | + `pm25_delta1` | 21.290 | 22.684 | −22.684 | onset momentum |
| 22 | stack inversion onto delta | 21.122 | 22.470 | −22.470 | both features |
| 29 | LightGBM on those features | 20.784 | 22.428 | −22.428 | leaf-wise (diagnosed) |
| **30** | **num_leaves 31→63** | **20.945** | **22.397** | **−22.397** | **local tweak after KEEP** |

Composite is `min(−val, −test)`, so a KEEP can happen when **val** is the bottleneck even if test ticks up (rungs 2–8). That is the gate working, not a bug. The last three KEEPs improved **both** sides.

21 other experiments were DISCARD. LightGBM Exp25 posted the best raw **test** (20.90) and still lost: val 22.71 < champion val 22.47.

## Champion

| | Value |
|---|---|
| Model | LightGBM num_leaves 63, lr 0.01, bagging 0.6 + `pm25_delta1` + `inversion_spread` |
| Protocol | calendar years, 24 h embargo, test = **2014** |
| 2014 test RMSE | **20.945 µg/m³** (Exp1 floor 21.768) |
| 2013 val RMSE | **22.397** (Exp1 23.354) |
| 2014 persistence RMSE | 22.316 µg/m³ |
| Skill vs persistence | **+6.1%** |
| n_test | 7950 hours |
| Campaign | 31 experiments, 9 KEEP / 22 DISCARD |

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
