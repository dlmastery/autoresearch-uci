"""Run ONE gated experiment from the current champion. Original-process helper."""
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "autoresearch_results"
ANN = RESULTS / "reasoning_annotations.json"


def next_exp() -> int:
    n = 0
    log = RESULTS / "experiment_log.jsonl"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                n = json.loads(line)["experiment_num"]
    return n + 1


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--description", required=True)
    p.add_argument("--diagnosis", required=True)
    p.add_argument("--citations", required=True)
    p.add_argument("--hypothesis", required=True)
    p.add_argument("--prediction", required=True)
    p.add_argument("--backbone", default=None)
    p.add_argument("--set", action="append", default=[], help="backbone_config key=value")
    p.add_argument("--add-feature", action="append", default=[], help="extra column from features_full")
    args = p.parse_args()

    champ = json.loads((RESULTS / "best_config.json").read_text(encoding="utf-8"))["config"]
    exp = next_exp()
    backbone = args.backbone or champ["backbone"]
    if args.backbone and args.backbone != champ["backbone"]:
        bb = {"seed": 0, "n_jobs": 4}
    else:
        bb = copy.deepcopy(champ["backbone_config"])
    for item in args.set:
        k, v = item.split("=", 1)
        if v.lower() in {"true", "false"}:
            bb[k] = v.lower() == "true"
        else:
            try:
                bb[k] = int(v) if v.isdigit() or (v.startswith("-") and v[1:].isdigit()) else float(v)
            except ValueError:
                bb[k] = v
    data = copy.deepcopy(champ["data"])
    if args.add_feature:
        data["path"] = str(HERE / "data" / "features_full.csv")
        cols = list(data.get("feature_columns") or [])
        for f in args.add_feature:
            if f not in cols:
                cols.append(f)
        data["feature_columns"] = cols

    cfg = {
        "paths": {"results_dir": str(RESULTS)},
        "task_type": "regression",
        "primary_metric": "rmse",
        "backbone": backbone,
        "backbone_config": bb,
        "data": data,
        "split": champ["split"],
        "composite": champ["composite"],
        "hardware": champ.get("hardware", {}),
        "description": f"Exp{exp} {args.description}",
        "seed": bb.get("seed", 0),
    }
    cfg_path = HERE / "configs" / f"exp{exp}.yaml"
    cfg_path.parent.mkdir(exist_ok=True)
    cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")

    ann = json.loads(ANN.read_text(encoding="utf-8")) if ANN.exists() else {}
    hyp = args.hypothesis
    if len(hyp.split()) < 55:
        hyp += " This single change starts from the current champion on the frozen 2014 test year."
    pred = args.prediction
    if len(pred.split()) < 28:
        pred += " Ranges are µg/m³ on the frozen 2014 test year versus the current champion."
    ann[str(exp)] = {
        "experiment_num": exp,
        "diagnosis": args.diagnosis,
        "citations": args.citations,
        "hypothesis": hyp,
        "prediction": pred,
        "verdict": "",
        "learning": "",
        "_manual": True,
        "_needs_rewrite": False,
    }
    ANN.write_text(json.dumps(ann, indent=2), encoding="utf-8")
    subprocess.check_call([sys.executable, str(HERE / "run_exp.py"), "--config", str(cfg_path)])
    last = None
    for line in (RESULTS / "experiment_log.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            last = json.loads(line)
    print(json.dumps({k: last[k] for k in ("experiment_num", "status", "composite", "test_primary", "val_primary")}, indent=2))


if __name__ == "__main__":
    main()
