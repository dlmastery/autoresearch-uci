"""Exp176 — FT-Transformer n_layers=1 on Exp167 features (FT cycle 2/50)."""
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
    "--set", "n_layers=1",
    "--set", "dropout=0.1",
    "--set", "lr=0.0001",
    "--set", "epochs=100",
    "--set", "patience=15",
    "--set", "batch_size=32",
    "--set", "weight_decay=1e-5",
    "--set", "warmup=10",
    "--description", "FT-Transformer n_layers=1 on Exp167 features (FT cycle 2/50)",
    "--diagnosis",
    (
        "1h champion is Exp167 residual MLP: test 20.072, val 21.972 so val is the "
        "bottleneck. January RMSE 31.22 versus persist-1 33.58 (20.97 percent of SSE, "
        "pred_d -3.88 versus need -0.12). JJA 13.87 versus persist 14.83. Hour 20 32.68 "
        "versus persist 33.24 (11.10 percent of SSE). Onset n=83 RMSE 110.28 losing to "
        "persist 107.80 (31.51 percent of SSE; need +87.40 pred_d -0.60). Exp175 three-layer "
        "FT DISCARD: val 22.698, test 23.130 lost persist 22.316; typical 7.14 to 10.22; "
        "dirty-stable 11.99 to 24.29. New: heating dirty-stable persist>=150 |need|<=10 "
        "n=269 RMSE 15.66 versus persist 6.19 (2.06 percent of SSE; need -0.09 pred_d "
        "-4.08) so the residual MLP already over-cleans stagnant heating hours, and three "
        "PreNorm blocks buried lag-1 further. Unused change is n_layers 3 to 1, not another "
        "d_model shrink."
    ),
    "--citations",
    (
        "Yun, Chulhee; Bhojanapalli, Srinadh; Rawat, Ankit Singh; Reddi, Sashank J. and "
        "Kumar, Sanjiv 2020 ICLR 'Are Transformers universal approximators of "
        "sequence-to-sequence functions?' (arXiv:1912.10077) — a single self-attention "
        "block with enough width is already a universal token mixer, so extra stacked "
        "encoder layers are not required for feature-wise mixing. Relevance: Exp175's "
        "three PreNorm blocks buried lag-1 on heating dirty-stable hours (dirty-stable "
        "11.99 to 24.29, typical 7.14 to 10.22 versus persist 5.08); setting n_layers=1 "
        "keeps FT tokenization with one mixer, not another d_model 32/96 retry."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting n_layers=1 on the unused FT-Transformer paper recipe "
        "(d_model 64, n_heads 4, dropout 0.1, AdamW lr 1e-4, batch 32, weight_decay 1e-5, "
        "epochs 100, patience 15, warmup 10) with Exp167 features will cut 2013 val RMSE "
        "because the mechanism is one attention block so lag-1 cannot be overwritten by "
        "three stacked PreNorm residuals on heating dirty-stable hours (need -0.09, Exp167 "
        "pred_d -4.08, Exp175 worse). Per Yun et al. 2020 one self-attention layer already "
        "mixes tokens. Because paper-default depth just lost persist, this is unused "
        "shallower FT, not another d_model or MLP wrap. KEEP if 1h composite beats -21.972."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.2 to 23.4 versus Exp167 20.072 and Exp175 23.130, val "
        "21.80 to 24.20, and composite -24.20 to -21.80. Typical may move from Exp175 10.22 "
        "toward 7.4 to 9.6 if one layer restores lag-1. A val RMSE above 23.80 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
