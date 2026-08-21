"""Exp181 — FT-Transformer Pre-LN batch_size=64 on Exp167 features (FT cycle 7/50)."""
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
    "--set", "batch_size=64",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN batch_size=64 on Exp167 features (FT cycle 7/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN batch 32 val 22.140 typical 7.96 versus "
        "champ 7.14. Dropout 0/0.2 closed. New: hour-9 persist>=80 n=166 RMSE 19.48 versus "
        "persist 18.55 (1.97 percent of SSE; need -1.52 pred_d -2.89) so morning dirty hours "
        "over-clean, and batch-32 SGD noise can shove lag-1 around on those hours. Unused "
        "change is batch 32 to 64 on Pre-LN, not another dropout."
    ),
    "--citations",
    (
        "Smith, Samuel L. and Le, Quoc V. 2018 ICLR 'A Bayesian Perspective on Generalization "
        "and Stochastic Gradient Descent' (arXiv:1710.06451) — the SGD noise scale is "
        "learning-rate times N over batch-size, so doubling B halves gradient noise and "
        "the optimizer stays closer to a wide identity basin. Relevance: Exp178 Pre-LN "
        "typical 7.96 versus Exp167 7.14 and hour-9 persist>=80 over-cleans pred_d -2.89 "
        "versus need -1.52 at 19.48 versus persist 18.55; raising batch_size from 32 to 64 "
        "is unused noise-scale shrink on Pre-LN, not another dropout or Post-LN revert."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting batch_size=64 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is half the SGD noise scale so morning "
        "dirty hours cannot over-clean lag-1 (need -1.52, Exp167 pred_d -2.89). Per Smith "
        "and Le 2018 that is Bayesian noise scale g proportional to 1/B. Because dropout "
        "0/0.2 already closed, this is unused larger batch not another regularizer. KEEP "
        "if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.30 to 21.60 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.80, and composite -22.80 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if quieter SGD restores hour-9 persist. A val RMSE above "
        "22.80 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
