"""Exp207 — FT-Transformer Pre-LN per-feature tokenizer on Exp192 (FT cycle 33/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "feature_tokenizer=per_feature",
    "--description", "FT-Transformer Pre-LN per-feature tokenizer on Exp192 recipe (FT cycle 33/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, collinear drops, patience, batch, lr, "
        "FFN-widen, wd, periodic embeddings, and pooling=mean closed. New: Iws<1 "
        "persist>=150 n=393 RMSE 28.97 versus persist 27.51 (9.92 percent of SSE; need "
        "+0.38 pred_d -0.69) so calm mega-haze over-cleans and loses to persist, and "
        "Exp167 was 26.72 with pred_d +1.19. Unused change is per-feature tokenizer, "
        "not another mean pool."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) "
        "— the Feature Tokenizer maps numerical column j by its own affine "
        "T_j(x_j)=b_j+x_j W_j so lag-1 and wind do not share one Linear(1,d) scale. "
        "Relevance: Exp192 uses a shared Linear(1,64); Iws<1 persist>=150 still "
        "over-cleans pred_d -0.69 versus need +0.38 at 28.97 versus persist 27.51 "
        "(Exp167 26.72); unused feature_tokenizer=per_feature is one paper tokenizer, "
        "not another CLS pool."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting feature_tokenizer=per_feature on the Exp192 Pre-LN "
        "FT champion (d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, "
        "AdamW lr 1e-4, batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, "
        "cbwd_prev_NW, rh_iws, linear embedding, CLS pooling, 2d FFN) will cut 2013 val "
        "RMSE because the mechanism is a separate W_j for Iws versus pm25_lag1 so calm "
        "mega-haze copies persist instead of sharing the wind scale (need +0.38, Exp192 "
        "pred_d -0.69, RMSE 28.97 versus persist 27.51, Exp167 26.72). Per Gorishniy et "
        "al. 2021 that is the Feature Tokenizer. Because pooling=mean DISCARD, this is "
        "unused architecture not another pool. KEEP if 1h composite beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if per-feature tokens lift Iws<1 persist>=150 pred_d from -0.69 toward "
        "need +0.38. A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen "
        "timestamps."
    ),
])
