"""Exp199 — FT-Transformer Pre-LN patience=8 on Exp192 champion (FT cycle 25/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "patience=8",
    "--description", "FT-Transformer Pre-LN patience=8 on Exp192 recipe (FT cycle 25/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck (gap 1.50). January RMSE 33.22 versus persist-1 33.58 (22.86 percent "
        "of SSE). JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 "
        "percent of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of "
        "SSE; need +87.40 pred_d -1.54). Collinear drops closed. New: typical persist>=80 "
        "n=1774 RMSE 10.78 versus persist 5.70 (6.20 percent of SSE; need +0.53 pred_d "
        "-0.07) so dirty-but-stable hours are almost twice persist, and Exp167 was 9.59. "
        "Unused change is patience=8, not another derived drop."
    ),
    "--citations",
    (
        "Caruana, Rich; Lawrence, Steve and Giles, C. Lee 2001 NeurIPS 'Overfitting in "
        "Neural Nets: Backpropagation, Conjugate Gradient, and Early Stopping' — nets "
        "keep fitting after the useful signal saturates, so a shorter early-stop window "
        "can cut val noise on easy examples. Relevance: Exp192 typical persist>=80 is "
        "10.78 versus persist 5.70 with need +0.53 but pred_d -0.07 (6.20 percent of SSE) "
        "and val 21.948 is 1.50 worse than test 20.453; setting unused patience=8 on "
        "Exp192 is one early-stop tighten, not another collinear drop."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting patience=8 on the Exp192 Pre-LN FT champion (d_model "
        "64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, warmup 10, cbwd_prev_NW, rh_iws, inversion_spread, "
        "is_weekend, pm25_accel) will cut 2013 val RMSE because the mechanism is stopping "
        "seven epochs earlier so dirty-but-stable hours copy persist instead of fitting "
        "2013 val noise (need +0.53, Exp192 pred_d -0.07, RMSE 10.78 versus persist 5.70). "
        "Per Caruana et al. 2001 that is early stopping against overfit. Because collinear "
        "drops DISCARD three times, this is unused patience not another drop. KEEP if 1h "
        "composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if earlier stopping cuts the typical persist>=80 tax. A val RMSE above "
        "22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
