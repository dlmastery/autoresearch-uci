"""Exp167 — MLP residual skips on Exp164 512-wide recipe (MLP cycle 43/50)."""
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
    "--set", "hidden=[512,256,128]",
    "--set", "residual=true",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP residual skips on Exp164 recipe (MLP cycle 43/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp164 MLP val 22.180 test "
        "20.201, January 31.90 versus JJA 13.98, hour 20 32.40, onset 111.26, 0.013 shy of "
        "Exp97. Exp166 LayerNorm missed val 22.442. New: dirty-stable persist>=150 "
        "|need|<=10 n=654 RMSE 13.13 versus persist 5.95 and Exp136 12.40 (3.47 percent of "
        "SSE), pred_d -3.91 on hours that need +0.34 so the 512-wide trunk overwrites "
        "lag-1. Keep LayerNorm off. Add unused residual skips."
    ),
    "--citations",
    (
        "He, Kaiming; Zhang, Xiangyu; Ren, Shaoqing and Sun, Jian 2016 CVPR 'Deep "
        "Residual Learning for Image Recognition' (arXiv:1512.03385) — identity shortcuts "
        "let a stack keep an input path so later nonlinear layers do not have to re-learn "
        "a copy, which is what persist needs on already-dirty stable hours. Relevance: "
        "Exp164 already has lag-1 in a 512-256-128 feedforward trunk, but dirty-stable "
        "persist>=150 |need|<=10 still over-cleans pred_d -3.91 versus need +0.34 at 13.13 "
        "versus persist 5.95, so adding unused residual skips on the Exp164 recipe is one "
        "identity path, not another LayerNorm."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting residual=true on the Exp164 MLP recipe (hidden "
        "512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0, layer_norm off) will cut "
        "2013 val RMSE because the mechanism is projection shortcuts so lag-1 can skip "
        "the 512-wide GELU stack on dirty-stable hours instead of being overwritten by "
        "pred_d -3.91. Per He et al. 2016 that is residual identity. Because LayerNorm "
        "just taxed typical over-move, this is unused residual not another normalizer. "
        "KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.0 to 22.6 versus Exp97 20.735 and Exp164 20.201, val "
        "21.60 to 23.10, and composite -23.10 to -21.60. Val may move from 22.180 toward "
        "21.90 to 22.16 if overwriting lag-1 on dirty-stable hours was a 2013 tax. A val "
        "RMSE above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
