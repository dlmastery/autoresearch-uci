"""Exp191 — FT-Transformer Pre-LN add iws_clip100 on Exp186 recipe (FT cycle 17/50)."""
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
    "--add-feature", "iws_clip100",
    "--description", "FT-Transformer Pre-LN add iws_clip100 on Exp186 recipe (FT cycle 17/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp186 Pre-LN +cbwd_prev_NW val 22.066 typical 7.51 "
        "versus champ 7.14. Roll3mean closed. New: Iws>=100 n=323 RMSE 5.71 versus persist "
        "5.40 (0.33 percent of SSE; need -0.32 pred_d +0.08) so storm hours are easy, and "
        "Exp186 over-cleans with pred_d -1.37. Unused change is add iws_clip100, not "
        "another rolling mean."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "FT-Transformer linearly embeds each numeric column so a 441 Iws hour stretches "
        "the token four times a 100 Iws hour, and a clipped twin saturates that scale. "
        "Relevance: Exp167 Iws>=100 is 5.71 versus persist 5.40 with need -0.32 but Exp186 "
        "over-cleans pred_d -1.37; adding iws_clip100 is one unused winsorized-wind token "
        "on Exp186, not another pm25_roll3mean."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding iws_clip100 on the unused Exp186 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW) "
        "with Exp167 features will cut 2013 val RMSE because the mechanism is a capped Iws "
        "token so storm hours cannot over-clean lag-1 (need -0.32, Exp186 pred_d -1.37, "
        "RMSE 5.51 versus persist 5.40). Per Gorishniy et al. 2021 that is feature-as-token. "
        "Because log_iws is already in the recipe and roll3mean DISCARD, this is unused "
        "clipped Iws not another smoother. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.20 versus Exp167 20.072 and Exp186 20.483, val "
        "21.70 to 22.40, and composite -22.40 to -21.70. Val may move from Exp186 22.066 "
        "toward 21.85 to 22.00 if the extra token stops storm over-clean. A val RMSE above "
        "22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
