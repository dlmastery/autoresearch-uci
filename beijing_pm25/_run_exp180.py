"""Exp180 — FT-Transformer Pre-LN dropout=0.2 on Exp167 features (FT cycle 6/50)."""
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
    "--set", "dropout=0.2",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN dropout=0.2 on Exp167 features (FT cycle 6/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN dropout 0.1 val 22.140; Exp179 dropout=0 "
        "DISCARD val 22.200 (2013 tax) test 20.509. New: weekend typical |need|<=10 n=1435 "
        "RMSE 8.10 versus persist 5.19 (2.94 percent of SSE; need +0.49 pred_d +0.92) while "
        "weekday typical is 6.73 versus persist 5.03, so weekend calm hours are the extra "
        "identity leak. Unused change is dropout 0.1 to 0.2 on Pre-LN, not another 0/0.05."
    ),
    "--citations",
    (
        "Gal, Yarin and Ghahramani, Zoubin 2016 ICML 'Dropout as a Bayesian Approximation: "
        "Representing Model Uncertainty in Deep Learning' (arXiv:1506.02142) — a higher "
        "dropout rate is an approximate posterior that down-weights overconfident residual "
        "overwrites when train and val year-patterns disagree. Relevance: Exp179 dropout=0 "
        "improved 2014 test to 20.509 but raised 2013 val to 22.200, and Exp167 weekend "
        "typical already leaks persist 5.19 at 8.10; raising Pre-LN dropout to 0.2 is unused "
        "stronger epistemic regularization on those weekend calm hours, not a Post-LN revert."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting dropout=0.2 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is stronger Bernoulli regularization so "
        "weekend typical hours cannot over-move lag-1 (need +0.49, Exp167 pred_d +0.92, "
        "RMSE 8.10 versus persist 5.19). Per Gal and Ghahramani 2016 that is dropout as "
        "approximate Bayesian averaging. Because dropout=0 taxed 2013, this is unused 0.2 "
        "not another shrink to 0.05. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.40 to 21.80 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.90, and composite -22.90 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if extra dropout damps 2013 weekend over-move. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
