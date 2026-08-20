"""Exp152 — MLP dropout=0.1 on Exp136 recipe (MLP cycle 28/50)."""
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
    "--set", "dropout=0.1",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP dropout=0.1 on Exp136 recipe (MLP cycle 28/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp126 "
        "dropout=0.3 taxed val 22.729. Exp151 lr=1e-3 was inert on building hours. New: "
        "Saturday n=1135 RMSE 20.98 versus CatBoost 20.35 and persist 22.43, need +0.19 "
        "pred_d -0.91 so p=0.2 over-cleans weekend (14.9 percent of SSE). Lower unused "
        "dropout, do not retry nearby lr."
    ),
    "--citations",
    (
        "Srivastava, Nitish; Hinton, Geoffrey; Krizhevsky, Alex; Sutskever, Ilya and "
        "Salakhutdinov, Ruslan 2014 JMLR 'Dropout: A Simple Way to Prevent Neural Networks "
        "from Overfitting' — independently dropping units with probability p thins "
        "co-adapted features, so a smaller p leaves more units available for rare weekend "
        "residual mappings. Relevance: Exp136 uses p=0.2 and Saturday still over-cleans "
        "pred_d -0.91 versus need +0.19 at 20.98 versus CatBoost 20.35, and p=0.3 already "
        "taxed 2013 val, so setting unused dropout to 0.1 is one opposite regularizer on "
        "the Exp136 recipe, not another Adam lr."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting dropout from 0.2 to 0.1 on the Exp136 MLP recipe "
        "(batch 16, hidden 256-128-64, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val RMSE "
        "because the mechanism is weaker unit dropout so Saturday-specific residual units "
        "are not thinned into weekday mean-reversion. Per Srivastava et al. 2014 that is "
        "dropout at lower p. Because p=0.3 taxed val and lr=1e-3 was inert, this is unused "
        "p=0.1 not another lr. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if p=0.2 Saturday over-clean was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
