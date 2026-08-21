"""Exp177 — FT-Transformer n_layers=2 on Exp167 features (FT cycle 3/50)."""
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
    "--set", "n_layers=2",
    "--set", "dropout=0.1",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--description", "FT-Transformer n_layers=2 on Exp167 features (FT cycle 3/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp175 n_layers=3 DISCARD val 22.698 test 23.130; "
        "Exp176 n_layers=1 DISCARD val 25.443 test 25.954 worse. New: typical |need|<=10 "
        "and |pred_d|>=5 n=1514 RMSE 10.54 versus persist 5.48 (5.26 percent of SSE; need "
        "+0.89 pred_d +0.93) so the residual MLP already over-moves 1514 calm hours, and "
        "one FT layer made typical 7.14 to 12.12 while three layers made 10.22. Unused "
        "change is n_layers=2, the middle depth, not another shrink to 1 or d_model 32."
    ),
    "--citations",
    (
        "Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; "
        "Zhang, Huishuai; Lan, Yanyan; Wang, Liwei and Liu, Tie-Yan 2020 ICML 'On Layer "
        "Normalization in the Transformer Architecture' (arXiv:2002.04745) — post-norm "
        "stacks wash the residual stream as depth grows, while a modest number of blocks "
        "can still mix tokens without erasing the input path. Relevance: this FT encoder "
        "is PyTorch post-norm (norm_first off); Exp176 one layer underfit val 25.443 and "
        "Exp175 three layers buried lag-1 (typical 10.22 versus persist 5.08), so n_layers=2 "
        "is the unused middle depth on typical |pred_d|>=5 hours, not another d_model retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting n_layers=2 on the unused FT-Transformer paper recipe "
        "(d_model 64, n_heads 4, dropout 0.1, AdamW lr 1e-4, batch 32, weight_decay 1e-5, "
        "epochs 100, patience 15, warmup 10) with Exp167 features will cut 2013 val RMSE "
        "versus both Exp175 and Exp176 because the mechanism is two post-norm blocks that "
        "mix tokens without three stacked overwrites of lag-1 on typical |pred_d|>=5 hours "
        "(n=1514, need +0.89). Per Xiong et al. 2020 that is a shallower residual stream. "
        "Because n_layers=1 underfit and n_layers=3 buried persist, this is unused middle "
        "depth, not another d_model or MLP wrap. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 21.4 to 25.4 versus Exp167 20.072, Exp175 23.130 and Exp176 "
        "25.954, val 22.10 to 25.20, and composite -25.20 to -22.10. If two layers interpolate "
        "depth, val may sit in 22.70 to 24.00. A val RMSE above 25.20 is a miss versus both "
        "prior FT depths. Ranges are ug/m3 on the frozen timestamps."
    ),
])
