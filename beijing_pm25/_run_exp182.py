"""Exp182 — FT-Transformer Pre-LN weight_decay=1e-4 on Exp167 features (FT cycle 8/50)."""
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
    "--set", "weight_decay=1e-4",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN weight_decay=1e-4 on Exp167 features (FT cycle 8/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN batch 32 val 22.140 typical 7.96 versus "
        "champ 7.14. Dropout 0/0.2 and batch 64 closed. New: DJF persist>=150 |need|<=10 "
        "n=207 RMSE 16.68 versus persist 6.07 (1.80 percent of SSE; need -0.07 pred_d "
        "-5.60) so winter dirty-stable hours over-clean lag-1, and Exp178 is worse at "
        "23.55 with pred_d -4.92. Unused change is weight_decay 1e-5 to 1e-4 on Pre-LN, "
        "not another dropout or batch."
    ),
    "--citations",
    (
        "Loshchilov, Ilya and Hutter, Frank 2019 ICLR 'Decoupled Weight Decay "
        "Regularization' (arXiv:1711.05101) — AdamW applies lambda times weight-norm "
        "independently of the adaptive second-moment denominator, so raising lambda from "
        "1e-5 to 1e-4 actually shrinks transformer residual weights instead of being "
        "cancelled by Adam. Relevance: Exp178 Pre-LN typical 7.96 versus Exp167 7.14 and "
        "DJF persist>=150 |need|<=10 over-cleans pred_d -5.60 versus need -0.07 at 16.68 "
        "versus persist 6.07 (Exp178 23.55); 10x AdamW decay is unused on Pre-LN, not "
        "another dropout or batch."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting weight_decay=1e-4 on the unused Exp178 Pre-LN FT "
        "recipe (d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW "
        "lr 1e-4, batch 32, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is decoupled L2 so winter dirty-stable "
        "hours cannot over-clean lag-1 (need -0.07, Exp167 pred_d -5.60, RMSE 16.68 versus "
        "persist 6.07). Per Loshchilov and Hutter 2019 that is AdamW weight decay "
        "independent of adaptive moments. Because dropout 0/0.2 and batch 64 already "
        "closed, this is unused stronger decay not another regularizer. KEEP if 1h "
        "composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.30 to 21.40 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.80, and composite -22.80 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if stronger AdamW restores DJF dirty-stable identity. A val "
        "RMSE above 22.80 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
