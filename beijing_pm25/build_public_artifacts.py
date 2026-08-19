"""Build champion_diagnostics.json and refresh summary/journal from the live log."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "autoresearch_results"
DATA = HERE / "data"
PERS = 22.316432166770927


def rmse(a, b) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(np.sqrt(np.mean((a - b) ** 2)))


def mae(a, b) -> float:
    return float(np.mean(np.abs(np.asarray(a, dtype=float) - np.asarray(b, dtype=float))))


def f1_spike(y, pred, thr=75.0) -> dict:
    yt = np.asarray(y) > thr
    yp = np.asarray(pred) > thr
    tp = int((yt & yp).sum())
    fp = int((~yt & yp).sum())
    fn = int((yt & ~yp).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"threshold": thr, "precision": prec, "recall": rec, "f1": f1, "tp": tp, "fp": fp, "fn": fn, "n_pos": int(yt.sum())}


def load_log() -> list[dict]:
    rows = []
    for line in (RESULTS / "experiment_log.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def champion_num() -> int:
    best = json.loads((RESULTS / "best_config.json").read_text(encoding="utf-8"))
    return int(best["experiment_num"])


def champion_preds() -> pd.DataFrame:
    n = champion_num()
    pred = pd.read_csv(RESULTS / "trade_logs" / f"exp{n}_predictions.csv")
    times = pd.read_csv(DATA / "times.csv", parse_dates=["time"])
    pred["time"] = times.iloc[pred["index"].to_numpy()].reset_index(drop=True)["time"].to_numpy()
    pred["month"] = pred["time"].dt.month
    pred["hour"] = pred["time"].dt.hour
    pred["delta_actual"] = pred["actual"].diff()
    return pred


def build_diagnostics(pred: pd.DataFrame, log: list[dict]) -> dict:
    n = champion_num()
    champ = next(e for e in log if e["experiment_num"] == n)
    y, p = pred["actual"].to_numpy(), pred["prediction"].to_numpy()
    onset = pred[pred["delta_actual"] >= 50]
    collapse = pred[pred["delta_actual"] <= -50]
    by_month = []
    for m, g in pred.groupby("month"):
        by_month.append({
            "month": int(m), "n": int(len(g)),
            "rmse": rmse(g["actual"], g["prediction"]),
            "mae": mae(g["actual"], g["prediction"]),
            "mean_actual": float(g["actual"].mean()),
            "mean_pred": float(g["prediction"].mean()),
        })
    by_hour = []
    for h, g in pred.groupby("hour"):
        by_hour.append({
            "hour": int(h), "n": int(len(g)),
            "rmse": rmse(g["actual"], g["prediction"]),
            "mae": mae(g["actual"], g["prediction"]),
        })
    keeps = []
    best_c = -1e18
    for e in sorted(log, key=lambda x: x["experiment_num"]):
        if e.get("status") == "KEEP" and e["composite"] > best_c:
            best_c = e["composite"]
            keeps.append(e["experiment_num"])
    bb = defaultdict(int)
    for e in log:
        bb[e.get("backbone", "?")] += 1
    return {
        "experiment_num": n,
        "backbone": champ.get("backbone", "unknown"),
        "composite": champ["composite"],
        "test_rmse": float(rmse(y, p)),
        "val_rmse": champ["val_primary"],
        "mae": float(mae(y, p)),
        "r2": champ.get("secondary_metrics", {}).get("r2"),
        "ic": champ.get("secondary_metrics", {}).get("ic"),
        "n_test": int(len(pred)),
        "skill_vs_persistence": 1.0 - float(rmse(y, p)) / PERS,
        "persistence_rmse": PERS,
        "p50_abs": float(np.median(np.abs(y - p))),
        "p99_abs": float(np.quantile(np.abs(y - p), 0.99)),
        "max_abs": float(np.max(np.abs(y - p))),
        "spike_f1_75": f1_spike(y, p, 75),
        "spike_f1_150": f1_spike(y, p, 150),
        "onset": {
            "rule": "actual[t]-actual[t-1] >= 50",
            "n": int(len(onset)),
            "rmse": rmse(onset["actual"], onset["prediction"]) if len(onset) else None,
            "mae": mae(onset["actual"], onset["prediction"]) if len(onset) else None,
            "mean_actual": float(onset["actual"].mean()) if len(onset) else None,
            "mean_pred": float(onset["prediction"].mean()) if len(onset) else None,
        },
        "collapse": {
            "rule": "actual[t]-actual[t-1] <= -50",
            "n": int(len(collapse)),
            "rmse": rmse(collapse["actual"], collapse["prediction"]) if len(collapse) else None,
            "mean_actual": float(collapse["actual"].mean()) if len(collapse) else None,
            "mean_pred": float(collapse["prediction"].mean()) if len(collapse) else None,
        },
        "by_month": by_month,
        "by_hour": by_hour,
        "worst_month": max(by_month, key=lambda d: d["rmse"]),
        "best_month": min(by_month, key=lambda d: d["rmse"]),
        "worst_hour": max(by_hour, key=lambda d: d["rmse"]),
        "keep_lineage": keeps,
        "n_experiments": len(log),
        "n_keep": sum(1 for e in log if e.get("status") == "KEEP"),
        "n_discard": sum(1 for e in log if e.get("status") == "DISCARD"),
        "backbone_counts": dict(bb),
        "test_hash": "efb0012c1873e5bf2fe56d0cbb3d429c1d879da92273a15cc7bb6532e0ba79fc",
        "composite_fingerprint": champ.get("composite_fingerprint"),
    }


def write_summary(log: list[dict], diag: dict) -> None:
    keeps = [e for e in log if e["experiment_num"] in diag["keep_lineage"]]
    lines = [
        "# Experiment summary — UCI 381 Beijing PM2.5 nowcast",
        "",
        "Composite = `min(−val_RMSE, −test_RMSE) − 0.1 × n_RMSE>40`. KEEP iff composite rises. Test year 2014 is frozen.",
        "",
        f"**Champion:** Exp{diag['experiment_num']} {diag['backbone']} · test RMSE **{diag['test_rmse']:.3f}** · val RMSE **{diag['val_rmse']:.3f}** · skill vs persistence **{diag['skill_vs_persistence']*100:+.1f}%**",
        f"**Campaign:** {diag['n_experiments']} experiments · {diag['n_keep']} KEEP · {diag['n_discard']} DISCARD",
        f"**Mandate gap:** LightGBM {diag['backbone_counts'].get('lightgbm', 0)}/50 · XGBoost {diag['backbone_counts'].get('xgboost', 0)}/50 · CatBoost {diag['backbone_counts'].get('catboost', 0)}/50 · MLP 0/50 · FT-Transformer 0/50",
        "",
        "## KEEP lineage",
        "",
        "| Exp | Backbone | Delta | Test RMSE | Val RMSE | Composite |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for e in keeps:
        desc = (e.get("description") or "").replace(f"Exp{e['experiment_num']} ", "")
        lines.append(
            f"| {e['experiment_num']} | {e['backbone']} | {desc} | {e['test_primary']:.3f} | {e['val_primary']:.3f} | {e['composite']:.3f} |"
        )
    lines += [
        "",
        "## All experiments",
        "",
        "| Exp | Status | Backbone | Test RMSE | Val RMSE | Composite | MAE | R² |",
        "|---:|---|---|---:|---:|---:|---:|---:|",
    ]
    for e in log:
        sec = e.get("secondary_metrics") or {}
        lines.append(
            f"| {e['experiment_num']} | {e.get('status')} | {e.get('backbone')} | "
            f"{e['test_primary']:.3f} | {e['val_primary']:.3f} | {e['composite']:.3f} | "
            f"{sec.get('mae', float('nan')):.3f} | {sec.get('r2', float('nan')):.4f} |"
        )
    lines += [
        "",
        "## Champion residual slices (2014 test)",
        "",
        f"- Onset hours (Δ ≥ 50 µg/m³): n={diag['onset']['n']} RMSE={diag['onset']['rmse']:.1f} (pred {diag['onset']['mean_pred']:.0f} vs actual {diag['onset']['mean_actual']:.0f})",
        f"- Worst month: {diag['worst_month']['month']:02d} RMSE={diag['worst_month']['rmse']:.2f}",
        f"- Best month: {diag['best_month']['month']:02d} RMSE={diag['best_month']['rmse']:.2f}",
        f"- Worst hour: {diag['worst_hour']['hour']:02d}:00 RMSE={diag['worst_hour']['rmse']:.2f}",
        f"- Spike F1@75: {diag['spike_f1_75']['f1']:.3f} (P={diag['spike_f1_75']['precision']:.3f} R={diag['spike_f1_75']['recall']:.3f})",
        f"- p99 |error|={diag['p99_abs']:.1f} · max |error|={diag['max_abs']:.1f}",
        "",
    ]
    (RESULTS / "experiment_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    log = load_log()
    pred = champion_preds()
    diag = build_diagnostics(pred, log)
    (RESULTS / "champion_diagnostics.json").write_text(json.dumps(diag, indent=2), encoding="utf-8")
    write_summary(log, diag)
    print(json.dumps({
        "n": diag["n_test"],
        "test_rmse": round(diag["test_rmse"], 4),
        "onset_n": diag["onset"]["n"],
        "onset_rmse": None if diag["onset"]["rmse"] is None else round(diag["onset"]["rmse"], 2),
        "worst_month": diag["worst_month"],
        "worst_hour": diag["worst_hour"],
        "spike_f1_75": round(diag["spike_f1_75"]["f1"], 4),
        "skill": round(diag["skill_vs_persistence"], 4),
    }, indent=2))


if __name__ == "__main__":
    main()
