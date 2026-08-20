"""Exp156 — MLP add rh_iws on Exp136 recipe (MLP cycle 32/50)."""
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
    "--add-feature", "rh_iws",
    "--description", "MLP add rh_iws on Exp136 recipe (MLP cycle 32/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp136 MLP val 22.259 test "
        "20.509, January 30.96 versus JJA 13.96, hour 20 32.19, onset 110.39. heating_build "
        "Exp155 inverted val. New: collapse on rh>=q75 n=45 RMSE 71.72 versus CatBoost "
        "65.80 and persist 81.61, need -75.71 pred_d -11.02 so humid crashes capture only "
        "15 percent of the drop (6.9 percent of SSE). rh_magnus, Iws, and log_iws are "
        "additive. Add unused rh_iws, do not retry heating_build."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Huijun and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' (doi:10.1038/nclimate3249) — Beijing haze traps when weak winds "
        "coincide with high relative humidity, so RH over Iws names a moist-calm cell "
        "that separate humidity and wind inputs miss. Relevance: Exp136 already has "
        "rh_magnus, Iws, log_iws, and vent_index but humid collapse still under-cleans "
        "pred_d -11.02 versus need -75.71 at 71.72 versus CatBoost 65.80, so adding unused "
        "RH divided by Iws plus one is one moist-calm ratio on the Exp136 recipe, not "
        "another heating product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding rh_iws on the Exp136 MLP recipe (batch 16, hidden "
        "256-128-64, dropout 0.2, AdamW lr 3e-4, weight_decay 1e-4, log_iws, month_sin, "
        "pm25_accel, vent_index, Smooth-L1, Exp97 features plus Magnus RH divided by Iws "
        "plus one) will cut 2013 val RMSE because the mechanism is an explicit moist-calm "
        "ratio so humid crash hours are not treated as dry-wind venting. Per Cai et al. "
        "2017 that is the weak-wind high-RH haze trap. Because heating_build just inverted "
        "val, this is unused rh_iws not another heating product. KEEP if 1h composite "
        "beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.1 to 22.6 versus Exp97 20.735 and Exp136 20.509, val "
        "21.70 to 23.10, and composite -23.10 to -21.70. Val may move from 22.259 toward "
        "21.90 to 22.16 if additive RH plus Iws was a 2013 tax. A val RMSE above 22.90 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
