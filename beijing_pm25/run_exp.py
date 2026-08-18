"""Launch one gated experiment against the cloned generalized_ml_autoresearch runner."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    Path(r"C:\Users\abhir\dlmastery-github\autoresearch"),
    HERE.parents[1] / "autoresearch" if len(HERE.parents) > 1 else HERE,
    HERE.parent.parent / "autoresearch",
    Path.cwd().parent / "autoresearch",
]
FRAMEWORK = next((p for p in CANDIDATES if (p / "generalized_ml_autoresearch").is_dir()), CANDIDATES[0])
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FRAMEWORK))

from calendar_split import register_with_framework  # noqa: E402
from generalized_ml_autoresearch.core.runner import run_experiment, _load_config  # noqa: E402

register_with_framework()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--description", default=None)
    args = p.parse_args()

    cfg = _load_config(args.config)
    if args.description:
        cfg["description"] = args.description

    def _abs(p: str) -> str:
        path = Path(p)
        if path.is_absolute():
            return str(path)
        for root in (HERE, HERE.parent, Path.cwd()):
            cand = (root / path).resolve()
            if cand.exists() or cand.parent.exists():
                return str(cand)
        return str((HERE / path.name).resolve())

    cfg["paths"]["results_dir"] = _abs(cfg["paths"]["results_dir"])
    if cfg["paths"].get("seed_reasoning"):
        cfg["paths"]["seed_reasoning"] = _abs(cfg["paths"]["seed_reasoning"])
    if cfg.get("data", {}).get("path"):
        cfg["data"]["path"] = _abs(cfg["data"]["path"])
    if cfg.get("split", {}).get("manifest_dir"):
        cfg["split"]["manifest_dir"] = _abs(cfg["split"]["manifest_dir"])

    results_dir = Path(cfg["paths"]["results_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / "trade_logs").mkdir(exist_ok=True)

    local_dash = HERE / "dashboard.html"
    if local_dash.exists():
        shutil.copy2(local_dash, results_dir / "dashboard.html")
    else:
        dash_src = FRAMEWORK / "generalized_ml_autoresearch" / "dashboard" / "dashboard.html"
        if dash_src.exists():
            shutil.copy2(dash_src, results_dir / "dashboard.html")

    # Seed / merge pre-run reasoning if a sibling seed file is named in config
    seed_path = cfg.get("paths", {}).get("seed_reasoning")
    if seed_path:
        seed = json.loads(Path(seed_path).read_text(encoding="utf-8"))
        ann = results_dir / "reasoning_annotations.json"
        existing = json.loads(ann.read_text(encoding="utf-8")) if ann.exists() else {}
        existing.update(seed)
        ann.write_text(json.dumps(existing, indent=2), encoding="utf-8")

    record = run_experiment(cfg)
    print("\n--- Summary ---")
    print(f"  Exp {record.experiment_num} ({record.backbone})")
    print(f"  Composite: {record.composite:.4f}  Status: {record.status}")
    print(f"  Test RMSE: {record.test_primary:.4f}")
    print(f"  Val RMSE:  {record.val_primary:.4f}")
    for i, v in enumerate(record.per_fold_test):
        print(f"  Window {i} test RMSE: {v:.4f}")


if __name__ == "__main__":
    main()
