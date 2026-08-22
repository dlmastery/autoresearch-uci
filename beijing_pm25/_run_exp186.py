"""Exp186 — FT-Transformer Pre-LN add cbwd_prev_NW on Exp167 features (FT cycle 12/50)."""
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
    "--add-feature", "cbwd_prev_NW",
    "--description", "FT-Transformer Pre-LN add cbwd_prev_NW on Exp167 features (FT cycle 12/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN val 22.140 typical 7.96 versus champ "
        "7.14. Schedule closed (lr 3e-4, warmup 0/20). New: prevNW then cv persist>=80 "
        "n=114 RMSE 29.35 versus persist 31.68 (3.07 percent of SSE; need -8.12 pred_d "
        "-2.25) so last-hour NW then calm under-cleans, and Exp178 is worse at 31.35 with "
        "pred_d -2.43. Unused change is add cbwd_prev_NW, not another HP."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "FT-Transformer embeds each column as its own token so a lagged categorical dummy "
        "becomes one extra key the CLS can attend to without changing depth or dropout. "
        "Relevance: Exp167 prevNW-then-cv persist>=80 under-cleans pred_d -2.25 versus "
        "need -8.12 at 29.35 versus persist 31.68 (Exp178 31.35); adding cbwd_prev_NW is "
        "one unused wind-regime token on the Exp178 Pre-LN recipe, not another warmup."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding cbwd_prev_NW on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10) with Exp167 "
        "features will cut 2013 val RMSE because the mechanism is one extra token so "
        "prevNW-then-calm dirty hours can keep dropping (need -8.12, Exp167 pred_d -2.25, "
        "Exp178 RMSE 31.35 versus champ 29.35). Per Gorishniy et al. 2021 that is "
        "feature-as-token. Because schedule HPs already closed, this is unused feature "
        "not another lr. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.40 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.80, and composite -22.80 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if the extra token steps prevNW-then-cv washout. A val "
        "RMSE above 22.80 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
