"""Exp129 — MLP Adam lr 3e-4 to 1e-4 on Exp127 recipe (MLP cycle 5/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "weight_decay=0.0001",
    "--set", "lr=0.0001",
    "--description", "MLP Adam lr=1e-4 on Exp127 recipe (MLP cycle 5/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp127 MLP val 22.528 test "
        "20.773. Exp128 width shrink inverted. New: Iws q3 n=1836 (Iws 5.34 to 17.88, "
        "mean 10.26) is 37.34 percent of Exp127 SSE versus 33.64 percent of Exp97, RMSE "
        "26.41 versus CatBoost 25.03 and persist 28.64. April Iws q3 52.7 loses persist "
        "52.1. persist>=300 n=399 pred_d -3.39 versus need -6.23 (under-cleans). Lower "
        "unused Adam lr, do not retry width or dropout."
    ),
    "--citations",
    (
        "Kingma, Diederik P. and Ba, Jimmy 2015 ICLR 'Adam: A Method for Stochastic "
        "Optimization' (arXiv:1412.6980) — Adam scales each coordinate by a biased "
        "second-moment estimate so the base learning rate is still a free step-size "
        "that controls how far 2010-12 moderate-wind mappings can move in 50 epochs. "
        "Relevance: Exp127 already uses AdamW at default 3e-4 with wd=1e-4, Iws q3 is "
        "37 percent of MLP SSE, and width shrink just inverted, so cutting lr from "
        "3e-4 to 1e-4 is one unused Adam lever on the Exp127 recipe, not another "
        "hidden-width or dropout retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting Adam lr from 3e-4 to 1e-4 on the Exp127 MLP "
        "recipe (hidden 256-128-64, dropout 0.2, weight_decay 1e-4, Smooth-L1, Exp97 "
        "features) will cut 2013 val RMSE because the mechanism is smaller adaptive "
        "steps so 2010-12 Iws-q3 venting co-adaptations cannot lock in before 2013 "
        "April-like moderate-wind hours. Per Kingma and Ba 2015 that is the Adam base "
        "lr. Because width 128-64-32 just failed and dropout 0.3 already failed, this "
        "is unused lr not another width. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.3 to 22.6 versus Exp97 20.735 and Exp127 20.773, val "
        "21.85 to 23.20, and composite -23.20 to -21.85. Val may move from 22.528 toward "
        "22.00 to 22.40 if 3e-4 over-fit 2010-12 Iws-q3. A val RMSE above 22.90 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
