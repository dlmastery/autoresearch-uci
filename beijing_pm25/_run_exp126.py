"""Exp126 — MLP dropout 0.2 to 0.3 on Exp125 recipe (MLP cycle 2/50)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--backbone", "mlp",
    "--set", "dropout=0.3",
    "--description", "MLP dropout=0.3 on Exp125 default recipe (MLP cycle 2/50)",
    "--diagnosis",
    (
        "1h champion remains Exp97 CatBoost: test 20.735, val 22.167 so val is the "
        "bottleneck, January 34.84 versus persist-1 33.58 and JJA 13.84, hour 20 32.48, "
        "onset n=83 RMSE 110.06 losing to persist-1 107.80. Exp125 MLP test 20.648 beat "
        "the champion but val 22.623 so composite failed. New: MLP val-test gap is 1.975 "
        "versus CatBoost 1.432. February 24.09 to 25.56 and April 27.06 to 28.86 ate the "
        "January win (34.84 to 31.02, 5.1 percent of SSE). 2013 February persist RMSE was "
        "38.30 versus 2014 26.01. Do not retry typical-hour over-adjust. Raise dropout."
    ),
    "--citations",
    (
        "Srivastava, Nitish; Hinton, Geoffrey; Krizhevsky, Alex; Sutskever, Ilya and "
        "Salakhutdinov, Ruslan 2014 JMLR 'Dropout: A Simple Way to Prevent Neural Networks "
        "from Overfitting' — independently dropping units with probability p thins co-adapted "
        "hidden features so a net cannot memorize one validation year. Relevance: Exp125 "
        "MLP val-test gap is 1.975 versus CatBoost 1.432 and February/April taxed 2014 while "
        "2013 February persist is 38.30, so raising dropout from 0.2 to 0.3 is one unused "
        "MLP regularizer from the Exp125 recipe, not another CatBoost feature."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting dropout from 0.2 to 0.3 on the Exp125 MLP recipe "
        "(hidden 256-128-64, AdamW lr 3e-4, weight_decay 1e-5, Smooth-L1, Exp97 features) "
        "will cut 2013 val RMSE because the mechanism is stronger unit dropout so 2010-12 "
        "plus 2013-easy-month co-adaptations cannot own every hidden unit that then miss "
        "2013 February-like hardness. Per Srivastava et al. 2014 that is dropout. Because "
        "Exp125 just won 2014 test and lost val, this is unused p=0.3 not another width "
        "or CatBoost HP. KEEP if 1h composite beats -22.167."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.4 to 22.5 versus Exp97 20.735 and Exp125 20.648, val "
        "21.90 to 23.20, and composite -23.20 to -21.90. Val may move from 22.623 toward "
        "22.00 to 22.40 if the 1.975 gap was overfit. A val RMSE above 22.80 is a miss. "
        "Ranges are ug/m3 on the frozen timestamps."
    ),
])
