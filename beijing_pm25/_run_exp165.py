"""Exp165 — MLP drop pm25_accel keep lags/delta1 on Exp164 recipe (MLP cycle 41/50)."""
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
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "vent_index",
    "--description", "MLP drop pm25_accel keep lags delta1 on Exp164 recipe (MLP cycle 41/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp164 MLP val 22.180 test "
        "20.201, January 31.90 versus JJA 13.98, hour 20 32.40, onset 111.26. Widen missed "
        "Exp97 by 0.013. New: need>=30 and accel<=0 n=121 RMSE 81.91 versus persist 78.35 "
        "and CatBoost 81.09 (25.0 percent of Exp164 SSE), need +55.19 pred_d -1.98 so the "
        "second-diff sign-flips at inflection onsets. Keep 24 lags and pm25_delta1. Drop "
        "unused pm25_accel."
    ),
    "--citations",
    (
        "Bai, Shaojie; Kolter, J. Zico and Koltun, Vladlen 2018 arXiv 'An Empirical "
        "Evaluation of Generic Convolutional and Recurrent Networks for Sequence "
        "Modeling' (arXiv:1803.01271) — sequence models already see the raw lag "
        "trajectory, so an explicit second difference can sign-flip at inflections and "
        "hurt more than it helps. Relevance: Exp164 already has 24 lags plus pm25_delta1 "
        "and pm25_accel, but need>=30 accel<=0 still predicts the wrong way pred_d -1.98 "
        "versus need +55.19 at 81.91 versus persist 78.35 and 25.0 percent of SSE, so "
        "dropping unused pm25_accel while keeping lags and delta1 is one inflection "
        "cleanup on the Exp164 recipe, not another widen."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping pm25_accel while keeping 24 lags and pm25_delta1 "
        "on the Exp164 MLP recipe (hidden 512-256-128, batch 16, dropout 0.2, AdamW lr "
        "3e-4, weight_decay 1e-4, log_iws, month_sin, vent_index, Smooth-L1, clip=1.0) "
        "will cut 2013 val RMSE because the mechanism is removing a second-diff that "
        "tells first-layer GELU units to drop when accel is negative even though the next "
        "hour jumps +55. Per Bai et al. 2018 that is lag trajectory versus a sign-flipping "
        "difference. Because widen just missed Exp97 by 0.013 and inverted on builds, "
        "this is unused drop-accel not another width. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.0 to 22.6 versus Exp97 20.735 and Exp164 20.201, val "
        "21.60 to 23.10, and composite -23.10 to -21.60. Val may move from 22.180 toward "
        "21.90 to 22.16 if the accel sign-flip was a 2013 tax. A val RMSE above 22.90 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
