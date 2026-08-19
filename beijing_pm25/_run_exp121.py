"""Exp121 — CatBoost Plain add nw_iws on Exp97 1h champion."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain add nw_iws on Exp97 (CatBoost cycle 47/50)",
    "--add-feature", "nw_iws",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. This fire does not retry "
        "border_count (Exp120 val 22.264, January PRES worse). New: hour-20 NW n=66 RMSE "
        "18.55 versus persist 13.83, need +1.88 pred_d -1.49 (wrong sign). NW persist>=150 "
        "Iws>=10 n=101 RMSE 47.82 versus persist 55.06 but pred_d -28.2 versus need -19.15. "
        "Train NW share 32 to 37 percent versus 2013 31.4 and 2014 28.2. Keep dow. Add "
        "NW times Iws, not another regularizer HP."
    ),
    "--citations",
    (
        "Cai, Wenju; Li, Ke; Liao, Hong; Wang, Huijun and Wu, Lixin 2017 Nature Climate "
        "Change 'Weather conditions conducive to Beijing severe haze more frequent under "
        "climate change' — weakened northwesterlies and a weaker Siberian High trap winter "
        "PM2.5, so NW wind times speed is the ventilation dose. Relevance: Exp120 coarsened "
        "PRES borders and over-cleaned more, but hour-20 NW pred_d is -1.49 versus need "
        "+1.88 so binary cbwd_NW over-cleans evenings, and nw_iws is one unused product "
        "from Exp97 after se_iws failed on the opposite (SE) axis."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding nw_iws = cbwd_NW times Iws to the Exp97 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, l2_leaf_reg 3, rh_magnus plus dewp_delta plus "
        "is_heating plus 24 lags plus dow plus is_weekend) will cut 2013 val RMSE because "
        "the mechanism is scaling NW cleanout by wind speed so weak evening NW hours are "
        "not treated like strong Siberian-High flushes. Per Cai et al. 2017 that is "
        "northwesterly ventilation. Because border_count just failed, this is an unused "
        "NW-speed product not another quantization HP. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 21.5 versus Exp97 20.735, val 21.90 to 22.40, "
        "and composite -22.45 to -21.90. Val may move from 22.167 toward 21.90 to 22.20 "
        "if binary NW over-clean was a 2013 tax. A val RMSE above 22.25 is a miss. Ranges "
        "are ug/m3 on the frozen timestamps."
    ),
])
