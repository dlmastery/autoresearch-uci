"""Exp136 — MLP add vent_index on Exp135 recipe (MLP cycle 12/50)."""
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
    "--description", "MLP add vent_index on Exp135 recipe (MLP cycle 12/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp135 MLP val 22.350 test "
        "20.417. New: vent-q3 n=1985 (mean Iws 11.3, inversion 14.0) RMSE 19.71 versus "
        "CatBoost 19.00 and persist 22.59 is 23.3 percent of Exp135 SSE versus 21.0 "
        "percent of Exp97, need -0.80 pred_d -2.54 so the net over-cleans moderate "
        "mixing. Iws and inversion_spread are already additive. Add unused Iws times "
        "inversion, do not retry pm25_accel."
    ),
    "--citations",
    (
        "Guo, Song; Hu, Min; Zamora, Misti L.; Peng, Jianfei; Shang, Dongjie; Zheng, "
        "Jing; Du, Zhuofei; Wu, Zhijun; Shao, Min; Zeng, Limin; Molina, Mario J. and "
        "Zhang, Renyi 2014 Science 'Elucidating severe urban haze formation in China' "
        "— urban haze persists when weak winds coincide with a shallow inversion, so "
        "ventilation is a product not a sum of wind and stability. Relevance: Exp135 "
        "already has Iws, log_iws, and inversion_spread but vent-q3 still over-cleans "
        "pred_d -2.54 versus need -0.80, so adding unused Iws times inversion is one "
        "mixing product on the Exp135 recipe, not another accel or month feature."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding vent_index on the Exp135 MLP recipe (batch 16, "
        "hidden 256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, "
        "month_sin, pm25_accel, Smooth-L1, Exp97 features plus Iws times inversion) "
        "will cut 2013 val RMSE because the mechanism is an explicit mixing product so "
        "moderate-vent hours are not treated like strong-vent over-cleans. Per Guo et "
        "al. 2014 that is wind-times-inversion ventilation. Because pm25_accel just "
        "helped accel-q4 and missed the val gate, this is unused vent_index not another "
        "second-diff. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.5 versus Exp97 20.735 and Exp135 20.417, val "
        "21.70 to 23.05, and composite -23.05 to -21.70. Val may move from 22.350 toward "
        "21.90 to 22.25 if vent-q3 over-clean was a 2013 tax. A val RMSE above 22.90 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
