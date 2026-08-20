"""Exp158 — MLP drop Is keep Iws on Exp136 recipe (MLP cycle 34/50)."""
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
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--drop-feature", "Is",
    "--description", "MLP drop Is keep Iws on Exp136 recipe (MLP cycle 34/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp157 drop "
        "Iws missed val 22.336. New: Is>0 n=35 RMSE 15.32 versus CatBoost 12.05 and "
        "persist 18.17 (0.25 percent of SSE). Test Is is 99.56 percent zero, mean 0.037 "
        "std 0.74 p99 0 max 23, so z-score maps a 23-hour snow streak to a 25-sigma "
        "spike. Snow pred_d -6.66 versus need -2.57 (over-clean). Keep Iws. Drop unused Is."
    ),
    "--citations",
    (
        "Grinsztajn, Leo; Oyallon, Edouard and Varoquaux, Gael 2022 NeurIPS "
        "'Why do tree-based models still outperform deep learning on typical tabular "
        "data?' (arXiv:2207.08815) — MLPs are harmed by uninformative irregular "
        "numerical features because gradient updates smear rare spikes across all hours, "
        "while a tree isolates them with one split. Relevance: Exp136 already z-scores "
        "Is but test Is is 99.56 percent zero with n=35 snow hours at 0.25 percent of SSE "
        "and max 23 maps to a 25-sigma spike, CatBoost snow RMSE 12.05 versus MLP 15.32, "
        "so dropping unused Is is one sparse-feature cleanup on the Exp136 recipe, not "
        "another drop Iws."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping Is while keeping Iws and log_iws on the Exp136 "
        "MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, "
        "weight_decay 1e-4, month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will "
        "cut 2013 val RMSE because the mechanism is removing a 99.56-percent-zero "
        "cumulative snow counter so first-layer GELU units are not saturated by Is=23 "
        "at 25 sigma. Per Grinsztajn et al. 2022 that is uninformative irregular "
        "features. Because drop Iws just missed val, this is unused drop-Is not another "
        "wind drop. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the 25-sigma snow spike was a 2013 tax. A val RMSE above 22.90 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
