"""Exp193 — FT-Transformer Pre-LN add se_iws on Exp192 champion (FT cycle 19/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--add-feature", "se_iws",
    "--description", "FT-Transformer Pre-LN add se_iws on Exp192 recipe (FT cycle 19/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). rh_iws KEEP was val-side; moist-calm over-clean "
        "worsened. New: January SE persist>=80 n=107 RMSE 53.54 versus persist 54.25 "
        "(9.22 percent of SSE; need +6.42 pred_d -2.22) so winter dirty southerly hours "
        "have the wrong sign, treated like NW cleanout. Unused change is add se_iws, "
        "not another RH ratio."
    ),
    "--citations",
    (
        "Wang, Yuesi; Yao, Li; Wang, Lili; Liu, Zirui; Ji, Dongsheng; Tang, Guiqian; "
        "Zhang, Jinkui; Sun, Yang; Hu, Bo and Xin, Jinyuan 2014 Science China Earth "
        "Sciences 'Mechanism for the formation of the January 2013 heavy haze pollution "
        "episode over central and eastern China' — southerly flow advects a North China "
        "Plain plume into Beijing, so SE wind times Iws is a transport flux not a "
        "cleanout. Relevance: Exp192 January SE persist>=80 is 53.54 versus persist 54.25 "
        "with need +6.42 but pred_d -2.22 (wrong sign); adding se_iws is one unused "
        "SE-speed token on Exp192, not another rh_iws ratio."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding se_iws on the Exp192 Pre-LN FT champion (d_model 64, "
        "n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws) "
        "will cut 2013 val RMSE because the mechanism is an explicit SE times Iws token "
        "so January dirty southerly hours are not over-cleaned like NW (need +6.42, "
        "Exp192 pred_d -2.22, RMSE 53.54 versus persist 54.25). Per Wang et al. 2014 that "
        "is regional advection. Because rh_iws KEEP missed the moist-calm bomb, this is "
        "unused SE flux not another RH ratio. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if the extra token flips January SE from over-clean to a small rise. A val "
        "RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
