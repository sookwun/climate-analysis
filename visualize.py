import csv
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def linear_fit(xs, ys):
    x_mean = statistics.mean(xs)
    y_mean = statistics.mean(ys)
    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)) / \
            sum((x - x_mean) ** 2 for x in xs)
    intercept = y_mean - slope * x_mean
    return slope, intercept


def plot_global_trend(ax, rows):
    years = [int(r["year"]) for r in rows]
    temps = [float(r["global_avg_celsius"]) for r in rows]
    slope, intercept = linear_fit(years, temps)
    trend = [slope * y + intercept for y in years]

    ax.plot(years, temps, color="#2196F3", linewidth=1.5, label="Annual avg")
    ax.plot(years, trend, color="#F44336", linewidth=1.5, linestyle="--",
            label=f"Trend (+{slope * 10:.3f} °C/decade)")
    ax.fill_between(years, temps, trend,
                    where=[t > tr for t, tr in zip(temps, trend)],
                    alpha=0.15, color="#F44336")
    ax.fill_between(years, temps, trend,
                    where=[t <= tr for t, tr in zip(temps, trend)],
                    alpha=0.15, color="#2196F3")
    ax.set_title("Global Average Temperature (1980–2024)")
    ax.set_ylabel("°C")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def plot_anomaly_bars(ax, rows):
    years = [int(r["year"]) for r in rows]
    anomalies = [float(r["anomaly_celsius"]) for r in rows]
    colors = ["#F44336" if a >= 0 else "#2196F3" for a in anomalies]

    ax.bar(years, anomalies, color=colors, width=0.8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Temperature Anomaly vs. 1951–1980 Baseline")
    ax.set_ylabel("°C anomaly")
    ax.grid(True, alpha=0.3, axis="y")


def plot_decadal_warming(ax, rows):
    by_decade = defaultdict(list)
    for r in rows:
        decade = (int(r["year"]) // 10) * 10
        by_decade[decade].append(float(r["anomaly_celsius"]))

    decades = sorted(by_decade)
    avgs = [statistics.mean(by_decade[d]) for d in decades]
    colors = ["#F44336" if a >= 0 else "#2196F3" for a in avgs]
    labels = [f"{d}s" for d in decades]

    bars = ax.bar(labels, avgs, color=colors, edgecolor="white", linewidth=0.5)
    for bar, avg in zip(bars, avgs):
        ax.text(bar.get_x() + bar.get_width() / 2,
                avg + (0.01 if avg >= 0 else -0.03),
                f"{avg:+.2f}", ha="center", va="bottom", fontsize=8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Average Anomaly by Decade")
    ax.set_ylabel("°C anomaly")
    ax.grid(True, alpha=0.3, axis="y")


def plot_seasonal(ax, rows):
    by_month = defaultdict(list)
    for r in rows:
        by_month[int(r["month"])].append(float(r["temp_celsius"]))

    months = list(range(1, 13))
    avgs = [statistics.mean(by_month[m]) for m in months]
    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    ax.plot(month_names, avgs, color="#4CAF50", linewidth=2, marker="o", markersize=5)
    ax.fill_between(month_names, avgs, min(avgs), alpha=0.15, color="#4CAF50")
    ax.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax.set_title("Seasonal Temperature Cycle (Northeast US)")
    ax.set_ylabel("°C")
    ax.grid(True, alpha=0.3)


def plot_hemisphere_gap(ax, rows):
    years = [int(r["year"]) for r in rows]
    nh = [float(r["northern_hemisphere"]) for r in rows]
    sh = [float(r["southern_hemisphere"]) for r in rows]

    ax.plot(years, nh, label="Northern hemisphere", color="#FF9800", linewidth=1.5)
    ax.plot(years, sh, label="Southern hemisphere", color="#9C27B0", linewidth=1.5)
    ax.fill_between(years, nh, sh, alpha=0.1, color="gray")
    ax.set_title("Northern vs. Southern Hemisphere Temperatures")
    ax.set_ylabel("°C")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


if __name__ == "__main__":
    annual = load_csv("temperature_annual.csv")
    monthly = load_csv("temperature_monthly.csv")

    fig = plt.figure(figsize=(14, 10))
    fig.suptitle("Climate Analysis Dashboard", fontsize=14, fontweight="bold", y=0.98)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.3)

    plot_global_trend(fig.add_subplot(gs[0, :]), annual)
    plot_anomaly_bars(fig.add_subplot(gs[1, :]), annual)
    plot_decadal_warming(fig.add_subplot(gs[2, 0]), annual)
    plot_seasonal(fig.add_subplot(gs[2, 1]), monthly)

    plt.savefig("climate_dashboard.png", dpi=150, bbox_inches="tight")
    print("Saved climate_dashboard.png")
