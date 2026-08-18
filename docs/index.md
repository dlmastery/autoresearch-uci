---
layout: default
title: AutoResearch-UCI
---

# AutoResearch-UCI — Beijing PM2.5

> **Champion:** Exp 30 LightGBM — 2014 test RMSE **20.945** · val RMSE **22.397** · skill vs persistence **+6.15%**
> **Protocol:** train 2010–2012 / val 2013 / test **2014** / 24 h embargo · `test_hash` frozen
> **Campaign:** 31 experiments · 9 KEEP · 22 DISCARD · original 50-exp × many-backbone mandate **not yet complete**

## Quick links

- 🎯 [Live dashboard](dashboard/) — KEEP ladder, residual forensics, filters, 7-field reasoning
- 📋 [AutoResearch report](dashboard/autoresearch_report.md)
- 🔍 [Forensic report](dashboard/forensic_report.md)
- 🧪 [14-section audit](dashboard/audit_report.md)
- 📓 [Experiment summary](dashboard/experiment_summary.md)
- 📔 [Research journal](dashboard/research_journal.md)
- 📚 [SOTA / published numbers](SOTA.md)
- 🧬 [Features and data](FEATURES_AND_DATA.md)
- 🏗 [Backbone campaign tracker](dashboard/BACKBONE_CAMPAIGN.md)
- 🏆 [Champion config](dashboard/best_config.json)
- 📉 [Champion residual JSON](dashboard/champion_diagnostics.json)
- 🧠 [Reasoning annotations](dashboard/reasoning_annotations.json)
- 📄 [Paper note](https://github.com/dlmastery/autoresearch-uci/blob/main/paper.md)
- 💻 [GitHub](https://github.com/dlmastery/autoresearch-uci)

## Three research findings

1. **1-hour nowcast is persistence-saturated.** Persistence RMSE = 22.316 on the frozen 2014 year. Exp30 skill is +6.15%. R² 0.95 is mostly lag-1.
2. **The remaining error is onset, not calm hours.** 95 hours with Δ ≥ 50 µg/m³ have RMSE 103.4 (pred 169 vs actual 248). January 33.07; hour 20 31.93.
3. **The composite gate works.** Exp25 LightGBM had the best raw test (20.90) and still DISCARD because 2013 val lost. Val is the bottleneck.

## Mandate status (original skill)

| Backbone | Done / 50 |
|---|---:|
| linear / ridge | 0 |
| mlp (Gu, Kelly & Xiu 2020) | 0 |
| ft_transformer (Gorishniy 2021) | 0 |
| tabnet / tabtransformer / saint | 0 |
| xgboost | 24 |
| lightgbm (champion — isolate here) | 5 |
| catboost | 2 |

Sister protocol: [dlmastery/autoresearch](https://github.com/dlmastery/autoresearch).
