"""Exp134 — MLP add month_sin on Exp133 recipe (MLP cycle 10/50)."""
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
    "--description", "MLP add month_sin on Exp133 recipe (MLP cycle 10/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp133 MLP val 22.502 test "
        "20.587. New: February n=597 RMSE 25.67 versus CatBoost 24.09 and persist 26.01 "
        "is 11.7 percent of Exp133 SSE versus 10.1 percent of Exp97, need -0.12 pred_d "
        "-3.96 so the net over-cleans February. Residual corr with month_sin is -0.078. "
        "is_heating is a Nov-Feb step that aliases February with November. Add unused "
        "cyclic month, do not retry log-Iws."
    ),
    "--citations",
    (
        "Lai, Guokun; Chang, Wei-Cheng; Yang, Yiming and Liu, Hanxiao 2018 SIGIR "
        "'Modeling Long- and Short-Term Temporal Patterns with Deep Neural Networks' "
        "(arXiv:1703.07015) — a periodic skip lets a net use season as its own axis "
        "instead of burying the calendar in a binary flag that aliases unlike months. "
        "Relevance: Exp133 already has is_heating but February still over-cleans 25.67 "
        "versus CatBoost 24.09 and residual corr with month_sin is -0.078, so adding "
        "month_sin is one unused periodic feature on the Exp133 recipe, not another "
        "log-Iws or training-budget HP."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding month_sin on the Exp133 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "Smooth-L1, Exp97 features plus sin 2pi month/12) will cut 2013 val RMSE "
        "because the mechanism is a cyclic month so 2013 February-like hardness is not "
        "collapsed into the same is_heating bit as November. Per Lai et al. 2018 that "
        "is a periodic temporal pattern. Because log_iws just helped rain and missed "
        "the val gate, this is unused month_sin not another Iws transform. KEEP if 1h "
        "composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 22.6 versus Exp97 20.735 and Exp133 20.587, val "
        "21.80 to 23.15, and composite -23.15 to -21.80. Val may move from 22.502 toward "
        "22.00 to 22.35 if February-November aliasing was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
