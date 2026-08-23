"""Exp202 — FT-Transformer Pre-LN lr=5e-5 on Exp192 champion (FT cycle 28/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "lr=5e-5",
    "--description", "FT-Transformer Pre-LN lr=5e-5 on Exp192 recipe (FT cycle 28/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience both sides, "
        "and batch 16 closed. New: heating Iws<2 persist>=150 n=333 RMSE 38.43 versus "
        "persist 37.04 (14.79 percent of SSE; need +0.45 pred_d -4.81) so winter calm "
        "mega-haze over-cleans and loses to persist, and Exp167 was 34.88 with pred_d "
        "-1.64. Unused change is lr=5e-5, not another batch."
    ),
    "--citations",
    (
        "Goyal, Priya; Dollar, Piotr; Girshick, Ross; Noordhuis, Pieter; Wesolowski, "
        "Lukasz; Kyrola, Andrew; Tulloch, Andrew; Jia, Yangqing and He, Kaiming 2017 "
        "arXiv 'Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour' "
        "(arXiv:1706.02677) — the linear scaling rule says learning rate should scale "
        "with batch size, so a too-large LR at a given batch oversteps the basin. "
        "Relevance: Exp201 batch 16 at lr 1e-4 inverted hour20 persist>=80 and global "
        "bias -3.93; unused lr=5e-5 at batch 32 is the Goyal-scaled complement that "
        "should damp heating Iws<2 persist>=150 over-clean pred_d -4.81 versus need +0.45."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting lr=5e-5 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws) will cut 2013 val RMSE because the mechanism is smaller AdamW steps so "
        "winter calm mega-haze over-cleans less (need +0.45, Exp192 pred_d -4.81, RMSE "
        "38.43 versus persist 37.04, Exp167 34.88). Per Goyal et al. 2017 that is linear "
        "LR scaling at fixed batch 32. Because batch 16 DISCARD with bias -3.93, this is "
        "unused lower lr not another batch. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if smaller steps lift heating Iws<2 persist>=150 pred_d from -4.81 toward "
        "need +0.45. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
