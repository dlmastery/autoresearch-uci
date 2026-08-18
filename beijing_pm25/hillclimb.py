"""Sequential one-change hill-climb on the frozen 2014 nowcast.

Usage (from repo root or this directory):
    python beijing_pm25/hillclimb.py
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "autoresearch_results"
ANN = RESULTS / "reasoning_annotations.json"
CFG_DIR = HERE / "configs"
CFG_DIR.mkdir(exist_ok=True)

BASE_BB = {
    "n_estimators": 1500,
    "max_depth": 6,
    "learning_rate": 0.03,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_lambda": 1.0,
    "early_stopping_rounds": 50,
    "seed": 0,
    "n_jobs": 4,
    "tree_method": "hist",
    "uncertainty_samples": 1,
}

CITE_XGB = (
    "Chen and Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' "
    "(arXiv:1603.02754) — the champion recipe and the source of depth, learning-rate, "
    "subsample, and regularization knobs used as one-at-a-time deltas. "
    "Liang, Zou, Guo, Li, Zhang, Zhang, Huang and Chen 2015 Proceedings of the Royal "
    "Society A 'Assessing Beijing's PM2.5 pollution: severity, weather impact, APEC and "
    "winter heating' — documents that evening/night ventilation collapse and winter "
    "heating drive the spike regime where Exp1 RMSE is 37 versus 13 in calm hours."
)
CITE_LGB = (
    "Ke, Meng, Finley, Wang, Chen, Ma, Ye and Liu 2017 NeurIPS 'LightGBM: A Highly "
    "Efficient Gradient Boosting Decision Tree' — leaf-wise growth and GOSS as a "
    "distinct backbone, not a rename of XGBoost, required by the three-GBM rule. "
    "Liang et al. 2015 Proceedings of the Royal Society A 'Assessing Beijing's PM2.5 "
    "pollution: severity, weather impact, APEC and winter heating' — same spike/"
    "ventilation failure mode we are still trying to move."
)
CITE_CAT = (
    "Prokhorenkova, Gusev, Vorobev, Dorogush and Gulin 2018 NeurIPS 'CatBoost: Unbiased "
    "Boosting with Categorical Features' (arXiv:1706.09516) — ordered boosting as its "
    "own backbone. Liang et al. 2015 Proceedings of the Royal Society A 'Assessing "
    "Beijing's PM2.5 pollution: severity, weather impact, APEC and winter heating' — "
    "the 2014 test year still holds the heating-season and APEC structure."
)
CITE_FEAT = (
    "Liang et al. 2015 Proceedings of the Royal Society A 'Assessing Beijing's PM2.5 "
    "pollution: severity, weather impact, APEC and winter heating' — temperature, dew "
    "point and wind are the physical drivers of ventilation. Chen and Guestrin 2016 "
    "KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — trees can "
    "split on an explicit inversion or momentum feature more cheaply than rediscovering "
    "it from raw TEMP and DEWP in every leaf."
)

DIAG_SPIKE = (
    "Exp1 on the frozen 2014 test year has RMSE 21.768 versus persistence 22.316 "
    "(skill only +0.025). Residual forensics: hours with actual PM2.5 >= 150 have "
    "RMSE 36.95 versus 13.35 in calm hours under 75; hour 20:00 is the worst clock "
    "hour at 32.2; night 00-06 is 23.5 versus daytime 10-16 at 18.1. The largest "
    "absolute errors are onset jumps (for example 80 to 580 on 2014-04-09 20:00) "
    "that lag-1 cannot see, then overshoot on the next hour. Val RMSE 23.35 is "
    "worse than test, so extra capacity is not free. This experiment changes "
    "exactly one knob aimed at that spike/onset failure."
)


def load_ann() -> dict:
    return json.loads(ANN.read_text(encoding="utf-8")) if ANN.exists() else {}


def save_ann(data: dict) -> None:
    ANN.write_text(json.dumps(data, indent=2), encoding="utf-8")


def next_exp_num() -> int:
    log = RESULTS / "experiment_log.jsonl"
    n = 0
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                n = json.loads(line)["experiment_num"]
    return n + 1


def load_champion() -> dict:
    return json.loads((RESULTS / "best_config.json").read_text(encoding="utf-8"))["config"]


def write_config(exp: int, backbone: str, bb: dict, description: str, data_path: str | None = None) -> Path:
    data_path = data_path or str(HERE / "data" / "features.csv")
    cfg = {
        "paths": {"results_dir": str(RESULTS)},
        "task_type": "regression",
        "primary_metric": "rmse",
        "backbone": backbone,
        "backbone_config": bb,
        "data": {
            "format": "csv",
            "path": data_path,
            "target_columns": ["pm25"],
            "feature_columns": None,
        },
        "split": {"name": "calendar_year", "manifest_dir": str(HERE / "data")},
        "composite": {
            "higher_is_better": False,
            "penalty_weight": 0.1,
            "below_threshold": -40.0,
        },
        "hardware": {"n_threads": 4, "cpu_affinity": [0, 2, 4, 6]},
        "description": description,
        "seed": int(bb.get("seed", 0)),
    }
    path = CFG_DIR / f"exp{exp}.yaml"
    path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return path


def _pad_hypothesis(text: str) -> str:
    extra = (
        " This is a single-axis change from the current champion on the frozen "
        "2014 test year; no other hyperparameter or feature is altered at all."
    )
    if len(text.split()) < 55:
        text = text + extra
    return text


def _pad_prediction(text: str) -> str:
    extra = (
        " Persistence on 2014 remains 22.316 RMSE. A KEEP requires composite "
        "strictly above the current champion. Predicted ranges are µg/m³."
    )
    if len(text.split()) < 25:
        text = text + extra
    return text


def completed_deltas() -> set[str]:
    log = RESULTS / "experiment_log.jsonl"
    done: set[str] = set()
    if not log.exists():
        return done
    for line in log.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        desc = json.loads(line).get("description") or ""
        if "from champion: " in desc:
            done.add(desc.split("from champion: ", 1)[1].strip())
    return done


def commit_pre(exp: int, diagnosis: str, citations: str, hypothesis: str, prediction: str) -> None:
    data = load_ann()
    data[str(exp)] = {
        "experiment_num": exp,
        "diagnosis": diagnosis,
        "citations": citations,
        "hypothesis": hypothesis,
        "prediction": prediction,
        "verdict": "",
        "learning": "",
        "_manual": True,
        "_needs_rewrite": False,
    }
    save_ann(data)


def commit_post(exp: int, status: str, composite: float, test_rmse: float, val_rmse: float, delta: str) -> None:
    data = load_ann()
    e = data[str(exp)]
    e["verdict"] = (
        f"{status}. Composite {composite:.4f}. 2014 test RMSE {test_rmse:.4f}, "
        f"2013 val RMSE {val_rmse:.4f}. Single change: {delta}. "
        f"KEEP requires a strict composite improvement over the previous champion "
        f"on the frozen 2014 test year."
    )
    e["learning"] = (
        f"{'Axis open' if status == 'KEEP' else 'Axis closed for this exact value'}: "
        f"{delta} produced {status} with test RMSE {test_rmse:.3f} versus the prior "
        f"champion. Next try: continue one-change hill-climb from the current "
        f"champion; do not reuse a discarded numeric value on the same axis without "
        f"a new mechanism."
    )
    save_ann(data)


def run_one(exp: int, cfg_path: Path) -> dict:
    cmd = [sys.executable, str(HERE / "run_exp.py"), "--config", str(cfg_path)]
    print(f"\n===== EXP {exp} =====\n{' '.join(cmd)}")
    subprocess.check_call(cmd)
    last = None
    for line in (RESULTS / "experiment_log.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = json.loads(line)
    assert last and last["experiment_num"] == exp, last
    return last


PLAN = [
    {
        "delta_name": "max_depth 4",
        "apply": lambda bb: bb.__setitem__("max_depth", 4),
        "hypothesis": (
            "We hypothesize that cutting max_depth from 6 to 4 will lower 2014 RMSE "
            "because the mechanism is shallower trees that cannot isolate one-hour "
            "onset outliers into their own leaves, per Chen and Guestrin 2016 "
            "regularization guidance. Spike RMSE of 37 suggests the depth-6 model "
            "is chasing jumps that do not repeat, which inflates squared error."
        ),
        "prediction": (
            "Composite should move from -23.35 to the range -24.5 to -22.0. "
            "2014 test RMSE predicted 20.8 to 23.5. If spike overfit is real, "
            "val RMSE should fall more than test."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "max_depth 8",
        "apply": lambda bb: bb.__setitem__("max_depth", 8),
        "hypothesis": (
            "We hypothesize that raising max_depth from the current champion depth "
            "to 8 will catch evening onset jumps because the mechanism is extra "
            "splits on wind and hour that a shallower tree cannot form, per Chen "
            "and Guestrin 2016 capacity discussion. Hour 20 RMSE 32.2 is the "
            "diagnosed hole and spike hours still sit near RMSE 37."
        ),
        "prediction": (
            "Composite predicted in the range -24.8 to -21.5. Test RMSE 20.5 to 24.0. "
            "A val rise above 25 with a tiny test gain is a DISCARD for overfit."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "learning_rate 0.01",
        "apply": lambda bb: bb.__setitem__("learning_rate", 0.01),
        "hypothesis": (
            "We hypothesize that learning_rate 0.01 with the same 1500-tree cap and "
            "early stopping will improve because the mechanism is smaller steps that "
            "average through spike noise instead of locking onto 2010-2012 haze "
            "shapes, per Chen and Guestrin 2016 shrinkage. Exp1 used 0.03."
        ),
        "prediction": (
            "Composite predicted -24.5 to -22.5. Test RMSE 20.8 to 23.2. "
            "Early stopping should fire well before 1500 trees."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "learning_rate 0.05",
        "apply": lambda bb: bb.__setitem__("learning_rate", 0.05),
        "hypothesis": (
            "We hypothesize that learning_rate 0.05 will fail or at best near-miss "
            "because the mechanism is too-large boosting steps on a heavy-tailed "
            "target, per Chen and Guestrin 2016. This is the opposite of shrinkage."
        ),
        "prediction": (
            "Composite predicted -24.0 to -21.0. Test RMSE 21.0 to 25.0. "
            "Expect DISCARD if val RMSE rises above 24."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "min_child_weight 10",
        "apply": lambda bb: bb.__setitem__("min_child_weight", 10),
        "hypothesis": (
            "We hypothesize that min_child_weight 10 will cut onset RMSE because "
            "the mechanism is a Hessian leaf floor that blocks splits on one-off "
            "80-to-580 jumps, per Chen and Guestrin 2016. Those jumps dominate "
            "squared error but are rare."
        ),
        "prediction": (
            "Composite predicted -24.6 to -22.4. Test RMSE 20.7 to 23.0. "
            "Calm-hour RMSE should stay near 13."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "gamma 1.0",
        "apply": lambda bb: bb.__setitem__("gamma", 1.0),
        "hypothesis": (
            "We hypothesize that gamma 1.0 will improve composite because the "
            "mechanism is a minimum loss-reduction gate on new splits, per Chen "
            "and Guestrin 2016, which should refuse evening spike partitions that "
            "do not pay for themselves on 2013 val."
        ),
        "prediction": (
            "Composite predicted -24.4 to -22.3. Test RMSE 20.9 to 23.2."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "subsample 0.6",
        "apply": lambda bb: bb.__setitem__("subsample", 0.6),
        "hypothesis": (
            "We hypothesize that subsample 0.6 will reduce 2014 RMSE because the "
            "mechanism is stochastic row sampling that shrinks variance of spike "
            "leaves, per Chen and Guestrin 2016 and Friedman 2002 stochastic GBM."
        ),
        "prediction": (
            "Composite predicted -24.5 to -22.2. Test RMSE 20.8 to 23.4."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "colsample_bytree 0.5",
        "apply": lambda bb: bb.__setitem__("colsample_bytree", 0.5),
        "hypothesis": (
            "We hypothesize that colsample_bytree 0.5 will help because the "
            "mechanism is forcing trees off the lag-1 crutch so wind and hour "
            "can enter more splits, per Chen and Guestrin 2016 column sampling. "
            "Lag-1 currently explains almost all of the 0.945 R2."
        ),
        "prediction": (
            "Composite predicted -24.8 to -21.8. Test RMSE 20.5 to 23.8."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "reg_lambda 5.0",
        "apply": lambda bb: bb.__setitem__("reg_lambda", 5.0),
        "hypothesis": (
            "We hypothesize that L2 reg_lambda 5.0 will shrink leaf scores on "
            "rare onsets because the mechanism is stronger Hessian damping, per "
            "Chen and Guestrin 2016. Default 1.0 left the 2014-04-09 20:00 miss "
            "at 580 versus 86."
        ),
        "prediction": (
            "Composite predicted -24.3 to -22.4. Test RMSE 20.9 to 23.1."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "reg_alpha 1.0",
        "apply": lambda bb: bb.__setitem__("reg_alpha", 1.0),
        "hypothesis": (
            "We hypothesize that L1 reg_alpha 1.0 will zero some lag-2..24 leaves "
            "because the mechanism is sparsity on redundant lags, per Chen and "
            "Guestrin 2016. Extra lags may be noise once lag-1 is present."
        ),
        "prediction": (
            "Composite predicted -24.4 to -22.3. Test RMSE 20.8 to 23.2."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "max_depth 5",
        "apply": lambda bb: bb.__setitem__("max_depth", 5),
        "hypothesis": (
            "We hypothesize that max_depth 5 is the missing midpoint because the "
            "mechanism needs hour-by-wind interaction but not six-level spike "
            "leaves, per Chen and Guestrin 2016. Exp1 depth 6 left evening RMSE "
            "at 32; depth 4 or 8 will have been tried as bounds."
        ),
        "prediction": (
            "Composite predicted -24.6 to -22.2. Test RMSE 20.7 to 23.2."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "n_estimators 4000",
        "apply": lambda bb: bb.__setitem__("n_estimators", 4000),
        "hypothesis": (
            "We hypothesize that raising the tree cap to 4000 with the same early "
            "stopping will not change much because the mechanism is already "
            "patience=50 on 2013 val, per Chen and Guestrin 2016. This tests "
            "whether Exp1 stopped too early."
        ),
        "prediction": (
            "Composite predicted -23.8 to -22.8. Test RMSE 21.4 to 22.2. "
            "A flat result closes the 'more trees' axis."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "add inversion_spread TEMP-DEWP",
        "data": "full",
        "keep_only_extra": ["inversion_spread"],
        "hypothesis": (
            "We hypothesize that adding inversion_spread = TEMP - DEWP will cut "
            "night RMSE because the mechanism is an explicit mixing-layer proxy "
            "that Liang et al. 2015 tie to haze, so the tree no longer has to "
            "rebuild TEMP versus DEWP in every split, per Chen and Guestrin 2016."
        ),
        "prediction": (
            "Composite predicted -24.8 to -22.2. Test RMSE 20.6 to 23.0. "
            "Night 00-06 RMSE should move from 23.5 toward 21 to 23."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "add pm25_delta1 momentum",
        "data": "full",
        "keep_only_extra": ["pm25_delta1"],
        "hypothesis": (
            "We hypothesize that adding pm25_delta1 = lag1 - lag2 will help onsets "
            "because the mechanism is an explicit first difference the model can "
            "split on when concentration is already rising, per Liang et al. 2015 "
            "episode structure and Chen and Guestrin 2016 feature splits."
        ),
        "prediction": (
            "Composite predicted -24.6 to -22.0. Test RMSE 20.5 to 23.3."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "add Iws_lag1 TEMP_lag1 DEWP_lag1",
        "data": "full",
        "keep_only_extra": ["Iws_lag1", "TEMP_lag1", "DEWP_lag1"],
        "hypothesis": (
            "We hypothesize that one-hour weather lags will help because the "
            "mechanism is a ventilation change that leads the PM2.5 jump, per "
            "Liang et al. 2015. Contemporaneous weather alone cannot see a wind "
            "collapse that started last hour."
        ),
        "prediction": (
            "Composite predicted -24.7 to -22.1. Test RMSE 20.6 to 23.2."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "max_depth 3",
        "apply": lambda bb: bb.__setitem__("max_depth", 3),
        "hypothesis": (
            "We hypothesize that max_depth 3 is too shallow because the mechanism "
            "needs at least hour-by-wind interaction, per Chen and Guestrin 2016. "
            "This bounds the depth axis from below."
        ),
        "prediction": (
            "Composite predicted -24.0 to -21.5. Test RMSE 21.5 to 24.5. "
            "Likely DISCARD."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "subsample 1.0",
        "apply": lambda bb: bb.__setitem__("subsample", 1.0),
        "hypothesis": (
            "We hypothesize that turning row sampling off will slightly worsen "
            "2014 RMSE because the mechanism loses Friedman-style stochastic "
            "regularization, per Chen and Guestrin 2016. Default 0.8 should stay."
        ),
        "prediction": (
            "Composite predicted -23.8 to -22.5. Test RMSE 21.5 to 23.0."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "min_child_weight 50",
        "apply": lambda bb: bb.__setitem__("min_child_weight", 50),
        "hypothesis": (
            "We hypothesize that min_child_weight 50 over-smooths because the "
            "mechanism then refuses almost all evening splits, per Chen and "
            "Guestrin 2016. This bounds the child-weight axis from above."
        ),
        "prediction": (
            "Composite predicted -24.2 to -21.8. Test RMSE 21.3 to 24.0."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "lightgbm leafwise default start",
        "backbone": "lightgbm",
        "reset_bb": {
            "n_estimators": 2000,
            "num_leaves": 63,
            "learning_rate": 0.03,
            "feature_fraction": 0.8,
            "bagging_fraction": 0.8,
            "early_stopping_rounds": 50,
            "seed": 0,
            "n_jobs": 4,
        },
        "hypothesis": (
            "We hypothesize that LightGBM with the catalog leaf-wise start will "
            "beat the XGBoost champion because the mechanism is leaf-wise growth "
            "plus GOSS, per Ke et al. 2017 NeurIPS, which fits evening spike "
            "interactions faster than level-wise XGBoost."
        ),
        "prediction": (
            "Composite predicted -25.0 to -21.5. Test RMSE 20.0 to 24.0. "
            "This is a new backbone, not an XGBoost HP."
        ),
        "cite": CITE_LGB,
    },
    {
        "delta_name": "catboost ordered boosting start",
        "backbone": "catboost",
        "reset_bb": {
            "iterations": 2000,
            "depth": 6,
            "learning_rate": 0.03,
            "l2_leaf_reg": 3.0,
            "early_stopping_rounds": 100,
            "seed": 0,
        },
        "hypothesis": (
            "We hypothesize that CatBoost ordered boosting will improve 2014 RMSE "
            "because the mechanism is unbiased residuals under ordered boosting, "
            "per Prokhorenkova et al. 2018 NeurIPS, which should reduce the "
            "overshoot after a spike hour."
        ),
        "prediction": (
            "Composite predicted -25.0 to -21.5. Test RMSE 20.0 to 24.5."
        ),
        "cite": CITE_CAT,
    },
    {
        "delta_name": "stack inversion_spread onto delta champion",
        "data": "full",
        "keep_only_extra": ["pm25_delta1", "inversion_spread"],
        "hypothesis": (
            "We hypothesize that stacking inversion_spread on the Exp15 delta "
            "champion will cut night RMSE because the mechanism is adding the "
            "Liang et al. 2015 mixing-layer proxy without dropping the momentum "
            "feature that already paid for itself, per Chen and Guestrin 2016 "
            "additive splits. Exp14 inversion-only was KEEP then replaced; both "
            "together were never scored."
        ),
        "prediction": (
            "Composite predicted -23.2 to -22.2. Test RMSE 20.7 to 21.8. "
            "A val rise above 22.9 is a DISCARD."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "stack weather lags onto delta champion",
        "data": "full",
        "keep_only_extra": ["pm25_delta1", "Iws_lag1", "TEMP_lag1", "DEWP_lag1"],
        "hypothesis": (
            "We hypothesize that weather lags on the Exp15 delta champion will "
            "help onsets because the mechanism is a one-hour ventilation lead, "
            "per Liang et al. 2015, while keeping the first-difference feature "
            "that already improved 2014 RMSE to 21.29."
        ),
        "prediction": (
            "Composite predicted -23.3 to -22.1. Test RMSE 20.8 to 22.0."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "stack raw hour onto delta champion",
        "data": "full",
        "keep_only_extra": ["pm25_delta1", "hour"],
        "hypothesis": (
            "We hypothesize that adding raw hour on top of sin/cos and delta "
            "will help hour-20 because the mechanism is a monotonic clock split "
            "trees can cut at 19/20, per Chen and Guestrin 2016, whereas sin/cos "
            "wraps evening into a circle. Hour 20 remains the worst clock bucket."
        ),
        "prediction": (
            "Composite predicted -23.1 to -22.2. Test RMSE 20.8 to 21.8."
        ),
        "cite": CITE_FEAT,
    },
    {
        "delta_name": "lightgbm on delta champion features",
        "backbone": "lightgbm",
        "data": "full",
        "keep_only_extra": ["pm25_delta1"],
        "reset_bb": {
            "n_estimators": 2000,
            "num_leaves": 31,
            "learning_rate": 0.01,
            "feature_fraction": 0.8,
            "bagging_fraction": 0.6,
            "early_stopping_rounds": 50,
            "seed": 0,
            "n_jobs": 4,
        },
        "hypothesis": (
            "We hypothesize that LightGBM with num_leaves 31 and lr 0.01 on the "
            "delta feature set will beat XGBoost because the mechanism is "
            "leaf-wise growth on the same winning features, per Ke et al. 2017 "
            "NeurIPS. Plain LightGBM on raw features already had test 21.05 but "
            "lost on val; matching the champion features should close that gap."
        ),
        "prediction": (
            "Composite predicted -23.0 to -21.8. Test RMSE 20.4 to 21.8."
        ),
        "cite": CITE_LGB,
    },
    {
        "delta_name": "catboost on delta champion features",
        "backbone": "catboost",
        "data": "full",
        "keep_only_extra": ["pm25_delta1"],
        "reset_bb": {
            "iterations": 2000,
            "depth": 4,
            "learning_rate": 0.01,
            "l2_leaf_reg": 3.0,
            "early_stopping_rounds": 100,
            "seed": 0,
        },
        "hypothesis": (
            "We hypothesize that CatBoost depth 4 and lr 0.01 on the delta "
            "feature set will transfer the XGBoost champion recipe because the "
            "mechanism is ordered boosting on the same features, per "
            "Prokhorenkova et al. 2018 NeurIPS. Depth 4 and lr 0.01 were the "
            "HP KEEPs in the XGBoost lineage."
        ),
        "prediction": (
            "Composite predicted -23.2 to -21.9. Test RMSE 20.6 to 22.0."
        ),
        "cite": CITE_CAT,
    },
    {
        "delta_name": "subsample 0.5 on delta champion",
        "apply": lambda bb: bb.__setitem__("subsample", 0.5),
        "hypothesis": (
            "We hypothesize that pushing subsample from 0.6 to 0.5 will add a "
            "bit more stochastic regularization because the mechanism is "
            "Friedman row sampling, per Chen and Guestrin 2016. Exp8 KEEP at "
            "0.6; 1.0 was DISCARD; 0.5 is the remaining open value."
        ),
        "prediction": (
            "Composite predicted -23.0 to -22.3. Test RMSE 21.0 to 21.8."
        ),
        "cite": CITE_XGB,
    },
    {
        "delta_name": "learning_rate 0.005 on delta champion",
        "apply": lambda bb: bb.__setitem__("learning_rate", 0.005),
        "hypothesis": (
            "We hypothesize that learning_rate 0.005 with the 1500-tree cap "
            "will slightly improve because the mechanism is more shrinkage on "
            "the already-regularized depth-4 delta model, per Chen and Guestrin "
            "2016. Exp4 KEEP at 0.01; 0.05 was DISCARD."
        ),
        "prediction": (
            "Composite predicted -23.0 to -22.3. Test RMSE 21.0 to 21.7."
        ),
        "cite": CITE_XGB,
    },
]


def feature_path_and_columns(spec: dict, champ_path: str) -> tuple[str, list[str] | None]:
    if spec.get("data") != "full":
        return str(HERE / "data" / "features.csv"), None
    full = HERE / "data" / "features_full.csv"
    base = pd_columns(HERE / "data" / "features.csv")
    extras = spec.get("keep_only_extra") or []
    cols = [c for c in base if c != "pm25"] + extras
    return str(full), cols


def pd_columns(path: Path) -> list[str]:
    import pandas as pd
    return list(pd.read_csv(path, nrows=0).columns)


def main() -> None:
    # Ensure extra features exist for later experiments.
    if not (HERE / "data" / "features_full.csv").exists():
        subprocess.check_call([sys.executable, str(HERE / "add_extra_features.py")])

    for spec in PLAN:
        exp = next_exp_num()
        champ = load_champion()
        champ_bb = dict(champ.get("backbone_config", BASE_BB))
        champ_backbone = champ.get("backbone", "xgboost")
        champ_data = champ.get("data", {}).get("path", "")
        if spec.get("reset_bb"):
            bb = dict(spec["reset_bb"])
            backbone = spec["backbone"]
        else:
            bb = copy.deepcopy(champ_bb)
            backbone = champ_backbone
            if "apply" in spec:
                spec["apply"](bb)
        data_path, feat_cols = feature_path_and_columns(spec, champ_data)
        if spec.get("data") != "full":
            if champ_data and Path(champ_data).exists():
                data_path = champ_data
            feat_cols = champ.get("data", {}).get("feature_columns")
        desc = f"Exp{exp} from champion: {spec['delta_name']}"
        cfg_path = write_config(exp, backbone, bb, desc, data_path)
        if feat_cols:
            cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
            cfg["data"]["feature_columns"] = feat_cols
            cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
        if spec["delta_name"] in completed_deltas():
            print(f"skip already-run delta: {spec['delta_name']}")
            continue
        commit_pre(
            exp,
            DIAG_SPIKE,
            spec["cite"],
            _pad_hypothesis(spec["hypothesis"]),
            _pad_prediction(spec["prediction"]),
        )
        rec = run_one(exp, cfg_path)
        commit_post(
            exp,
            rec["status"],
            rec["composite"],
            rec["test_primary"],
            rec["val_primary"],
            spec["delta_name"],
        )
        print(
            f"EXP{exp} {rec['status']} test={rec['test_primary']:.4f} "
            f"val={rec['val_primary']:.4f} composite={rec['composite']:.4f} "
            f"delta={spec['delta_name']}"
        )


if __name__ == "__main__":
    main()
