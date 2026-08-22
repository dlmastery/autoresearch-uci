"""Exp188 — FT-Transformer Pre-LN add pres_delta on Exp186 recipe (FT cycle 14/50)."""
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
    "--add-feature", "pres_delta",
    "--description", "FT-Transformer Pre-LN add pres_delta on Exp186 recipe (FT cycle 14/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp186 Pre-LN +cbwd_prev_NW val 22.066 typical 7.51 "
        "versus champ 7.14. Heating_night closed. New: rising P persist>=80 need<-20 n=128 "
        "RMSE 54.57 versus persist 72.02 (11.90 percent of SSE; need -54.38 pred_d -15.93) "
        "so rising-pressure dirty hours under-collapse, and Exp186 is 50.36 with pred_d "
        "-17.52. Unused change is add pres_delta, not another heating dummy."
    ),
    "--citations",
    (
        "Gorishniy, Yury; Rubachev, Ivan; Khrulkov, Valentin and Babenko, Artem 2021 "
        "NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — "
        "FT-Transformer embeds each column as its own token so a first-difference of PRES "
        "becomes one extra key the CLS can attend to while contemporaneous PRES stays. "
        "Relevance: Exp167 rising-pressure persist>=80 need<-20 under-collapses pred_d "
        "-15.93 versus need -54.38 at 54.57 versus persist 72.02 (Exp186 50.36); adding "
        "pres_delta is one unused synoptic token on Exp186, not another heating_night."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding pres_delta on the unused Exp186 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW) "
        "with Exp167 features will cut 2013 val RMSE because the mechanism is one extra "
        "token so rising-pressure dirty hours can collapse with lag-1 (need -54.38, Exp167 "
        "pred_d -15.93, Exp186 RMSE 50.36 versus persist 72.02). Per Gorishniy et al. 2021 "
        "that is feature-as-token. Because heating_night already DISCARD, this is unused "
        "pressure-change token not another heating dummy. KEEP if 1h composite beats "
        "-21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.15 to 21.20 versus Exp167 20.072 and Exp186 20.483, val "
        "21.70 to 22.40, and composite -22.40 to -21.70. Val may move from Exp186 22.066 "
        "toward 21.85 to 22.00 if the extra token steps rising-P collapse. A val RMSE "
        "above 22.40 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
