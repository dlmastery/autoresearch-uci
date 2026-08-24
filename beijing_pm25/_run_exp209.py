"""Exp209 — FT-Transformer Pre-LN LayerScale 0.1 on Exp192 (FT cycle 35/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "layer_scale=0.1",
    "--description", "FT-Transformer Pre-LN LayerScale 0.1 on Exp192 recipe (FT cycle 35/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN-widen, "
        "wd, periodic embeddings, pooling=mean, per-feature tokenizer, and activation=relu "
        "closed. New: cbwd_cv persist>=200 n=308 RMSE 31.65 versus persist 29.22 (9.28 "
        "percent of SSE; need +0.68 pred_d -3.64) so calm-variable mega-haze over-cleans "
        "and loses to persist, and Exp167 was 28.41 with pred_d -0.33. Unused change is "
        "LayerScale 0.1, not another activation."
    ),
    "--citations",
    (
        "Touvron, Hugo; Cord, Matthieu; Sablayrolles, Alexandre; Synnaeve, Gabriel and "
        "Jegou, Herve 2021 IEEE International Conference on Computer Vision 'Going "
        "deeper with Image Transformers' (arXiv:2103.17239) — LayerScale multiplies "
        "each residual branch by a learned diagonal initialized at 0.1 so Pre-LN stacks "
        "cannot dump a large correction in early training. Relevance: Exp192 Pre-LN "
        "residuals over-clean cbwd_cv persist>=200 pred_d -3.64 versus need +0.68 at "
        "31.65 versus persist 29.22 (Exp167 28.41); unused layer_scale=0.1 is one paper "
        "residual gate, not another FFN activation."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting layer_scale=0.1 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, GELU, 2d FFN) will cut 2013 val "
        "RMSE because the mechanism is a learned residual diagonal init 0.1 so calm-"
        "variable mega-haze copies persist instead of over-cleaning (need +0.68, Exp192 "
        "pred_d -3.64, RMSE 31.65 versus persist 29.22, Exp167 28.41). Per Touvron et "
        "al. 2021 that is LayerScale. Because activation=relu DISCARD, this is unused "
        "architecture not another FFN. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if LayerScale lifts cbwd_cv persist>=200 pred_d from -3.64 toward need "
        "+0.68. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
