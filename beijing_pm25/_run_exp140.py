"""Exp140 — MLP add se_iws on Exp136 recipe (MLP cycle 16/50)."""
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
    "--add-feature", "se_iws",
    "--description", "MLP add se_iws on Exp136 recipe (MLP cycle 16/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: SE Iws>=10 n=1483 RMSE "
        "24.43 versus CatBoost 23.63 and persist 25.65, need +1.84 pred_d -0.39 so the "
        "net over-cleans southerly fetch as if it were NW ventilation (26.5 percent of "
        "SSE). log_iws and vent_index already scale wind but not direction. Add unused "
        "se_iws, do not retry evening_peak."
    ),
    "--citations",
    (
        "Wang, Yuesi; Yao, Li; Wang, Lili; Liu, Zirui; Ji, Dongsheng; Tang, Guiqian; "
        "Zhang, Jinkui; Sun, Yang; Hu, Bo and Xin, Jinyuan 2014 Science China Earth "
        "Sciences 'Mechanism for the formation of the January 2013 heavy haze pollution "
        "episode over central and eastern China' — southerly flow advects a North China "
        "Plain plume into Beijing, so SE wind speed is a transport flux not a cleanout. "
        "Relevance: Exp136 already has Iws, log_iws, cbwd_SE, and vent_index but SE "
        "Iws>=10 still predicts -0.39 versus need +1.84 and owns 26.5 percent of SSE, so "
        "adding unused se_iws is one direction-speed product on the Exp136 recipe, not "
        "another hour bin."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding se_iws on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus cbwd_SE times Iws) will "
        "cut 2013 val RMSE because the mechanism is an explicit southerly transport flux "
        "so moderate-strong SE hours are not treated like NW cleanout. Per Wang et al. "
        "2014 that is regional advection. Because evening_peak just inverted 2013 val, "
        "this is unused se_iws not another hour bin. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if SE over-clean was a 2013 tax. A val RMSE above 22.85 is a "
        "miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
