"""Exp170 — MLP persist_residual on Exp167 residual recipe (MLP cycle 46/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "persist_residual=true",
    "--description", "MLP persist_residual y=lag1+delta on Exp167 residual recipe (MLP cycle 46/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck, January 31.22 versus persist-1 33.58 and JJA 13.87, hour 20 32.68 "
        "versus persist 33.24 (skill only 1.7 percent, 11.10 percent of SSE), onset n=83 "
        "RMSE 110.28 losing to persist-1 107.80. Exp168 huber_beta inverted onset; Exp169 "
        "se_pm25 missed val 22.117. New: January onset n=18 RMSE 139.25 versus persist "
        "127.93 (10.90 percent of SSE; need +107.72 pred_d -9.78) so the 128-d head "
        "subtracts about 10 ug on hours that jump +108, worse than persist. Typical "
        "|need|<=10 n=5117 RMSE 7.14 versus persist 5.08. Hidden residual did not pin "
        "the OUTPUT to lag-1. Add unused persist residual yhat=lag1+delta, not another SE product."
    ),
    "--citations",
    (
        "Zeng, Ailing; Chen, Muxi; Zhang, Lei and Xu, Qiang 2023 AAAI 'Are Transformers "
        "Effective for Time Series Forecasting?' (arXiv:2205.13504) — a one-layer linear "
        "residual around the series baseline beats transformers that must relearn identity, "
        "because the deep stack otherwise overwrites the last observation on most hours. "
        "Relevance: Exp167 hidden residual still lets the 128-d head anti-jump January "
        "onsets (pred_d -9.78 versus need +107.72 at 139.25 versus persist 127.93) and "
        "typical |need|<=10 still loses persist 5.08 at 7.14, so adding unused "
        "persist_residual yhat = pm25_lag1 + delta on the Exp167 recipe is one output-space "
        "identity, not another hidden skip or SE payload."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting persist_residual=true on the Exp167 residual MLP "
        "recipe (hidden 512-256-128, batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay "
        "1e-4, residual true, log_iws, month_sin, pm25_accel, vent_index, layer_norm off, "
        "clip=1.0, huber_beta=1) will cut 2013 val RMSE because the mechanism is an "
        "explicit lag-1 identity so the GELU stack only learns the increment and cannot "
        "subtract 10 ug on January onsets that need +108. Per Zeng et al. 2023 that is "
        "DLinear-style residual forecasting. Because se_pm25 just missed val and hidden "
        "residual already kept, this is unused output persist not another skip or SE "
        "product. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 19.6 to 22.4 versus Exp167 20.072, val 21.40 to 23.00, and "
        "composite -23.00 to -21.40. Val may move from 21.972 toward 21.50 to 21.90 if "
        "January anti-jump and typical overwrite were a 2013 tax. A val RMSE above 22.80 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
