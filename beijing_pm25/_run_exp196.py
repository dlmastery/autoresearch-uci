"""Exp196 — FT-Transformer Pre-LN drop pm25_accel keep delta1 on Exp192 (FT cycle 22/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--drop-feature", "pm25_accel",
    "--description", "FT-Transformer Pre-LN drop pm25_accel keep delta1 on Exp192 recipe (FT cycle 22/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens closed after three DISCARDs. New: "
        "need>=30 accel<=0 n=121 RMSE 80.99 versus persist 78.35 (23.86 percent of SSE; "
        "need +55.19 pred_d -1.01) so the second-diff token sign-flips at inflections "
        "and over-cleans a +55 jump. Unused change is drop pm25_accel keep delta1, not "
        "another extra column."
    ),
    "--citations",
    (
        "Bai, Shaojie; Kolter, J. Zico and Koltun, Vladlen 2018 ICML 'An Empirical "
        "Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling' "
        "(arXiv:1803.01271) — sequence models already see the raw lag trajectory, so an "
        "explicit second difference can sign-flip at inflections and hurt more than it "
        "helps. Relevance: Exp192 already has 24 lags plus pm25_delta1 but need>=30 "
        "accel<=0 still predicts pred_d -1.01 versus need +55.19 at 80.99 versus persist "
        "78.35 and 23.86 percent of SSE; dropping unused pm25_accel is one inflection "
        "cleanup on Exp192, not another extra token."
    ),
    "--hypothesis",
    (
        "We hypothesize that dropping pm25_accel while keeping 24 lags and pm25_delta1 on "
        "the Exp192 Pre-LN FT champion (d_model 64, n_heads 4, n_layers 3, dropout 0.1, "
        "norm_first true, AdamW lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience "
        "15, warmup 10, cbwd_prev_NW, rh_iws) will cut 2013 val RMSE because the mechanism "
        "is removing a second-diff token that tells the CLS to drop when accel is negative "
        "even though the next hour jumps +55 (need +55.19, Exp192 pred_d -1.01, RMSE 80.99 "
        "versus persist 78.35). Per Bai et al. 2018 that is lag trajectory versus a "
        "sign-flipping difference. Because extra tokens DISCARD three times, this is unused "
        "drop-accel not another column. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if dropping accel flips contra-accel hours from pred_d -1.01 toward a small "
        "rise. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
