"""Exp141 — MLP add pm25_delta6 on Exp136 recipe (MLP cycle 17/50)."""
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
    "--add-feature", "pm25_delta6",
    "--description", "MLP add pm25_delta6 on Exp136 recipe (MLP cycle 17/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: hours with delta6>20 "
        "n=2457 RMSE 25.92 versus CatBoost 26.91 and persist 27.93, need +1.17 pred_d "
        "-0.85 so the net mean-reverts a still-building 6h episode (49.4 percent of SSE). "
        "delta1 and accel span 1-2h not lag1-minus-lag7. Add unused pm25_delta6, do not "
        "retry se_iws."
    ),
    "--citations",
    (
        "Bai, Shaojie; Kolter, J. Zico and Koltun, Vladlen 2018 ICML 'An Empirical "
        "Evaluation of Generic Convolutional and Recurrent Networks for Sequence "
        "Modeling' (arXiv:1803.01271) — dilated temporal nets treat a several-step "
        "lookback slope as a first-class local trend that a 1-step delta does not span. "
        "Relevance: Exp136 already has pm25_delta1 and pm25_accel but delta6>20 still "
        "predicts -0.85 versus need +1.17 and owns 49.4 percent of SSE, so adding unused "
        "lag1-minus-lag7 is one 6h episode-slope feature on the Exp136 recipe, not "
        "another wind product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_delta6 on the Exp136 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, Exp97 features plus lag1 minus "
        "lag7) will cut 2013 val RMSE because the mechanism is an explicit 6h episode "
        "slope so still-building hours are not treated as mean-reverting delta1. Per Bai "
        "et al. 2018 that is a dilated lookback trend. Because se_iws just inverted 2013 "
        "val, this is unused pm25_delta6 not another wind product. KEEP if 1h composite "
        "beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if 6h-building mean-reversion was a 2013 tax. A val RMSE above "
        "22.85 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
