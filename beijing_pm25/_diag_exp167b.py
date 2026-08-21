"""One-off Exp167 diagnosis. Not part of the experiment loop."""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
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
sse = float((df["err"] ** 2).sum())
persist_err = df["pm25_lag1"] - df["actual"]
print(
    f"n={len(df)} model={np.sqrt((df.err**2).mean()):.3f} "
    f"persist={np.sqrt((persist_err**2).mean()):.3f}"
)


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
        f"act={df.loc[m,'actual'].mean():.1f} pred={df.loc[m,'pred'].mean():.1f}"
    )


on = df.need > 50
print("--- required ---")
sl("January", df.month == 1)
sl("JJA", df.month.isin([6, 7, 8]))
sl("hour20", df.hour == 20)
sl("onset", on)
print("val bottleneck: val 21.972 vs test 20.072")

print("--- SE ---")
se = df.cbwd_SE == 1
sl("SE", se)
sl("onset+SE", on & se)
sl("onset+notSE", on & ~se)
sl("SE persist 50-150", se & (df.pm25_lag1 >= 50) & (df.pm25_lag1 < 150))
sl("SE persist>=150", se & (df.pm25_lag1 >= 150))
sl("SE need>20", se & (df.need > 20))
sl("SE need>30", se & (df.need > 30))
sl("SE persist>=50 need>20", se & (df.pm25_lag1 >= 50) & (df.need > 20))
sl("SE persist 50-150 need>30", se & (df.pm25_lag1 >= 50) & (df.pm25_lag1 < 150) & (df.need > 30))
sl("onset+SE persist<50", on & se & (df.pm25_lag1 < 50))
sl("onset+SE persist 50-150", on & se & (df.pm25_lag1 >= 50) & (df.pm25_lag1 < 150))
sl("onset+SE persist>=150", on & se & (df.pm25_lag1 >= 150))
sl("onset+SE Iws<5", on & se & (df.Iws < 5))
sl("onset+SE Iws>=5", on & se & (df.Iws >= 5))
sl("onset+SE Iws>=10", on & se & (df.Iws >= 10))
sl("onset+SE heating", on & se & (df.is_heating == 1))
sl("onset+SE hour18-21", on & se & df.hour.isin([18, 19, 20, 21]))
sl("SE hour20", se & (df.hour == 20))
sl("SE typical", se & (df.need.abs() <= 10))

print("onset+SE by month", df.loc[on & se].groupby("month").size().to_dict())
print("onset+SE by hour", df.loc[on & se].groupby("hour").size().to_dict())
print("onset+SE Iws p50", float(df.loc[on & se, "Iws"].median()), "non-onset SE", float(df.loc[se & ~on, "Iws"].median()))
print("onset+SE lag1 p50", float(df.loc[on & se, "pm25_lag1"].median()))
print("onset+SE pred_d p10/50/90", df.loc[on & se, "pred_d"].quantile([0.1, 0.5, 0.9]).tolist())
print("onset+SE need p10/50/90", df.loc[on & se, "need"].quantile([0.1, 0.5, 0.9]).tolist())
print("onset+SE frac pred_d<10", float((df.loc[on & se, "pred_d"] < 10).mean()))
print("onset+SE frac below lag1", float((df.loc[on & se, "pred_d"] < 0).mean()))
print("corr SE lag1 vs need among SE", float(df.loc[se, ["pm25_lag1", "need"]].corr().iloc[0, 1]))
print("corr SE Iws vs need among SE", float(df.loc[se, ["Iws", "need"]].corr().iloc[0, 1]))

print("--- other leftover ---")
sl("onset+accel<=0", on & (df.pm25_accel <= 0))
sl("onset Iws>=10", on & (df.Iws >= 10))
sl("hour01", df.hour == 1)
sl("hour09", df.hour == 9)
sl("typical", df.need.abs() <= 10)
sl("dirty-stable", (df.pm25_lag1 >= 150) & (df.need.abs() <= 10))

print("--- SE * lag1 idea ---")
df["se_pm"] = df.cbwd_SE * df.pm25_lag1
print("se_pm mean onset+SE", float(df.loc[on & se, "se_pm"].mean()), "SE non-onset", float(df.loc[se & ~on, "se_pm"].mean()), "non-SE", 0.0)
print("among SE, lag1 onset vs not", float(df.loc[on & se, "pm25_lag1"].mean()), float(df.loc[se & ~on, "pm25_lag1"].mean()))
