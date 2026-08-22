"""Exp187 — FT-Transformer Pre-LN add heating_night on Exp186 recipe (FT cycle 13/50)."""
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
    "--add-feature", "heating_night",
    "--description", "FT-Transformer Pre-LN add heating_night on Exp186 recipe (FT cycle 13/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp186 Pre-LN +cbwd_prev_NW val 22.066 typical 7.51 "
        "versus champ 7.14. New: heating_night persist>=150 |need|<=10 n=166 RMSE 17.25 "
        "versus persist 6.09 (1.54 percent of SSE; need +0.23 pred_d -4.23) so stagnant "
        "heating nights over-clean, and Exp186 is worse at 22.35 with pred_d -5.23. Unused "
        "change is add heating_night, not another wind dummy."
    ),
    "--citations",
    (
        "Zhang, Shuyi; Guo, Bin; Dong, Anlan; He, Jing; Xu, Ziping and Chen, Song Xi "
        "2017 JRSS Series A 'Cautionary tales on air-quality improvement in Beijing' — "
        "they show Beijing district heating from mid-November concentrates PM2.5 at night "
        "when the mixed layer collapses, a regime is_heating times hour_sin cannot mark "
        "as one token. Relevance: Exp167 heating_night persist>=150 |need|<=10 over-cleans "
        "pred_d -4.23 versus need +0.23 at 17.25 versus persist 6.09 (Exp186 22.35); adding "
        "heating_night is one unused interaction token on Exp186, not another cbwd dummy."
    ),
    "--hypothesis",
    (
        "We hypothesize that adding heating_night on the unused Exp186 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15, warmup 10, cbwd_prev_NW) "
        "with Exp167 features will cut 2013 val RMSE because the mechanism is one extra "
        "token so stagnant heating nights cannot over-clean lag-1 (need +0.23, Exp167 "
        "pred_d -4.23, Exp186 RMSE 22.35 versus champ 17.25). Per Zhang et al. 2017 that "
        "is nocturnal heating-season PM2.5. Because cbwd_prev_NW already helped wind "
        "regime, this is unused heating-night token not another wind dummy. KEEP if 1h "
        "composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.20 to 21.30 versus Exp167 20.072 and Exp186 20.483, val "
        "21.70 to 22.50, and composite -22.50 to -21.70. Val may move from Exp186 22.066 "
        "toward 21.85 to 22.00 if the extra token holds heating-night persist. A val RMSE "
        "above 22.50 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
