"""Exp214 — FT-Transformer Pre-LN final_ln=true on Exp192 (FT cycle 40/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--set", "final_ln=true",
    "--description", "FT-Transformer Pre-LN final_ln=true on Exp192 recipe (FT cycle 40/50)",
    "--diagnosis",
    (
        "1h champion is now Exp192 FT Pre-LN +rh_iws: test 20.453, val 21.948 so val is "
        "the bottleneck. January RMSE 33.22 versus persist-1 33.58 (22.86 percent of SSE). "
        "JJA 14.12 versus persist 14.83. Hour 20 32.69 versus persist 33.24 (10.70 percent "
        "of SSE). Onset n=83 RMSE 110.79 losing to persist 107.80 (30.63 percent of SSE; "
        "need +87.40 pred_d -1.54). Extra tokens, drops, patience, batch, lr, FFN, wd, "
        "periodic, pooling, tokenizer, relu, LayerScale, drop_path, n_heads=1, SAM, and "
        "loss=mse closed. New: hour23 persist>=80 n=162 RMSE 25.95 versus persist 25.41 "
        "(3.28 percent of SSE; need +2.64 pred_d -0.06) so midnight dirty hours have the "
        "wrong sign and lose to persist, and Exp167 was 23.27 with pred_d +1.89 beating "
        "persist. Unused change is final_ln=true, not another loss."
    ),
    "--citations",
    (
        "Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; "
        "Zhang, Huishuai; Lan, Yanyan; Wang, Liwei and Liu, Tie-Yan 2020 ICML 'On Layer "
        "Normalization in the Transformer Architecture' (arXiv:2002.04745) — Pre-LN "
        "residual streams grow with depth, so GPT-2 places a final LayerNorm before the "
        "head while PyTorch TransformerEncoder with norm_first omits it. Relevance: "
        "Exp192 Pre-LN has no final LN; hour23 persist>=80 still predicts -0.06 versus "
        "need +2.64 at 25.95 versus persist 25.41 (Exp167 23.27); unused final_ln=true "
        "is one paper Pre-LN fix, not another Smooth L1."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting final_ln=true on the Exp192 Pre-LN FT champion "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW, "
        "rh_iws, shared Linear tokenizer, CLS pooling, GELU, 2d FFN, smooth_l1, no SAM) "
        "will cut 2013 val RMSE because the mechanism is a final LayerNorm on the "
        "unnormalized CLS so midnight dirty hours can rise instead of a mis-scaled "
        "persist copy (need +2.64, Exp192 pred_d -0.06, RMSE 25.95 versus persist 25.41, "
        "Exp167 23.27). Per Xiong et al. 2020 that is GPT-2 Pre-LN. Because loss=mse "
        "DISCARD, this is unused architecture not another loss. KEEP if 1h composite "
        "beats -21.948."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp192 20.453, val 21.70 to 22.40, "
        "and composite -22.40 to -21.70. Val may move from Exp192 21.948 toward 21.85 to "
        "21.94 if final LN lifts hour23 persist>=80 pred_d from -0.06 toward need +2.64. "
        "A val RMSE above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
