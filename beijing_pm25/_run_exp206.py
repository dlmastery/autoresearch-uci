"""Exp206 — FT-Transformer Pre-LN pooling=mean on Exp192 champion (FT cycle 32/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "pooling=mean",
    "--description", "FT-Transformer Pre-LN pooling=mean on Exp192 recipe (FT cycle 32/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch, lr, "
        "FFN-widen, wd, and periodic embeddings closed. New: persist>=200 |need|<=10 n=338 "
        "RMSE 18.87 versus persist 6.00 (3.62 percent of SSE; need -0.10 pred_d -5.83) so "
        "stable mega-haze over-cleans 3x persist, and Exp167 was 14.09 with pred_d -3.59. "
        "Unused change is pooling=mean, not another periodic tokenizer."
    ),
    "--citations",
    (
        "Reimers, Nils and Gurevych, Iryna 2019 EMNLP 'Sentence-BERT: Sentence Embeddings "
        "using Siamese BERT-Networks' (arXiv:1908.10084) — mean pooling of all token states "
        "beats the CLS token for a single vector, so lag-1 persist is not drowned by weather "
        "keys. Relevance: Exp192 reads only CLS; persist>=200 |need|<=10 over-cleans pred_d "
        "-5.83 versus need -0.10 at 18.87 versus persist 6.00 (Exp167 14.09); unused "
        "pooling=mean is one paper pool, not another periodic embed."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting pooling=mean on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, linear tokenizer, 2d FFN) will cut 2013 val RMSE because the mechanism is "
        "averaging every token so stable mega-haze copies persist instead of CLS-driven "
        "over-clean (need -0.10, Exp192 pred_d -5.83, RMSE 18.87 versus persist 6.00, "
        "Exp167 14.09). Per Reimers and Gurevych 2019 that is MEAN pooling. Because "
        "periodic embeddings DISCARD, this is unused architecture not another tokenizer. "
        "KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if mean pooling lifts persist>=200 |need|<=10 pred_d from -5.83 toward need "
        "-0.10. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
