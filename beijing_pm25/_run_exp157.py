"""Exp157 — MLP drop raw Iws keep log_iws on Exp136 recipe (MLP cycle 33/50)."""
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
    "--drop-feature", "Iws",
    "--description", "MLP drop Iws keep log_iws on Exp136 recipe (MLP cycle 33/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. rh_iws "
        "Exp156 inverted humid collapse. New: Iws>=50 n=746 RMSE 10.46 versus CatBoost "
        "9.92 and persist 12.61 (2.4 percent of SSE). Test Iws median 4.92 std 41.64 p99 "
        "232 so the linear tail is collinear with log_iws after z-score. Drop unused raw "
        "Iws, keep log_iws, do not retry rh_iws."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11959) — "
        "MLP tabular nets are sensitive to numerical scale, so a heavy-tailed linear copy "
        "sitting next to its log1p twin lets the tail dominate first-layer embeddings. "
        "Relevance: Exp136 already has log_iws plus raw Iws and Iws>=50 still loses "
        "CatBoost 10.46 versus 9.92 with Iws p99 232 versus median 4.92, so dropping "
        "unused raw Iws while keeping log_iws is one scale cleanup on the Exp136 recipe, "
        "not another RH/wind ratio."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping raw Iws while keeping log_iws on the Exp136 MLP "
        "recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay "
        "1e-4, month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val "
        "RMSE because the mechanism is removing the linear storm tail so first-layer GELU "
        "units are not saturated by Iws p99=232. Per Gorishniy et al. 2021 that is "
        "numerical-scale sensitivity. Because rh_iws just inverted humid collapse, this "
        "is unused drop-Iws not another wind product. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the raw Iws tail was a 2013 tax. A val RMSE above 22.90 is a "
        "miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
