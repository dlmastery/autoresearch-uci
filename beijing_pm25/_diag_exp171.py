"""One-off Exp167 January-onset diagnosis for Exp171. Not part of the loop."""
from pathlib import Path

import json
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
log = HERE / "autoresearch_results" / "experiment_log.jsonl"
rows = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines() if l.strip()]
print("n_exps", len(rows), "last", rows[-1]["experiment_num"], rows[-1]["status"], rows[-1]["description"][:80])
for e in rows[-5:]:
    print(e["experiment_num"], e["status"], f"c={e['composite']:.3f}", f"test={e['test_primary']:.3f}", f"val={e['val_primary']:.3f}")

pred = pd.read_csv(HERE / "autoresearch_results/trade_logs/exp167_predictions.csv")
feat = pd.read_csv(HERE / "data/features_full.csv")
times = pd.read_csv(HERE / "data/times.csv", parse_dates=["time"])
feat["time"] = times["time"]
df = feat.iloc[pred["index"].values].copy()
df["pred"] = pred["prediction"].values
df["actual"] = pred["actual"].values
df["err"] = df["pred"] - df["actual"]
df["need"] = df["actual"] - df["pm25_lag1"]
df["pred_d"] = df["pred"] - df["pm25_lag1"]
df["month"] = df["time"].dt.month
df["hour"] = df["time"].dt.hour
df["dow"] = df["time"].dt.dayofweek
sse = float((df["err"] ** 2).sum())
persist_err = df["pm25_lag1"] - df["actual"]


def sl(name, m):
    n = int(m.sum())
    if n == 0:
        print(f"{name}: n=0")
        return
    rmse = float(np.sqrt((df.loc[m, "err"] ** 2).mean()))
    prmse = float(np.sqrt((persist_err[m].values ** 2).mean()))
    sse_frac = float((df.loc[m, "err"] ** 2).sum()) / sse * 100
    print(
        f"{name}: n={n} RMSE={rmse:.2f} persist={prmse:.2f} sse={sse_frac:.2f}% "
        f"need={df.loc[m,'need'].mean():.2f} pred_d={df.loc[m,'pred_d'].mean():.2f} "
        f"lag1={df.loc[m,'pm25_lag1'].mean():.1f} Iws={df.loc[m,'Iws'].median():.2f} "
        f"rh={df.loc[m,'rh_magnus'].mean():.1f} inv={df.loc[m,'inversion_spread'].mean():.1f}"
    )


print("--- required ---")
sl("January", df.month == 1)
sl("JJA", df.month.isin([6, 7, 8]))
sl("hour20", df.hour == 20)
sl("onset", df.need > 50)
print("val bottleneck: val 21.972 vs test 20.072")

jan_on = (df.month == 1) & (df.need > 50)
print("\n--- January onset rows ---")
cols = ["time", "hour", "actual", "pred", "pm25_lag1", "need", "pred_d", "Iws", "cbwd_NW", "cbwd_SE", "cbwd_cv", "cbwd_NE", "rh_magnus", "inversion_spread", "is_heating", "pm25_delta1", "pm25_accel"]
sub = df.loc[jan_on, cols].copy()
sub["dir"] = np.where(sub.cbwd_SE > 0.5, "SE", np.where(sub.cbwd_NW > 0.5, "NW", np.where(sub.cbwd_NE > 0.5, "NE", "cv")))
print(sub[["time", "hour", "lag1" if "lag1" in sub else "pm25_lag1", "need", "pred_d", "Iws", "dir", "rh_magnus", "inversion_spread", "pm25_delta1"]].to_string(index=False))

print("\n--- January onset by dir ---")
for d in ["SE", "NW", "NE", "cv"]:
    sl(f"Jan onset {d}", jan_on & (sub["dir"].reindex(df.index).fillna("") == d) if False else jan_on & (
        (df.cbwd_SE > 0.5 if d == "SE" else False)
        | (df.cbwd_NW > 0.5 if d == "NW" else False)
        | (df.cbwd_NE > 0.5 if d == "NE" else False)
        | ((df.cbwd_cv > 0.5) if d == "cv" else False)
    ))

print("\n--- Jan onset anti-jump (pred_d<0) vs not ---")
sl("Jan onset pred_d<0", jan_on & (df.pred_d < 0))
sl("Jan onset pred_d>=0", jan_on & (df.pred_d >= 0))
sl("Jan onset NW", jan_on & (df.cbwd_NW > 0.5))
sl("Jan onset SE", jan_on & (df.cbwd_SE > 0.5))
sl("Jan onset cv", jan_on & (df.cbwd_cv > 0.5))
sl("Jan onset night 18-2", jan_on & ((df.hour >= 18) | (df.hour <= 2)))
sl("Jan onset Iws>=5", jan_on & (df.Iws >= 5))
sl("Jan onset Iws<5", jan_on & (df.Iws < 5))
sl("Jan onset lag1>=200", jan_on & (df.pm25_lag1 >= 200))
sl("Jan onset lag1<200", jan_on & (df.pm25_lag1 < 200))
sl("Jan onset accel<=0", jan_on & (df.pm25_accel <= 0))
sl("Jan onset accel>0", jan_on & (df.pm25_accel > 0))
sl("Jan onset delta1<=0", jan_on & (df.pm25_delta1 <= 0))
sl("Jan onset delta1>0", jan_on & (df.pm25_delta1 > 0))

print("\n--- broader anti-jump onsets ---")
sl("onset pred_d<0", (df.need > 50) & (df.pred_d < 0))
sl("onset pred_d>=0", (df.need > 50) & (df.pred_d >= 0))
sl("onset NW pred_d<0", (df.need > 50) & (df.cbwd_NW > 0.5) & (df.pred_d < 0))
sl("onset NW", (df.need > 50) & (df.cbwd_NW > 0.5))
sl("heating onset pred_d<0", (df.need > 50) & (df.is_heating > 0.5) & (df.pred_d < 0))
sl("DJF onset", (df.month.isin([12, 1, 2])) & (df.need > 50))
sl("DJF onset NW", (df.month.isin([12, 1, 2])) & (df.need > 50) & (df.cbwd_NW > 0.5))
sl("DJF onset NW pred_d<0", (df.month.isin([12, 1, 2])) & (df.need > 50) & (df.cbwd_NW > 0.5) & (df.pred_d < 0))

print("\n--- hour20 January ---")
sl("Jan hour20", (df.month == 1) & (df.hour == 20))
sl("Jan hour20 persist>=150", (df.month == 1) & (df.hour == 20) & (df.pm25_lag1 >= 150))
sl("heating hour 18-22 persist>=150", (df.is_heating > 0.5) & df.hour.isin([18, 19, 20, 21, 22]) & (df.pm25_lag1 >= 150))

print("\n--- collapse vs onset pred_d by NW ---")
sl("collapse NW", (df.need < -50) & (df.cbwd_NW > 0.5))
sl("onset NW Iws>=10", (df.need > 50) & (df.cbwd_NW > 0.5) & (df.Iws >= 10))
sl("onset NW Iws<10", (df.need > 50) & (df.cbwd_NW > 0.5) & (df.Iws < 10))
