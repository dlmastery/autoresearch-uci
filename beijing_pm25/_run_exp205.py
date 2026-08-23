"""Exp205 — FT-Transformer Pre-LN periodic numerical embeddings on Exp192 (FT cycle 31/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "num_embedding=periodic",
    "--description", "FT-Transformer Pre-LN periodic embeddings on Exp192 recipe (FT cycle 31/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch, lr, "
        "FFN-widen, and wd both sides closed. New: need>20 hour0-5 n=148 RMSE 53.41 versus "
        "persist 51.28 (12.69 percent of SSE; need +40.07 pred_d +0.50) so overnight jumps "
        "capture only 1 percent of the rise and lose to persist, and Exp167 was 52.95 with "
        "pred_d +0.63. Unused change is periodic numerical embeddings, not another wd."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan and Babenko, Artem 2022 NeurIPS 'On Embeddings "
        "for Numerical Features in Tabular Deep Learning' (arXiv:2203.05556) — linear "
        "scalar-to-token maps miss periodic structure, so sin/cos of learned frequencies "
        "give each numerical column a richer token. Relevance: Exp192 uses Linear(1, d); "
        "overnight need>20 hour0-5 still predicts +0.50 versus need +40.07 at 53.41 versus "
        "persist 51.28 (Exp167 52.95); unused num_embedding=periodic is one paper tokenizer, "
        "not another weight decay."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting num_embedding=periodic on the Exp192 Pre-LN FT "
        "champion (d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW "
        "lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, "
        "cbwd_prev_NW, rh_iws, 2d FFN) will cut 2013 val RMSE because the mechanism is "
        "learned Fourier tokens so overnight jump hours can rise instead of copying persist "
        "(need +40.07, Exp192 pred_d +0.50, RMSE 53.41 versus persist 51.28, Exp167 52.95). "
        "Per Gorishniy et al. 2022 that is periodic numerical embeddings. Because wd 1e-6 "
        "DISCARD, this is unused architecture not another decay. KEEP if 1h composite "
        "beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if periodic tokens lift need>20 hour0-5 pred_d from +0.50 toward need "
        "+40.07. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
