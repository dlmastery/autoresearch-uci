"""Exp198 — FT-Transformer Pre-LN drop inversion_spread keep TEMP DEWP on Exp192 (FT cycle 24/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--drop-feature", "inversion_spread",
    "--description", "FT-Transformer Pre-LN drop inversion_spread keep TEMP DEWP on Exp192 recipe (FT cycle 24/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Drop is_weekend closed. New: inv<3 persist>=80 n=628 "
        "RMSE 19.78 versus persist 21.46 (7.39 percent of SSE; need -1.59 pred_d -0.13) so "
        "moist near-saturated dirty hours under-clean, and inversion_spread correlates "
        "-0.95 with rh_magnus and 1.0 with TEMP-DEWP. Unused change is drop inversion_spread "
        "keep TEMP and DEWP, not another calendar dummy."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "FT-Transformer linearly embeds each numeric column as its own token so a perfect "
        "copy of TEMP minus DEWP is a duplicate key already spanned by TEMP, DEWP, and "
        "rh_magnus. Relevance: Exp192 inversion_spread correlates 1.0 with TEMP-DEWP and "
        "-0.95 with rh_magnus, and inv<3 persist>=80 under-cleans pred_d -0.13 versus need "
        "-1.59 at 19.78 versus persist 21.46; dropping unused inversion_spread is one "
        "stability-copy cleanup on Exp192, not another drop-weekend."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping inversion_spread while keeping TEMP and DEWP on the "
        "Exp192 Pre-LN FT champion (d_model 64, n_heads 4, n_layers 3, dropout 0.1, "
        "norm_first true, AdamW lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience "
        "15, warmup 10, cbwd_prev_NW, rh_iws, pm25_accel, is_weekend) will cut 2013 val "
        "RMSE because the mechanism is removing a duplicate TEMP-DEWP token so moist "
        "near-saturated dirty hours are not smeared with rh_magnus (need -1.59, Exp192 "
        "pred_d -0.13, RMSE 19.78 versus persist 21.46). Per Gorishniy et al. 2021 that is "
        "a redundant feature-as-token. Because drop is_weekend DISCARD, this is unused "
        "stability copy not a calendar dummy. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if dropping inversion_spread lets TEMP DEWP and rh_magnus split moist "
        "under-clean. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
