"""Exp213 — FT-Transformer Pre-LN loss=mse on Exp192 (FT cycle 39/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "loss=mse",
    "--description", "FT-Transformer Pre-LN loss=mse on Exp192 recipe (FT cycle 39/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN-widen, "
        "wd, periodic embeddings, pooling, tokenizer, relu, LayerScale, drop_path, "
        "n_heads=1, and SAM rho=0.05 closed. New: cbwd_NW need>20 n=70 RMSE 57.41 versus "
        "persist 49.98 (6.94 percent of SSE; need +41.41 pred_d -6.25) so northerly jumps "
        "have the wrong sign and lose to persist, and Exp167 was 57.83 with pred_d -7.09. "
        "Unused change is loss=mse, not another SAM radius."
    ),
    "--citations",
    (
        "Girshick, Ross 2015 IEEE ICCV 'Fast R-CNN' (arXiv:1504.08083) — Smooth L1 is "
        "linear past beta=1 so a 47 ug/m3 northerly-jump miss costs about 47 while "
        "hundreds of typical 7 ug hours dominate the sum, and squared error would let "
        "those 70 hours dominate the gradient. Relevance: Exp192 hardcodes smooth_l1 "
        "beta=1; cbwd_NW need>20 still predicts -6.25 versus need +41.41 at 57.41 versus "
        "persist 49.98 (Exp167 57.83); unused loss=mse is one paper L2 step, not another "
        "SAM radius."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting loss=mse on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, GELU, 2d FFN, no SAM) will cut "
        "2013 val RMSE because the mechanism is squared residuals so northerly jumps can "
        "rise instead of a Huber-linear cleanout (need +41.41, Exp192 pred_d -6.25, RMSE "
        "57.41 versus persist 49.98, Exp167 57.83). Per Girshick 2015 that is turning "
        "Smooth L1 off. Because SAM rho=0.05 DISCARD, this is unused loss not another "
        "SAM radius. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if MSE lifts cbwd_NW need>20 pred_d from -6.25 toward need +41.41. A val "
        "RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
