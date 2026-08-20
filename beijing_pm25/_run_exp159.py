"""Exp159 — MLP drop PRES keep TEMP on Exp136 recipe (MLP cycle 35/50)."""
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
    "--drop-feature", "PRES",
    "--description", "MLP drop PRES keep TEMP on Exp136 recipe (MLP cycle 35/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp158 drop "
        "Is missed val 22.394. New: PRES>=1025 persist>=150 n=413 RMSE 38.33 versus "
        "CatBoost 42.89 and persist 40.56 (18.2 percent of SSE), need -3.20 pred_d -8.47 "
        "so the net over-cleans dirty anticyclones. Test PRES-TEMP corr -0.84. Keep Is. "
        "Drop unused PRES."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan and Babenko, Artem 2022 NeurIPS "
        "'On Embeddings for Numerical Features in Tabular Deep Learning' "
        "(arXiv:2203.05556) — a shared linear first layer wastes rank when two "
        "z-scored numeric columns are near-duplicates, so dropping a redundant channel "
        "frees GELU units from a collinear direction. Relevance: Exp136 already z-scores "
        "PRES and TEMP with corr -0.84, and PRES>=1025 persist>=150 still over-cleans "
        "pred_d -8.47 versus need -3.20 at 18.2 percent of SSE, so dropping unused raw "
        "PRES while keeping TEMP is one collinear-channel cleanup on the Exp136 recipe, "
        "not another drop Is."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping PRES while keeping TEMP, Iws, and Is on the "
        "Exp136 MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, "
        "weight_decay 1e-4, month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will "
        "cut 2013 val RMSE because the mechanism is removing a collinear anticyclone "
        "copy so first-layer GELU units are not double-counting the TEMP-PRES thermal "
        "axis at corr -0.84. Per Gorishniy et al. 2022 that is redundant numerical "
        "embeddings. Because drop Is just missed val, this is unused drop-PRES not "
        "another sparse precip drop. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the collinear PRES channel was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
