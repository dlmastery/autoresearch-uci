"""Exp163 — MLP drop cbwd_cv keep directed winds on Exp136 recipe (MLP cycle 39/50)."""
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
    "--drop-feature", "cbwd_cv",
    "--description", "MLP drop cbwd_cv keep directed winds on Exp136 recipe (MLP cycle 39/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp162 drop "
        "is_heating missed val 22.426. New: cbwd one-hots sum to 1.0 exactly. cv "
        "persist>=150 n=505 RMSE 26.40 versus CatBoost 28.95 and persist 27.68 (10.5 "
        "percent of SSE), need +1.28 pred_d -0.76 so dirty calm hours under-build. cv Iws "
        "median 1.78 versus non-cv 8.94. Keep NE NW SE. Drop unused cbwd_cv."
    ),
    "--citations",
    (
        "Borisov, Vadim; Leemann, Tobias; Sessler, Kathrin; Haug, Johannes; Pawelczyk, "
        "Martin and Kasneci, Gjergji 2022 IEEE 'Deep Neural Networks and Tabular Data: A "
        "Survey' (arXiv:2110.01889) — one-hot encodings of a K-level categorical make the "
        "first-layer design matrix rank-deficient, so MLP gradients smear across a "
        "dummy-trap null space. Relevance: Exp136 already has cbwd_NE NW SE and cv that "
        "sum to 1.0, and cv persist>=150 still under-builds pred_d -0.76 versus need +1.28 "
        "at 26.40 versus persist 27.68, so dropping unused cbwd_cv while keeping the three "
        "directed winds is one dummy-trap cleanup on the Exp136 recipe, not another "
        "calendar drop."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping cbwd_cv while keeping cbwd_NE, cbwd_NW, and "
        "cbwd_SE on the Exp136 MLP recipe (batch 16, hidden 256-128-64, dropout 0.2, "
        "AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, pm25_accel, vent_index, "
        "Smooth-L1, clip=1.0) will cut 2013 val RMSE because the mechanism is removing the "
        "fourth one-hot so first-layer GELU units identify directed winds against calm "
        "rather than a rank-deficient (1,1,1,1) kernel. Per Borisov et al. 2022 that is "
        "one-hot collinearity. Because drop is_heating just missed val, this is unused "
        "drop-cv not another calendar dummy. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the dummy-trap calm channel was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
