import csv
import statistics
from collections import defaultdict


def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def trend_analysis(rows):
    """Linear trend in global average temperature over time."""
    years = [int(r["year"]) for r in rows]
    temps = [float(r["global_avg_celsius"]) for r in rows]

    n = len(years)
    x_mean = statistics.mean(years)
    y_mean = statistics.mean(temps)

    slope = sum((x - x_mean) * (y - y_mean) for x, y in zip(years, temps)) / \
            sum((x - x_mean) ** 2 for x in years)

    print("=== Global Temperature Trend ===")
    print(f"  Period: {years[0]}–{years[-1]}")
    print(f"  Warming rate: {slope * 10:.3f} °C per decade")
    print(f"  Total change: {temps[-1] - temps[0]:.2f} °C")
    print()


def anomaly_analysis(rows):
    """Identify the hottest and coldest years by anomaly."""
    sorted_rows = sorted(rows, key=lambda r: float(r["anomaly_celsius"]))

    print("=== Temperature Anomalies ===")
    print("  5 coldest years:")
    for r in sorted_rows[:5]:
        print(f"    {r['year']}: {float(r['anomaly_celsius']):+.2f} °C")
    print("  5 hottest years:")
    for r in reversed(sorted_rows[-5:]):
        print(f"    {r['year']}: {float(r['anomaly_celsius']):+.2f} °C")
    print()


def seasonal_patterns(rows):
    """Average temperature by month across all recorded years."""
    by_month = defaultdict(list)
    for r in rows:
        by_month[int(r["month"])].append(float(r["temp_celsius"]))

    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    print("=== Seasonal Patterns (Northeast US) ===")
    for month in range(1, 13):
        avg = statistics.mean(by_month[month])
        bar = "#" * int((avg + 5) * 0.8)
        print(f"  {month_names[month-1]}: {avg:6.1f} °C  {bar}")
    print()


def decadal_warming(rows):
    """Compare average anomaly across decades."""
    by_decade = defaultdict(list)
    for r in rows:
        decade = (int(r["year"]) // 10) * 10
        by_decade[decade].append(float(r["anomaly_celsius"]))

    print("=== Decadal Average Anomaly ===")
    for decade in sorted(by_decade):
        avg = statistics.mean(by_decade[decade])
        bar = "#" * int(abs(avg) * 10)
        sign = "+" if avg >= 0 else "-"
        print(f"  {decade}s: {sign}{abs(avg):.2f} °C  {bar}")
    print()


if __name__ == "__main__":
    annual = load_csv("temperature_annual.csv")
    monthly = load_csv("temperature_monthly.csv")

    trend_analysis(annual)
    anomaly_analysis(annual)
    decadal_warming(annual)
    seasonal_patterns(monthly)
