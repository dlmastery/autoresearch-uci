"""Exp153 — MLP batch_size=64 on Exp136 recipe (MLP cycle 29/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "batch_size=64",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP batch_size=64 on Exp136 recipe (MLP cycle 29/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp130 batch "
        "16 helped 2014. Exp152 dropout=0.1 was a 0.031 val close miss. New: persist 80-150 "
        "n=2068 RMSE 22.91 versus CatBoost 22.65 and persist 24.17, need +0.32 pred_d -1.31 "
        "so batch-16 SGD over-cleans the moderate haze band (32.5 percent of SSE). Raise "
        "unused batch, do not retry dropout 0.1."
    ),
    "--citations",
    (
        "Smith, Samuel L. and Le, Quoc V. 2018 ICLR 'A Bayesian Perspective on "
        "Generalization and Stochastic Gradient Descent' (arXiv:1710.06451) — the SGD "
        "noise scale is learning-rate over batch size, so a 4x larger batch with fixed "
        "lr is a 4x quieter optimizer. Relevance: Exp136 uses batch 16 and persist 80-150 "
        "still over-cleans pred_d -1.31 versus need +0.32 at 22.91 versus persist 24.17 "
        "owning 32.5 percent of SSE, so setting unused batch_size to 64 is one quieter "
        "SGD step on the Exp136 recipe, not another dropout."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting batch_size from 16 to 64 on the Exp136 MLP recipe "
        "(hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val RMSE "
        "because the mechanism is a smaller SGD noise scale so moderate persist 80-150 "
        "hours are not jittered off persist into over-clean. Per Smith and Le 2018 that "
        "is the noise scale g=lr/batch. Because batch 16 helped 2014 and dropout 0.1 was "
        "a val close miss, this is unused large batch not another dropout. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.8 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.20, and composite -23.20 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if noisy moderate-haze over-clean was a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
