"""Exp144 — MLP add is_janfeb on Exp136 recipe (MLP cycle 20/50)."""
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
    "--add-feature", "is_janfeb",
    "--description", "MLP add is_janfeb on Exp136 recipe (MLP cycle 20/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: February n=597 RMSE "
        "25.74 versus CatBoost 24.09 and persist 26.01, need -0.12 pred_d -3.14 so the "
        "net over-cleans the coldest high-mean month (mean 166.7, 11.8 percent of SSE). "
        "Feb persist>=150 n=262 RMSE 34.20 loses persist 33.74. Nov-Dec pred_d is near "
        "zero. is_heating lumps them. Add unused is_janfeb, do not retry cbwd_prev_NW."
    ),
    "--citations",
    (
        "Chen, Yuyu; Ebenstein, Avraham; Greenstone, Michael and Li, Hongbin 2013 "
        "Science 'Evidence on the impact of sustained exposure to air pollution on life "
        "expectancy from China's Huai River policy' — residential coal north of the Huai "
        "peaks in the coldest months, so January-February is a different emission regime "
        "than the November-December shoulder already covered by is_heating. Relevance: "
        "Exp136 already has is_heating and month_sin but February still over-cleans "
        "pred_d -3.14 versus need -0.12 and loses CatBoost 25.74 versus 24.09, so adding "
        "unused is_janfeb is one peak-winter dummy on the Exp136 recipe, not another "
        "previous-direction flag."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_janfeb on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus a January-February dummy) "
        "will cut 2013 val RMSE because the mechanism is isolating peak-heating mega-winter "
        "from the Nov-Dec shoulder so February is not treated like milder heating months. "
        "Per Chen et al. 2013 that is Huai-River peak coal. Because cbwd_prev_NW just "
        "inverted 2013 val, this is unused is_janfeb not previous-direction memory. KEEP "
        "if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if February over-clean was a 2013 tax. A val RMSE above 22.85 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
