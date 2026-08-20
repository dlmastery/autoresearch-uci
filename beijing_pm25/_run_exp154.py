"""Exp154 — MLP weight_decay=0 on Exp136 recipe (MLP cycle 30/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0",
    "--set", "batch_size=16",
    "--add-feature", "log_iws",
    "--add-feature", "month_sin",
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP weight_decay=0 on Exp136 recipe (MLP cycle 30/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp127 raised "
        "wd to 1e-4. Exp153 batch 64 taxed val. New: stuck need>20 and |pred_d|<5 n=293 "
        "RMSE 50.33 versus CatBoost 50.03 and persist 50.51, need +37.67 pred_d +0.52 so "
        "AdamW L2 shrinks the residual head to persist (22.2 percent of SSE). Drop unused "
        "wd, do not retry batch 64."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2019 ICLR 'Decoupled Weight Decay "
        "Regularization' (arXiv:1711.05101) — AdamW applies weight decay outside the "
        "adaptive step so L2 actually shrinks hidden weights, including the residual "
        "head that must leave persist. Relevance: Exp136 uses wd=1e-4 and stuck hours "
        "need>20 with |pred_d|<5 still sit at pred_d +0.52 versus need +37.67 at 50.33 "
        "versus persist 50.51, so setting unused weight_decay to 0 is one opposite "
        "AdamW lever on the Exp136 recipe, not another batch size."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting weight_decay from 1e-4 to 0 on the Exp136 MLP "
        "recipe (batch 16, hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, log_iws, "
        "month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 val RMSE "
        "because the mechanism is no decoupled L2 so the residual-from-lag1 head can "
        "grow instead of staying persist-locked at pred_d +0.52. Per Loshchilov and "
        "Hutter 2019 that is AdamW weight decay, inverted. Because Exp127 raised wd and "
        "batch 64 just taxed val, this is unused wd=0 not another batch. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if L2-shrunk residual weights were a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
