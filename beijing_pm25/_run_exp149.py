"""Exp149 — MLP hetero_loss on Exp136 recipe (MLP cycle 25/50)."""
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
    "--set", "hetero_loss=true",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP hetero_loss on Exp136 recipe (MLP cycle 25/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Extra depth "
        "Exp148 inverted val to 23.289 and collapse 76.83 to 86.28. New: crash persist>=150 "
        "and need<-50 n=110 RMSE 86.06 versus CatBoost 81.81 and persist 108.97, need -95.34 "
        "pred_d -25.16 so homoscedastic Smooth-L1 only captures 26 percent of the drop "
        "(24.4 percent of SSE). Add unused hetero_loss, do not retry extra hidden 32."
    ),
    "--citations",
    (
        "Kendall, Alex and Gal, Yarin 2017 NeurIPS 'What Uncertainties Do We Need in "
        "Bayesian Deep Learning for Computer Vision?' (arXiv:1703.04977) — a learned "
        "log-variance head makes the residual loss heteroscedastic so high-noise inputs "
        "downweight the mean gradient instead of dominating it. Relevance: Exp136 crash "
        "hours persist>=150 and need<-50 still miss CatBoost 86.06 versus 81.81 with "
        "pred_d -25.16 versus need -95.34, and extra depth just made collapse worse, so "
        "turning unused hetero_loss on is one aleatoric head on the Exp136 recipe, not "
        "another hidden layer."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting hetero_loss from false to true on the Exp136 MLP "
        "recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay "
        "1e-4, log_iws, month_sin, pm25_accel, vent_index, Smooth-L1 plus a learned "
        "log-var head) will cut 2013 val RMSE because the mechanism is input-dependent "
        "precision so crash hours with need -95 cannot dominate the mean the way they did "
        "under homoscedastic Smooth-L1. Per Kendall and Gal 2017 that is heteroscedastic "
        "aleatoric loss. Because extra hidden 32 just inverted collapse, this is unused "
        "hetero_loss not another depth. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if crash-hour gradient domination was a 2013 tax. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
