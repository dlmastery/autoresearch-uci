"""Exp179 — FT-Transformer Pre-LN dropout=0 on Exp167 features (FT cycle 5/50)."""
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
    "--set", "dropout=0",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN dropout=0 on Exp167 features (FT cycle 5/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN DISCARD val 22.140 test 20.674, typical "
        "7.14 to 7.96, JJA 13.87 to 14.15. New: JJA typical |need|<=10 n=1327 RMSE 5.78 "
        "versus persist 5.22 (1.38 percent of SSE; need +0.53 pred_d +1.44) so the residual "
        "MLP already over-moves easy summer hours, and Exp178 encoder dropout 0.1 can add "
        "Bernoulli noise on that lag-1 skip. Unused change is dropout 0.1 to 0 on Pre-LN, "
        "not a Post-LN revert."
    ),
    "--citations",
    (
        "Srivastava, Nitish; Hinton, Geoffrey; Krizhevsky, Alex; Sutskever, Ilya and "
        "Salakhutdinov, Ruslan 2014 JMLR 'Dropout: A Simple Way to Prevent Neural Networks "
        "from Overfitting' (arXiv:1207.0580) — randomly dropping units prevents co-adaptation "
        "but injects noise into a residual stream that already encodes last-hour identity. "
        "Relevance: Exp178 Pre-LN typical 7.96 versus Exp167 7.14 and JJA typical 5.78 versus "
        "persist 5.22 (pred_d +1.44 versus need +0.53); encoder dropout 0.1 still perturbs "
        "lag-1 on easy summer hours, so dropout=0 is the unused opposite of paper 0.1, not "
        "another depth or Post-LN retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting dropout=0 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, norm_first true, AdamW lr 1e-4, batch 32, "
        "weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is removing Bernoulli noise from the "
        "Pre-LN residual stream so JJA typical hours keep lag-1 (need +0.53, Exp167 pred_d "
        "+1.44). Per Srivastava et al. 2014 dropout is a regularizer that hurts when identity "
        "is already the right predictor. Because Pre-LN already restored persist versus "
        "Post-LN, this is unused dropout-off, not another architecture. KEEP if 1h composite "
        "beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.40 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.80, and composite -22.80 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if dropout was taxing JJA typical. A val RMSE above 22.80 is "
        "a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
