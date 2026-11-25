"""
Cynaris Project 1 - Exploratory Data Analysis of Indian Equity Market Data
Dataset: tejhq/indian-markets (NSE subset) on Hugging Face.
This script downloads a reproducible sample at runtime, performs EDA with
Pandas and Matplotlib, and writes charts, CSV summaries, and a 5-finding report.
"""
import argparse
from pathlib import Path
import warnings

import pandas as pd
import matplotlib.pyplot as plt
from datasets import load_dataset

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
DATA_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

def load_market_data(max_rows: int = 100_000) -> pd.DataFrame:
    print("Connecting to the public Hugging Face Indian markets dataset...")
    stream = load_dataset(
        "tejhq/indian-markets",
        "nse",
        split="train",
        streaming=True
    )
    # Shuffle a bounded buffer so the sample is not limited to the first ticker.
    sample = list(stream.shuffle(seed=42, buffer_size=50_000).take(max_rows))
    if not sample:
        raise RuntimeError("No rows were returned by the dataset source.")
    df = pd.DataFrame(sample)
    df.to_csv(DATA_DIR / "nse_sample.csv", index=False)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    required = ["date", "symbol", "series", "open", "high", "low",
                "close", "prev_close", "volume", "turnover"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Dataset is missing expected columns: {missing}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    numeric = ["open", "high", "low", "close", "prev_close", "volume", "turnover"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["date", "symbol", "close", "volume", "turnover"])
    df = df[df["series"].astype(str).eq("EQ")]
    df = df[(df["close"] > 0) & (df["volume"] >= 0) & (df["turnover"] >= 0)]
    df = df.drop_duplicates(subset=["date", "symbol", "series"])
    df = df.sort_values(["symbol", "date"]).reset_index(drop=True)
    df["daily_return_pct"] = (
        df.groupby("symbol")["close"].pct_change() * 100
    )
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df

def make_charts(df: pd.DataFrame) -> dict:
    plt.figure(figsize=(11, 5))
    yearly = df.groupby("year")["turnover"].sum().sort_index()
    yearly.plot(kind="bar")
    plt.title("Total Trading Turnover by Year (Sample)")
    plt.xlabel("Year")
    plt.ylabel("Turnover (dataset units)")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "yearly_turnover.png", dpi=160)
    plt.close()

    top_volume = (df.groupby("symbol")["volume"].sum()
                    .sort_values(ascending=False).head(10).sort_values())
    plt.figure(figsize=(10, 6))
    top_volume.plot(kind="barh")
    plt.title("Top 10 Symbols by Total Traded Volume (Sample)")
    plt.xlabel("Total traded volume (shares)")
    plt.ylabel("NSE symbol")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "top_10_volume_symbols.png", dpi=160)
    plt.close()

    volatility = (df.groupby("symbol")["daily_return_pct"]
                    .agg(["std", "count"])
                    .query("count >= 20")
                    .sort_values("std", ascending=False).head(10))
    plt.figure(figsize=(10, 6))
    volatility["std"].sort_values().plot(kind="barh")
    plt.title("Top 10 Symbols by Daily Return Volatility (20+ observations)")
    plt.xlabel("Standard deviation of daily return (%)")
    plt.ylabel("NSE symbol")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "return_volatility.png", dpi=160)
    plt.close()

    monthly = df.groupby("month")["turnover"].sum().sort_index()
    plt.figure(figsize=(12, 5))
    monthly.plot()
    plt.title("Monthly Trading Turnover (Sample)")
    plt.xlabel("Month")
    plt.ylabel("Turnover (dataset units)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "monthly_turnover.png", dpi=160)
    plt.close()

    return {"yearly": yearly, "top_volume": top_volume,
            "volatility": volatility, "monthly": monthly}

def write_report(df: pd.DataFrame, charts: dict) -> None:
    n_rows = len(df)
    n_symbols = df["symbol"].nunique()
    start = df["date"].min().date()
    end = df["date"].max().date()
    total_turnover = df["turnover"].sum()
    median_volume = df["volume"].median()
    top_symbol = charts["top_volume"].idxmax()
    top_symbol_volume = charts["top_volume"].max()
    top_vol_symbol = charts["volatility"].index[-1] if not charts["volatility"].empty else "Not available"
    top_vol_value = charts["volatility"]["std"].max() if not charts["volatility"].empty else float("nan")
    best_year = charts["yearly"].idxmax() if not charts["yearly"].empty else "Not available"
    best_year_turnover = charts["yearly"].max() if not charts["yearly"].empty else float("nan")
    avg_return = df["daily_return_pct"].mean()
    missing_pct = (df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100

    report = f"""# Business Insight Report: Exploratory Analysis of Indian NSE Equity Data

## 1. Objective
Explore a reproducible sample of Indian National Stock Exchange (NSE) equity records
using Python, Pandas, and Matplotlib. The analysis examines trading activity,
symbol-level participation, price-return behaviour, and data quality.

## 2. Dataset and scope
- Source: `tejhq/indian-markets`, NSE subset on Hugging Face.
- Source page: https://huggingface.co/datasets/tejhq/indian-markets
- Records analysed after cleaning: **{n_rows:,}**
- Unique NSE symbols: **{n_symbols:,}**
- Date range represented in the sample: **{start} to {end}**
- Dataset fields used: date, symbol, series, open, high, low, close,
  previous close, volume, and turnover.
- This project uses a shuffled sample of up to 100,000 records for a manageable
  beginner-level analysis. It is not a full-market census.

## 3. Methodology
1. Loaded the NSE subset in streaming mode to avoid downloading the entire dataset.
2. Shuffled a bounded buffer with a fixed random seed and selected up to 100,000 rows.
3. Converted date and numeric columns to appropriate types.
4. Removed rows missing essential date, symbol, close, volume, or turnover values.
5. Kept equity-series (`EQ`) records, removed invalid non-positive closing prices,
   and removed duplicate date-symbol-series records.
6. Calculated daily percentage returns by symbol using `pct_change()`.
7. Grouped data by year, month, and symbol; visualised the results with Matplotlib.

## 4. Five data-driven findings

1. **Trading activity is concentrated in a small group of symbols.**
   The highest-volume symbol in this sample is **{top_symbol}**, with
   **{top_symbol_volume:,.0f}** shares traded. This can help analysts identify
   securities that deserve closer liquidity monitoring.

2. **Trading turnover varies across years.**
   The year with the highest total turnover in this sample is **{best_year}**,
   with turnover of **{best_year_turnover:,.2f}** in the source dataset's units.
   This is a sample-level observation and should not be interpreted as a market-wide
   trend without checking the full dataset.

3. **Some symbols show greater day-to-day price variability.**
   Among symbols with at least 20 observations, **{top_vol_symbol}** has the highest
   standard deviation of daily percentage returns (**{top_vol_value:.3f}%**).
   Higher historical variability indicates a need for careful risk monitoring;
   it does not predict future performance.

4. **The sample provides a baseline for return analysis.**
   The mean daily percentage return across valid symbol-day observations is
   **{avg_return:.4f}%**. This is an unweighted descriptive average, not an index
   return or an investment-performance measure.

5. **Data quality checks are essential before reporting.**
   After cleaning, the combined missing-cell rate across the analysed table is
   **{missing_pct:.2f}%**. Analysts should retain the cleaning log and check whether
   missingness is concentrated in particular columns or symbols before drawing
   broader conclusions.

## 5. Business recommendations
- Use turnover and volume summaries to prioritise liquidity monitoring.
- Review high-volatility symbols separately rather than treating all securities alike.
- Compare monthly and yearly activity using consistent full-period coverage.
- Validate unusual values and missingness with the original exchange records.
- Do not use this descriptive EDA as a buy/sell recommendation.

## 6. Limitations
- The analysis is based on a shuffled sample of up to 100,000 NSE records, not the
  full 7.38-million-row NSE subset.
- A shuffled streaming sample is not guaranteed to be perfectly representative.
- Historical price and volume patterns are descriptive and do not establish causality.
- The source dataset describes Indian exchange-listed equities, not retail sales,
  e-commerce orders, or HR records. The assignment itself lists NSE 500 data as a
  recommended option, so this project follows that Indian-market direction.

## 7. Reproducibility
Run `python main.py --rows 100000`. The script downloads the sample, cleans it,
creates charts under `outputs/`, saves the sample under `data/`, and regenerates
this report with actual computed values.
"""
    (ROOT / "Business_Insight_Report.md").write_text(report, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="NSE Indian market EDA")
    parser.add_argument("--rows", type=int, default=100_000,
                        help="Maximum number of streamed records to analyse")
    args = parser.parse_args()
    warnings.filterwarnings("ignore", category=FutureWarning)

    raw = load_market_data(args.rows)
    df = clean_data(raw)
    if df.empty:
        raise RuntimeError("No usable EQ records remained after cleaning.")

    df.to_csv(OUT_DIR / "cleaned_nse_sample.csv", index=False)
    df.groupby("symbol").agg(
        observations=("close", "count"),
        mean_close=("close", "mean"),
        total_volume=("volume", "sum"),
        total_turnover=("turnover", "sum"),
        return_volatility=("daily_return_pct", "std")
    ).sort_values("total_turnover", ascending=False).to_csv(
        OUT_DIR / "symbol_summary.csv"
    )
    charts = make_charts(df)
    write_report(df, charts)
    print(f"Analysis complete. {len(df):,} cleaned rows, {df['symbol'].nunique():,} symbols.")
    print(f"Report: {ROOT / 'Business_Insight_Report.md'}")
    print(f"Charts and CSV summaries: {OUT_DIR}")

if __name__ == "__main__":
    main()
