"""Exp195 — FT-Transformer Pre-LN add pm25_delta6 on Exp192 champion (FT cycle 21/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--add-feature", "pm25_delta6",
    "--description", "FT-Transformer Pre-LN add pm25_delta6 on Exp192 recipe (FT cycle 21/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). is_severe closed. New: January delta6>20 n=255 RMSE "
        "44.94 versus persist 43.23 (15.49 percent of SSE; need +2.95 pred_d -5.67) so "
        "winter still-building 6h episodes have the wrong sign, treated like mean-reverting "
        "delta1. Unused change is add pm25_delta6, not another lag1 flag."
    ),
    "--citations",
    (
        "Bai, Shaojie; Kolter, J. Zico and Koltun, Vladlen 2018 ICML 'An Empirical "
        "Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling' "
        "(arXiv:1803.01271) — dilated temporal nets treat a several-step lookback slope as "
        "a first-class local trend that a 1-step delta does not span. Relevance: Exp192 "
        "already has pm25_delta1 and pm25_accel but January delta6>20 still predicts -5.67 "
        "versus need +2.95 at 44.94 versus persist 43.23; adding unused lag1-minus-lag7 is "
        "one 6h episode-slope token on Exp192, not another is_severe flag."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pm25_delta6 on the Exp192 Pre-LN FT champion (d_model "
        "64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws) will "
        "cut 2013 val RMSE because the mechanism is an explicit lag1-minus-lag7 token so "
        "January still-building 6h hours are not over-cleaned like mean-reverting delta1 "
        "(need +2.95, Exp192 pred_d -5.67, RMSE 44.94 versus persist 43.23). Per Bai et al. "
        "2018 that is a dilated lookback trend. Because is_severe DISCARD, this is unused "
        "6h slope not another lag1 flag. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if the extra token flips January 6h-build from over-clean to a small rise. "
        "A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
