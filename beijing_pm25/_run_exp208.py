"""Exp208 — FT-Transformer Pre-LN activation=relu on Exp192 (FT cycle 34/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "activation=relu",
    "--description", "FT-Transformer Pre-LN activation=relu on Exp192 recipe (FT cycle 34/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch, lr, "
        "FFN-widen, wd, periodic embeddings, pooling=mean, and per-feature tokenizer "
        "closed. New: TEMP<0 persist>=150 n=367 RMSE 37.12 versus persist 36.32 (15.20 "
        "percent of SSE; need -6.97 pred_d -9.74) so frozen mega-haze over-cleans and "
        "loses to persist, and Exp167 was 33.79 with pred_d -9.49. Unused change is "
        "activation=relu, not another tokenizer."
    ),
    "--citations",
    (
        "Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; "
        "Gomez, Aidan N.; Kaiser, Lukasz and Polosukhin, Illia 2017 NeurIPS 'Attention "
        "Is All You Need' (arXiv:1706.03762) — the original Transformer FFN uses ReLU, "
        "which hard-zeros negative pre-activations so a weather-driven negative residual "
        "cannot leak through a GELU tail. Relevance: Exp192 hardcodes GELU; TEMP<0 "
        "persist>=150 still over-cleans pred_d -9.74 versus need -6.97 at 37.12 versus "
        "persist 36.32 (Exp167 33.79); unused activation=relu is one paper FFN, not "
        "another tokenizer."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting activation=relu on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, 2d FFN) will cut 2013 val RMSE "
        "because the mechanism is hard-zeroing negative FFN units so frozen mega-haze "
        "stops over-cleaning via GELU leak (need -6.97, Exp192 pred_d -9.74, RMSE 37.12 "
        "versus persist 36.32, Exp167 33.79). Per Vaswani et al. 2017 that is the ReLU "
        "FFN. Because per-feature tokenizer DISCARD, this is unused architecture not "
        "another tokenizer. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if ReLU lifts TEMP<0 persist>=150 pred_d from -9.74 toward need -6.97. "
        "A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
