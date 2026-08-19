"""Exp88 — CatBoost Plain l2_leaf_reg 3 to 10 on Exp78 1h."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
subprocess.check_call([
    sys.executable, str(HERE / "live_exp.py"),
    "--description", "CatBoost Plain l2_leaf_reg=10 on Exp30 features (CatBoost cycle 14/50)",
    "--backbone", "catboost",
    "--set", "iterations=2000",
    "--set", "depth=6",
    "--set", "learning_rate=0.03",
    "--set", "l2_leaf_reg=10",
    "--set", "early_stopping_rounds=100",
    "--set", "boosting_type=Plain",
    "--diagnosis",
    (
        "1h champion remains Exp30: test 20.945, val 22.397 so val is the 1h bottleneck, "
        "January 33.07 versus JJA 14.03, hour 20 31.93, onset n=83 RMSE 110.05 losing to "
        "persist-1 107.80. This fire recomputes Exp87 Lossguide residuals, not last step's "
        "pre-run hour-10 blob. Exp87 val 22.476 flat versus Exp78 22.472, test 21.188 worse. "
        "New: hour-10 persist>=150 RMSE 52.60 worse than Exp78 48.03 and Exp30 38.25. "
        "Hour-10 collapse pred +9.4 versus Exp78 +2.2 versus need -113.7. Extra leaf-wise "
        "capacity hurt the bomb. Exp78 remains 0.075 from KEEP. l2_leaf_reg is still 3. "
        "Lossguide, Ordered, lr 0.01, and depth 4 stay closed."
    ),
    "--citations",
    (
        "Prokhorenkova, Liudmila; Gusev, Gleb; Vorobev, Aleksandr; Dorogush, Anna Veronika "
        "and Gulin, Andrey 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical "
        "Features' (arXiv:1706.09516) — l2_leaf_reg shrinks oblivious-leaf values and is "
        "the default-3 knob they use when extra capacity overfits a rare shard. Relevance: "
        "Exp87 Lossguide made hour-10 persist>=150 RMSE 48.03 to 52.60 on the frozen 2014 "
        "nowcast, so raising l2_leaf_reg to 10 on Exp78 Symmetric trees is one change from "
        "Exp78, not another grow_policy."
    ),
    "--hypothesis",
    (
        "We hypothesize that setting l2_leaf_reg from 3 to 10 on the Exp78 CatBoost Plain "
        "recipe (depth 6, learning_rate 0.03, boosting_type Plain, iterations 2000) with "
        "the Exp30 inversion_spread plus pm25_delta1 plus 24-lag features unchanged will "
        "cut 2013 val RMSE because the mechanism is stronger leaf L2 so 2010-2012 hour-10 "
        "persist shards cannot own large wrong-sign values. Per Prokhorenkova et al. 2018 "
        "that is l2_leaf_reg. Because Lossguide just made hour-10 worse, this is less "
        "capacity not more. KEEP if 1h composite beats -22.397. This single change starts "
        "from the current champion on the frozen 2014 test year."
    ),
    "--prediction",
    (
        "I predict 1h test RMSE 20.7 to 22.2 versus Exp30 20.945, val 22.05 to 22.65, and "
        "composite -22.75 to -22.05. Hour-10 persist>=150 RMSE may move from 48.03 toward "
        "40 to 47 versus Exp30 38.25. A val RMSE above 22.55 is a miss. Ranges are ug/m3 "
        "on the frozen 2014 timestamps."
    ),
])
