"""Exp178 — FT-Transformer Pre-LN (norm_first) on Exp167 features (FT cycle 4/50)."""
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
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN norm_first on Exp167 features (FT cycle 4/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). FT depth {1,2,3} closed: Exp175 post-norm 3-layer val "
        "22.698 typical 10.22; Exp176/177 worse. New: dirty-stable NW persist>=150 "
        "|need|<=10 n=156 RMSE 17.54 versus persist 6.18 (1.50 percent of SSE; need -0.08 "
        "pred_d -9.17) so the residual MLP subtracts 9 ug on already-dirty NW hours that "
        "should stay put, and post-norm FT buried lag-1 further (dirty-stable 11.99 to "
        "24.29). Unused rethink is Pre-LN, not n_layers=4."
    ),
    "--citations",
    (
        "Xiong, Ruibin; Yang, Yunchang; He, Di; Zheng, Kai; Zheng, Shuxin; Xing, Chen; "
        "Zhang, Huishuai; Lan, Yanyan; Wang, Liwei and Liu, Tie-Yan 2020 ICML 'On Layer "
        "Normalization in the Transformer Architecture' (arXiv:2002.04745) — Pre-LN puts "
        "LayerNorm inside the residual branch so the unnormalized skip keeps the input "
        "stream, whereas Post-LN washes that path as depth grows. Relevance: this FT "
        "encoder defaulted to PyTorch post-norm; Exp175 three-layer Post-LN buried lag-1 "
        "on dirty-stable NW hours (Exp167 pred_d -9.17 versus need -0.08 at 17.54 versus "
        "persist 6.18), so setting norm_first=true is one Pre-LN architecture change, not "
        "another depth or d_model retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting norm_first=true on the unused FT-Transformer paper "
        "recipe (d_model 64, n_heads 4, n_layers 3, dropout 0.1, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is a Pre-LN residual stream so lag-1 is "
        "not washed by three Post-LN blocks on dirty-stable NW hours (need -0.08, Exp167 "
        "pred_d -9.17). Per Xiong et al. 2020 that is Pre-LN identity. Because FT depth "
        "{1,2,3} already closed, this is unused architecture not another layer count. KEEP "
        "if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 24.2 versus Exp167 20.072 and Exp175 23.130, val "
        "21.80 to 24.40, and composite -24.40 to -21.80. Val may move from Exp175 22.698 "
        "toward 21.90 to 22.60 if Pre-LN restores lag-1 on dirty-stable NW. A val RMSE "
        "above 24.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
