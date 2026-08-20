"""Exp151 — MLP Adam lr=1e-3 on Exp136 recipe (MLP cycle 27/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "batch_size=16",
    "--set", "lr=0.001",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP Adam lr=1e-3 on Exp136 recipe (MLP cycle 27/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp129 lr=1e-4 "
        "underfit val 23.069. Exp150 clip=0 helped crash but taxed val. New: build need>20 "
        "persist>=80 n=438 RMSE 51.59 versus CatBoost 51.10 and persist 50.39, need +38.21 "
        "pred_d +0.88 so 3e-4 stays persist-locked while haze still builds (34.9 percent of "
        "SSE). Raise unused Adam lr, do not retry grad_clip."
    ),
    "--citations",
    (
        "Kingma, Diederik P. and Ba, Jimmy 2015 ICLR 'Adam: A Method for Stochastic "
        "Optimization' (arXiv:1412.6980) — Adam's base learning rate is a free global "
        "step-size on top of per-coordinate second-moment scaling, so a larger lr moves "
        "the weights farther in a 50-epoch cosine budget. Relevance: Exp136 uses default "
        "3e-4 and build persist>=80 need>20 still loses persist 51.59 versus 50.39 with "
        "pred_d +0.88 versus need +38.21, and 1e-4 already underfit, so raising unused lr "
        "to 1e-3 is one opposite Adam lever on the Exp136 recipe, not another clip."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting Adam lr from 3e-4 to 1e-3 on the Exp136 MLP recipe "
        "(batch 16, hidden 256-128-64, dropout 0.2, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val RMSE because the "
        "mechanism is larger adaptive steps so persist-locked building hours are not stuck "
        "at pred_d +0.88 while need is +38. Per Kingma and Ba 2015 that is the Adam base "
        "lr. Because 1e-4 underfit and clip=0 just taxed 2013 val, this is unused lr raise "
        "not another clip. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.8 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.20, and composite -23.20 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if persist-locked building hours were a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
