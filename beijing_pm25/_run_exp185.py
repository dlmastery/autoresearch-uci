"""Exp185 — FT-Transformer Pre-LN warmup=20 on Exp167 features (FT cycle 11/50)."""
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
    "--set", "warmup=20",
    "--set", "norm_first=true",
    "--description", "FT-Transformer Pre-LN warmup=20 on Exp167 features (FT cycle 11/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE). "
        "JJA 13.87 versus persist 14.83. Hour 20 32.68 versus persist 33.24 (11.10 percent "
        "of SSE). Onset n=83 RMSE 110.28 losing to persist 107.80 (31.51 percent of SSE; "
        "need +87.40 pred_d -0.60). Exp178 Pre-LN warmup 10 val 22.140 typical 7.96 versus "
        "champ 7.14. Exp184 warmup=0 DISCARD global bias -3.78. New: cbwd_cv persist>=100 "
        "|need|<=10 n=392 RMSE 9.26 versus persist 5.88 (1.05 percent of SSE; need +0.72 "
        "pred_d +2.30) so calm-wind dirty-stable over-moves, and Exp178 is worse at 13.52 "
        "with pred_d +2.74. Unused change is warmup 10 to 20 on Pre-LN, not another zero."
    ),
    "--citations",
    (
        "Vaswani, Ashish; Shazeer, Noam; Parmar, Niki; Uszkoreit, Jakob; Jones, Llion; "
        "Gomez, Aidan N.; Kaiser, Lukasz and Polosukhin, Illia 2017 NeurIPS 'Attention "
        "Is All You Need' (arXiv:1706.03762) — they set lrate proportional to "
        "min(step^{-0.5}, step * warmup_steps^{-1.5}) with warmup_steps=4000 so the first "
        "updates stay small and embeddings do not explode. Relevance: Exp184 warmup=0 "
        "over-cleaned with global bias -3.78 and hour2-4 pred_d -7.81, while calm-wind "
        "dirty-stable already over-moves pred_d +2.30 versus need +0.72 at 9.26 versus "
        "persist 5.88 (Exp178 13.52); doubling warmup to 20 epochs is unused longer ramp, "
        "not another warmup=0."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting warmup=20 on the unused Exp178 Pre-LN FT recipe "
        "(d_model 64, n_heads 4, n_layers 3, dropout 0.1, norm_first true, AdamW lr 1e-4, "
        "batch 32, weight_decay 1e-5, epochs 100, patience 15) with Exp167 features will "
        "cut 2013 val RMSE because the mechanism is a longer linear ramp so calm-wind "
        "dirty-stable hours cannot over-move lag-1 (need +0.72, Exp167 pred_d +2.30, "
        "Exp178 RMSE 13.52 versus champ 9.26). Per Vaswani et al. 2017 that is warmup "
        "protecting early steps. Because warmup=0 already closed, this is unused longer "
        "ramp not another zero. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.30 to 21.50 versus Exp167 20.072 and Exp178 20.674, val "
        "21.70 to 22.90, and composite -22.90 to -21.70. Val may move from Exp178 22.140 "
        "toward 21.85 to 22.10 if longer warmup damps calm-wind over-move. A val RMSE "
        "above 22.90 is a miss. Ranges are ug/m3 on the frozen timestamps."
    ),
])
