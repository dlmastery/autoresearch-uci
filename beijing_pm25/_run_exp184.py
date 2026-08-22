"""Exp184 — FT-Transformer Pre-LN warmup=0 on Exp167 features (FT cycle 10/50)."""
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
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=0",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN warmup=0 on Exp167 features (FT cycle 10/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN warmup 10 val 22.140 typical 7.96 versus "
        "champ 7.14. Dropout, batch 64, wd 1e-4, and lr 3e-4 closed. New: hour2-4 "
        "persist>=80 n=521 RMSE 26.68 versus persist 30.40 (11.58 percent of SSE; need "
        "-5.20 pred_d -6.13) so nocturnal dirty hours dominate residual, and Exp178 is "
        "worse at 28.83 with pred_d -4.66. Unused change is warmup 10 to 0 on Pre-LN, "
        "not another learning rate."
    ),
    "--citations",
    (
        "Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; "
        "Zhang, Huishuai; Lan, Yanyan; Wang, Liwei and Liu, Tie-Yan 2020 ICML 'On Layer "
        "Normalization in the Transformer Architecture' (arXiv:2002.04745) — Pre-LN keeps "
        "the residual stream unnormalized so training is stable at the target learning "
        "rate from step one and does not need a warmup ramp, unlike Post-LN. Relevance: "
        "Exp178 already uses Pre-LN but still ramps 10 epochs from the Post-LN default, "
        "and hour2-4 persist>=80 is 11.58 percent of SSE at 26.68 versus persist 30.40 "
        "(Exp178 28.83); setting warmup=0 is unused Pre-LN schedule, not another lr."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting warmup=0 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is full lr from epoch 1 so nocturnal "
        "dirty hours can track lag-1 (need -5.20, Exp167 pred_d -6.13, Exp178 RMSE 28.83 "
        "versus champ 26.68). Per Xiong et al. 2020 that is Pre-LN without warmup. Because "
        "lr=3e-4 already closed, this is unused schedule not another step size. KEEP if "
        "1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.30 to 21.40 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.80, and composite -22.80 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if no-warmup fits hour2-4 persist. A val RMSE above 22.80 "
        "is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
