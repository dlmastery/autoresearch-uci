"""Exp211 — FT-Transformer Pre-LN n_heads=1 on Exp192 (FT cycle 37/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "n_heads=1",
    "--description", "FT-Transformer Pre-LN n_heads=1 on Exp192 recipe (FT cycle 37/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN-widen, "
        "wd, periodic embeddings, pooling, per-feature tokenizer, activation=relu, "
        "LayerScale, and drop_path closed. New: need>20 Iws>=10 n=138 RMSE 70.15 versus "
        "persist 68.21 (20.42 percent of SSE; need +43.26 pred_d -0.12) so windy jumps "
        "capture 0 percent of the rise and lose to persist, and Exp167 was 70.38 with "
        "pred_d +0.67. Unused change is n_heads=1, not another drop_path."
    ),
    "--citations",
    (
        "Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; "
        "Gomez, Aidan N.; Kaiser, Lukasz and Polosukhin, Illia 2017 NeurIPS 'Attention "
        "Is All You Need' (arXiv:1706.03762) — multi-head attention splits subspaces so "
        "one head can attend to wind-cleanout while another copies persist, and a single "
        "head forces one softmax over both. Relevance: Exp192 uses 4 heads; need>20 "
        "Iws>=10 still predicts -0.12 versus need +43.26 at 70.15 versus persist 68.21 "
        "(Exp167 70.38); unused n_heads=1 is one paper ablation, not another stochastic "
        "depth."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting n_heads=1 on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, rh_iws, "
        "shared Linear tokenizer, CLS pooling, GELU, 2d FFN, no LayerScale, no drop_path) "
        "will cut 2013 val RMSE because the mechanism is one softmax over persist and "
        "Iws so windy jumps keep lag-1 instead of a dedicated cleanout head (need +43.26, "
        "Exp192 pred_d -0.12, RMSE 70.15 versus persist 68.21, Exp167 70.38). Per Vaswani "
        "et al. 2017 that is single-head attention. Because drop_path DISCARD, this is "
        "unused architecture not another residual skip. KEEP if 1h composite beats "
        "-21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if one head lifts need>20 Iws>=10 pred_d from -0.12 toward need +43.26. "
        "A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
