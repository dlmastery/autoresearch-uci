"""Exp194 — FT-Transformer Pre-LN add is_severe on Exp192 champion (FT cycle 20/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--add-feature", "is_severe",
    "--description", "FT-Transformer Pre-LN add is_severe on Exp192 recipe (FT cycle 20/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). se_iws closed. New: lag1>=250 and |need|<=10 n=201 "
        "RMSE 21.39 versus persist 5.94 (2.76 percent of SSE; need +0.03 pred_d -7.46) so "
        "stable mega-haze hours are over-cleaned 3.6 times persist, and Exp167 was 15.28 "
        "with pred_d -4.42. Unused change is add is_severe, not another wind product."
    ),
    "--citations",
    (
        "Chen, Yuyu; Ebenstein, Avraham; Greenstone, Michael and Li, Hongbin 2013 Science "
        "'Evidence on the impact of sustained exposure to air pollution on life expectancy "
        "from China's Huai River policy' — winter heating north of the Huai River produces "
        "sustained high PM, not hour-to-hour spikes that mean-revert, so a 1h nowcast should "
        "copy persist on already-severe hours rather than shrink toward the seasonal mean. "
        "Relevance: Exp192 lag1>=250 |need|<=10 is 21.39 versus persist 5.94 with need +0.03 "
        "but pred_d -7.46; adding is_severe is one unused HJ-633 breakpoint token on Exp192, "
        "not another se_iws wind product."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding is_severe on the Exp192 Pre-LN FT champion (d_model 64, "
        "n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws) will "
        "cut 2013 val RMSE because the mechanism is an explicit lag1>=250 token so stable "
        "mega-haze hours copy persist instead of over-cleaning (need +0.03, Exp192 pred_d "
        "-7.46, RMSE 21.39 versus persist 5.94). Per Chen et al. 2013 that is sustained "
        "heating-season exposure. Because se_iws DISCARD, this is unused severe flag not "
        "another wind product. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if the extra token stops stable-severe over-clean. A val RMSE above 22.40 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
