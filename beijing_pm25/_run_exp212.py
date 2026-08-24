"""Exp212 — FT-Transformer Pre-LN SAM rho=0.05 on Exp192 (FT cycle 38/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "sam_rho=0.05",
    "--description", "FT-Transformer Pre-LN SAM rho=0.05 on Exp192 recipe (FT cycle 38/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN-widen, "
        "wd, periodic embeddings, pooling, tokenizer, relu, LayerScale, drop_path, and "
        "n_heads=1 closed. New: cbwd_SE persist>=80 need>20 n=189 RMSE 61.14 versus "
        "persist 61.32 (21.24 percent of SSE; need +41.20 pred_d +3.20) so southerly "
        "jumps capture 8 percent of the rise and tie persist, and Exp167 was 61.08 with "
        "pred_d +4.03. Unused change is SAM rho=0.05, not another n_heads."
    ),
    "--citations",
    (
        "Foret, Pierre; Kleiner, Ariel; Mobahi, Hossein and Neyshabur, Behnam 2021 ICLR "
        "'Sharpness-Aware Minimization for Efficiently Improving Generalization' "
        "(arXiv:2010.01412) — a first-order ascent of radius rho finds a flat neighbor "
        "so 2013 val does not pay for a sharp 2010-12 southerly-jump minimum. Relevance: "
        "Exp192 AdamW sits in a sharp basin; cbwd_SE persist>=80 need>20 still predicts "
        "+3.20 versus need +41.20 at 61.14 versus persist 61.32 (Exp167 61.08); unused "
        "sam_rho=0.05 is one paper flat-minima step, not another head count."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting sam_rho=0.05 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, GELU, 2d FFN) will cut 2013 val "
        "RMSE because the mechanism is a worst-case neighbor of radius 0.05 so southerly "
        "jumps can rise instead of a sharp persist copy (need +41.20, Exp192 pred_d "
        "+3.20, RMSE 61.14 versus persist 61.32, Exp167 61.08). Per Foret et al. 2021 "
        "that is SAM. Because n_heads=1 DISCARD, this is unused training not another "
        "attention width. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if SAM lifts cbwd_SE persist>=80 need>20 pred_d from +3.20 toward need "
        "+41.20. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
