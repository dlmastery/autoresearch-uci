"""Exp175 — isolate FT-Transformer Gorishniy 2021 paper defaults on Exp167 features (FT 1/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "ft_transformer",
    "--set", "d_model=64",
    "--set", "n_heads=4",
    "--set", "n_layers=3",
    "--set", "dropout=0.1",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--description", "FT-Transformer Gorishniy 2021 paper default on Exp167 features (FT cycle 1/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE, "
        "pred_d -3.88 versus need -0.12). JJA 13.87 versus persist 14.83. Hour 20 32.68 "
        "versus persist 33.24 (11.10 percent of SSE; need +7.65 pred_d +4.25). Onset n=83 "
        "RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; need +87.40 pred_d "
        "-0.60). MLP 50/50 is complete; mixup_alpha=0.2 also DISCARD at val 22.014. New: "
        "hour-20 SE persist>=80 n=74 RMSE 60.62 versus persist 61.42 (8.49 percent of SSE; "
        "need +14.47 pred_d +5.69). The 16 hour-20 SE persist>=80 need>20 hours hold 8.26 "
        "percent of SSE at 128.62 versus persist 129.94 with pred_d only +10.29 versus "
        "need +64.31. Residual GELU cannot route hour times SE times dirty-lag; isolate "
        "unused FT-Transformer paper defaults on the same Exp167 columns."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "each numerical column is a token and a PreNorm Transformer mixes tokens via a "
        "CLS readout, which beat ResNet-style MLPs on most of their tabular suites. "
        "Relevance: Exp167 residual MLP is persist-locked on hour-20 SE persist>=80 "
        "(RMSE 60.62, pred_d +5.69 versus need +14.47, 8.49 percent of SSE) because "
        "additive GELU layers cannot attend hour_sin to cbwd_SE to pm25_lag1; switching "
        "the unused backbone to FT-Transformer paper defaults on the same Exp167 features "
        "is one architecture change, not another MLP hyperparameter."
    ),
    "--hypothesis",
    (
        "We hypothesize that switching the unused backbone from Exp167 residual MLP to "
        "ft_transformer paper defaults (d_model 64, n_heads 4, n_layers 3, dropout 0.1, "
        "AdamW lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10) "
        "on the same Exp167 feature recipe will cut 2013 val RMSE because the mechanism "
        "is feature-wise self-attention so hour, SE, Iws, and lag-1 tokens can mix on "
        "evening dirty-SE hours instead of remaining persist-locked at pred_d +5.69 "
        "versus need +14.47. Per Gorishniy et al. 2021 that is FT-Transformer "
        "tokenization. Because MLP 50/50 is complete and residual identity already kept, "
        "this is unused tabular transformer isolation, not another MLP loss or dummy. "
        "KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.8 to 23.6 versus Exp167 20.072, val 21.70 to 24.50, "
        "and composite -24.50 to -21.70. Val may move from 21.972 toward 21.70 to 21.90 "
        "if hour-20 SE persist>=80 evening advection was a 2013 tax that attention can "
        "route. A val RMSE above 23.80 is a miss versus the residual MLP identity path. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
