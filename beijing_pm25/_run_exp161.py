"""Exp161 — MLP drop inversion_spread keep TEMP/DEWP on Exp136 recipe (MLP cycle 37/50)."""
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
    "--drop-feature", "inversion_spread",
    "--description", "MLP drop inversion_spread keep TEMP DEWP on Exp136 recipe (MLP cycle 37/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp160 drop "
        "is_weekend missed val 22.492. New: inversion_spread equals TEMP-DEWP exactly and "
        "corr with rh_magnus is -0.954. inv q4 n=2220 RMSE 22.17 versus CatBoost 22.39 "
        "(32.6 percent of SSE), need -0.87 pred_d -2.42 so dry well-mixed hours over-clean. "
        "Keep TEMP, DEWP, rh_magnus, vent_index. Drop unused inversion_spread."
    ),
    "--citations",
    (
        "Rumelhart, David E.; Hinton, Geoffrey E. and Williams, Ronald J. 1986 Nature "
        "'Learning representations by back-propagating errors' — hidden units form linear "
        "combinations of the raw inputs, so an explicit difference of two already-included "
        "covariates is a rank-1 duplicate the first layer already spans. Relevance: Exp136 "
        "already has TEMP, DEWP, and rh_magnus with inversion_spread corr -0.954, and inv "
        "q4 still over-cleans pred_d -2.42 versus need -0.87 at 32.6 percent of SSE, so "
        "dropping unused inversion_spread while keeping TEMP and DEWP is one derived-channel "
        "cleanup on the Exp136 recipe, not another calendar drop."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping inversion_spread while keeping TEMP, DEWP, and "
        "rh_magnus on the Exp136 MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, "
        "AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, pm25_accel, vent_index, "
        "Smooth-L1, clip=1.0) will cut 2013 val RMSE because the mechanism is removing a "
        "linear TEMP-DEWP copy that is also a near-duplicate of Magnus RH at corr -0.954 "
        "so first-layer GELU units are not double-counting dewpoint depression. Per "
        "Rumelhart et al. 1986 that is hidden units learning linear combinations. Because "
        "drop is_weekend just missed val, this is unused drop-inversion not another "
        "calendar drop. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the TEMP-DEWP copy was a 2013 tax. A val RMSE above 22.90 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
