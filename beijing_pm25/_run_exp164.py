"""Exp164 — MLP hidden 512-256-128 widen on Exp136 recipe (MLP cycle 40/50)."""
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
    "--add-feature", "pm25_accel",
    "--add-feature", "vent_index",
    "--description", "MLP hidden 512-256-128 on Exp136 recipe (MLP cycle 40/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. Exp163 drop "
        "cbwd_cv missed val 22.350. New: need>=30 build n=309 RMSE 65.12 versus persist "
        "64.39 and CatBoost 64.51 (39.2 percent of SSE), need +50.54 pred_d +1.23 so the "
        "256-wide net is persist-locked on jumps. Typical |need|<=10 already beats "
        "CatBoost 7.21 versus 8.35. Widen unused hidden to 512-256-128, do not retry shrink."
    ),
    "--citations",
    (
        "Kaplan, Jared; McCandlish, Sam; Henighan, Tom; Brown, Tom B.; Chess, Benjamin; "
        "Child, Rewon; Gray, Scott; Radford, Alec; Wu, Jeffrey and Amodei, Dario 2020 "
        "arXiv 'Scaling Laws for Neural Language Models' (arXiv:2001.08361) — test loss "
        "falls as a power of model width, so doubling first-layer units adds rank for rare "
        "high-gradient events without changing depth. Relevance: Exp136 typical already "
        "beats CatBoost 7.21 versus 8.35 but need>=30 build still loses persist 65.12 "
        "versus 64.39 with pred_d +1.23 versus need +50.54 at 39.2 percent of SSE, so "
        "widening hidden 256-128-64 to 512-256-128 is one unused capacity raise on the "
        "Exp136 recipe, not another extra layer or width shrink."
    ),
    "--hypothesis",
    (
        "We hypothesize that widening hidden from 256-128-64 to 512-256-128 on the "
        "Exp136 MLP recipe (batch 16, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, "
        "log_iws, month_sin, pm25_accel, vent_index, Smooth-L1, clip=1.0) will cut 2013 "
        "val RMSE because the mechanism is more first-layer GELU directions so "
        "persist-locked build hours with need +50.54 are not forced through a 256-unit "
        "bottleneck that only moves pred_d +1.23. Per Kaplan et al. 2020 that is width "
        "scaling. Because drop cbwd_cv just missed val and Exp128 shrink already failed, "
        "this is unused widen not another drop or shrink. KEEP if 1h composite beats "
        "-22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.8 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.20, and composite -23.20 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if the 256-wide build bottleneck was a 2013 tax. A val RMSE above "
        "22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
