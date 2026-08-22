"""Exp197 — FT-Transformer Pre-LN drop is_weekend keep dow on Exp192 (FT cycle 23/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--drop-feature", "is_weekend",
    "--description", "FT-Transformer Pre-LN drop is_weekend keep dow on Exp192 recipe (FT cycle 23/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Drop-accel closed. New: Sunday persist>=150 n=227 RMSE "
        "33.76 versus persist 37.39 (7.78 percent of SSE; need -10.70 pred_d -6.96) so "
        "Sunday dirty hours under-clean, while Saturday persist>=150 over-cleans pred_d "
        "-3.79 versus need -2.94. is_weekend equals dow>=5 exactly. Unused change is drop "
        "is_weekend keep dow, not another PM derivative."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "FT-Transformer linearly embeds each numeric column as its own token so a dummy "
        "that is a perfect function of another column is a duplicate key the CLS must "
        "attend to. Relevance: Exp192 is_weekend correlates 1.0 with dow>=5, Sunday "
        "persist>=150 under-cleans pred_d -6.96 versus need -10.70 at 33.76 versus persist "
        "37.39 while Saturday over-cleans; dropping unused is_weekend is one collinear "
        "calendar cleanup on Exp192, not another drop-accel."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping is_weekend while keeping dow on the Exp192 Pre-LN "
        "FT champion (d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, "
        "AdamW lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, "
        "cbwd_prev_NW, rh_iws, pm25_accel) will cut 2013 val RMSE because the mechanism is "
        "removing a duplicate weekend token so Sunday dirty hours are not smeared with "
        "Saturday (need -10.70, Exp192 pred_d -6.96, RMSE 33.76 versus persist 37.39). Per "
        "Gorishniy et al. 2021 that is a redundant feature-as-token. Because drop-accel "
        "DISCARD, this is unused calendar collinear not a PM second-diff. KEEP if 1h "
        "composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if dropping is_weekend lets dow split Saturday over-clean from Sunday "
        "under-clean. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
