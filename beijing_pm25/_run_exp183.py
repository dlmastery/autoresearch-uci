"""Exp183 — FT-Transformer Pre-LN lr=3e-4 on Exp167 features (FT cycle 9/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "ft_transformer",
    "--set", "d_model=64",
    "--set", "n_heads=4",
    "--set", "n_layers=3",
    "--set", "dropout=0.1",
    "--set", "lr=0.0003",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN lr=3e-4 on Exp167 features (FT cycle 9/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN lr 1e-4 val 22.140 typical 7.96 versus "
        "champ 7.14. Dropout 0/0.2, batch 64, and weight_decay 1e-4 closed. New: Ir>0 "
        "persist>=50 n=179 RMSE 28.75 versus persist 32.21 (4.62 percent of SSE; need "
        "-9.08 pred_d -3.36) so rain washout under-moves, and Exp178 is worse at pred_d "
        "-1.48. Unused change is lr 1e-4 to 3e-4 on Pre-LN, not another regularizer."
    ),
    "--citations",
    (
        "Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; "
        "Zhang, Huishuai; Lan, Yanyan; Wang, Liwei and Liu, Tie-Yan 2020 ICML 'On Layer "
        "Normalization in the Transformer Architecture' (arXiv:2002.04745) — Pre-LN keeps "
        "the residual stream unnormalized so gradient scale stays independent of depth and "
        "the encoder can use a larger learning rate than Post-LN. Relevance: Exp178 already "
        "switched to Pre-LN but kept the Post-LN paper-default lr 1e-4, and rain washout "
        "Ir>0 persist>=50 under-moves pred_d -1.48 versus need -9.08 at 29.45 versus persist "
        "32.21; raising lr to 3e-4 is unused Pre-LN step size, not another dropout or wd."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting lr=3e-4 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is a larger Pre-LN residual step so rain "
        "washout hours can drop with lag-1 (need -9.08, Exp167 pred_d -3.36, Exp178 pred_d "
        "-1.48). Per Xiong et al. 2020 that is Pre-LN larger-lr stability. Because dropout, "
        "batch, and wd already closed, this is unused optimizer step not another "
        "regularizer. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.50 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.90, and composite -22.90 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if 3x lr steps rain washout. A val RMSE above 22.90 is a "
        "miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
