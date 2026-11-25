"""
Cynaris Internship Project 1: Exploratory Data Analysis
Dataset: customer_profiles.csv (Indian real-estate customer/lead business dataset)

Run:
    pip install -r requirements.txt
    python eda_analysis.py

Outputs are written to the outputs/ folder.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "customer_profiles.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["is_converted"] = df["conversion_status"].eq("Closed Won")
df["budget_mid_lakhs"] = (df["budget_min_lakhs"] + df["budget_max_lakhs"]) / 2

print("DATASET OVERVIEW")
print("Rows, columns:", df.shape)
print("\\nData types:\\n", df.dtypes)
print("\\nMissing values:\\n", df.isna().sum())
print("\\nDuplicate customer IDs:", df["customer_id"].duplicated().sum())
print("\\nNumerical summary:\\n", df.describe().round(2))

print("\\nCUSTOMER SEGMENT ANALYSIS")
print(df.groupby("customer_segment").agg(
    customers=("customer_id", "count"),
    closed_won=("is_converted", "sum"),
    conversion_rate=("is_converted", "mean"),
    average_spend_inr=("total_spend_inr", "mean")
).sort_values("conversion_rate", ascending=False).round(3))

print("\\nLEAD SOURCE ANALYSIS")
print(df.groupby("lead_source").agg(
    customers=("customer_id", "count"),
    closed_won=("is_converted", "sum"),
    conversion_rate=("is_converted", "mean")
).sort_values("conversion_rate", ascending=False).round(3))

print("\\nCITY ANALYSIS")
print(df.groupby("city_of_residence").agg(
    customers=("customer_id", "count"),
    closed_won=("is_converted", "sum"),
    conversion_rate=("is_converted", "mean")
).sort_values("customers", ascending=False).round(3))

# Charts
charts = [
    ("customer_segment", "Customers by Segment", "Customer Segment", "Customers", "customers_by_segment.png"),
    ("lead_source", "Customers by Lead Source", "Lead Source", "Customers", "customers_by_source.png"),
    ("city_of_residence", "Customers by City", "City", "Customers", "customers_by_city.png"),
]
for col, title, xlabel, ylabel, filename in charts:
    plt.figure(figsize=(8, 5))
    df[col].value_counts().plot(kind="bar")
    plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.xticks(rotation=25, ha="right"); plt.tight_layout()
    plt.savefig(OUT / filename, dpi=150); plt.close()

for group_col, filename, title in [
    ("customer_segment", "conversion_by_segment.png", "Closed-Won Rate by Customer Segment"),
    ("lead_source", "conversion_by_source.png", "Closed-Won Rate by Lead Source"),
]:
    rates = df.groupby(group_col)["is_converted"].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(8, 5)); rates.plot(kind="bar")
    plt.title(title); plt.xlabel(group_col.replace("_", " ").title()); plt.ylabel("Closed-Won Rate (%)")
    plt.xticks(rotation=25, ha="right"); plt.tight_layout()
    plt.savefig(OUT / filename, dpi=150); plt.close()

plt.figure(figsize=(7, 5))
df.boxplot(column="total_spend_inr", by="conversion_status", grid=False)
plt.title("Customer Spend by Conversion Status"); plt.suptitle("")
plt.xlabel("Conversion Status"); plt.ylabel("Total Spend (INR)")
plt.tight_layout(); plt.savefig(OUT / "spend_by_status.png", dpi=150); plt.close()

print("\\nOVERALL CLOSED-WON RATE:", round(df["is_converted"].mean() * 100, 2), "%")
print("Total recorded spend (INR):", round(df["total_spend_inr"].sum(), 2))
print("\\nCharts saved to:", OUT)
