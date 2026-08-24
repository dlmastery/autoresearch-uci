"""Exp210 — FT-Transformer Pre-LN drop_path=0.1 on Exp192 (FT cycle 36/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "drop_path=0.1",
    "--description", "FT-Transformer Pre-LN drop_path=0.1 on Exp192 recipe (FT cycle 36/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN-widen, "
        "wd, periodic embeddings, pooling=mean, per-feature tokenizer, activation=relu, "
        "and LayerScale closed. New: month2 persist>=150 n=262 RMSE 34.48 versus persist "
        "33.74 (9.36 percent of SSE; need -2.03 pred_d -8.61) so February mega-haze "
        "over-cleans 4x and loses to persist, and Exp167 was 32.79 with pred_d -6.70. "
        "Unused change is drop_path=0.1, not another LayerScale."
    ),
    "--citations",
    (
        "Huang, Gao; Sun, Yu; Liu, Zhuang; Sedra, Daniel and Weinberger, Kilian Q. 2016 "
        "ECCV 'Deep Networks with Stochastic Depth' (arXiv:1603.09382) — randomly skipping "
        "residual blocks with a linearly ramped probability forces later layers not to "
        "fire a weather residual on every row. Relevance: Exp192 always applies all 3 "
        "Pre-LN blocks; month2 persist>=150 still over-cleans pred_d -8.61 versus need "
        "-2.03 at 34.48 versus persist 33.74 (Exp167 32.79); unused drop_path=0.1 is one "
        "paper identity-skip, not another LayerScale."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting drop_path=0.1 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, GELU, 2d FFN, no LayerScale) will "
        "cut 2013 val RMSE because the mechanism is a linearly ramped identity skip so "
        "February mega-haze copies persist instead of a always-on weather residual "
        "(need -2.03, Exp192 pred_d -8.61, RMSE 34.48 versus persist 33.74, Exp167 32.79). "
        "Per Huang et al. 2016 that is stochastic depth. Because LayerScale DISCARD, this "
        "is unused architecture not another residual scale. KEEP if 1h composite beats "
        "-21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if stochastic depth lifts month2 persist>=150 pred_d from -8.61 toward "
        "need -2.03. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
