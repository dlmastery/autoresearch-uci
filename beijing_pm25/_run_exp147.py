"""Exp147 — MLP add cv_inv on Exp136 recipe (MLP cycle 23/50)."""
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
    "--add-feature", "cv_inv",
    "--description", "MLP add cv_inv on Exp136 recipe (MLP cycle 23/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96, hour 20 32.19, onset 110.39. New: cv inversion>=q75 n=486 "
        "RMSE 19.55 versus CatBoost 19.03 and persist 20.77, need +0.58 pred_d -1.67 so "
        "the net over-cleans dry-calm hours (mean inversion 19.4, 5.6 percent of SSE). "
        "vent_index is Iws times inversion and Iws is ~2 on cv so it cannot name this. "
        "Add unused cv_inv, do not retry dow_sin."
    ),
    "--citations",
    (
        "Guo, Song; Hu, Min; Zamora, Misti L.; Peng, Jianfei; Shang, Dongjie; Zheng, "
        "Jing; Du, Zhuofei; Wu, Zhijun; Shao, Min; Zeng, Limin; Molina, Mario J. and "
        "Zhang, Renyi 2014 Science 'Elucidating severe urban haze formation in China' — "
        "urban haze sits in a stagnant moist residual layer, so calm hours with large "
        "dewpoint depression are a different trap-versus-cleanout regime than calm-moist. "
        "Relevance: Exp136 already has vent_index equals Iws times inversion but on cv "
        "hours Iws is about 2 so dry-calm still over-cleans pred_d -1.67 versus need "
        "+0.58, and adding unused cv times inversion is one calm-stability product on "
        "the Exp136 recipe, not another weekday sine."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding cv_inv on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus cbwd_cv times inversion) "
        "will cut 2013 val RMSE because the mechanism is an explicit dry-calm product so "
        "high-inversion cv hours are not treated as generic dry cleanout. Per Guo et al. "
        "2014 that is stagnant-layer chemistry. Because dow_sin just inverted 2013 val, "
        "this is unused cv_inv not another weekday encoding. KEEP if 1h composite beats "
        "-22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.00, and composite -23.00 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if dry-calm over-clean was a 2013 tax. A val RMSE above 22.85 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
