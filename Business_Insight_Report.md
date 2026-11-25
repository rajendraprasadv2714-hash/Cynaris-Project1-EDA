# Business Insight Report: Exploratory Analysis of Indian NSE Equity Data

## 1. Objective
Explore a reproducible sample of Indian National Stock Exchange (NSE) equity records
using Python, Pandas, and Matplotlib. The analysis examines trading activity,
symbol-level participation, price-return behaviour, and data quality.

## 2. Dataset and scope
- Source: `tejhq/indian-markets`, NSE subset on Hugging Face.
- Source page: https://huggingface.co/datasets/tejhq/indian-markets
- Records analysed after cleaning: **91,218**
- Unique NSE symbols: **134**
- Date range represented in the sample: **2010-01-04 to 2023-12-29**
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
   The highest-volume symbol in this sample is **ADANIPOWER**, with
   **19,367,013,426** shares traded. This can help analysts identify
   securities that deserve closer liquidity monitoring.

2. **Trading turnover varies across years.**
   The year with the highest total turnover in this sample is **2023**,
   with turnover of **5,798,576,005,000.11** in the source dataset's units.
   This is a sample-level observation and should not be interpreted as a market-wide
   trend without checking the full dataset.

3. 3.3. Some symbols show greater day-to-day price variability.

Among symbols with at least 20 observations, ALLSEC has the highest standard deviation of daily percentage returns (63.887%). Higher historical variability indicates a need for careful risk monitoring; it does not predict future performance.

4. **The sample provides a baseline for return analysis.**
   The mean daily percentage return across valid symbol-day observations is
   **0.1461%**. This is an unweighted descriptive average, not an index
   return or an investment-performance measure.
5. Data quality checks are essential before reporting.

After cleaning, the combined missing-cell rate across all 17 columns is approximately 7.81%. Missing values are concentrated in optional fields such as name, ISIN and trades. Analysts should distinguish essential analytical fields from optional metadata when assessing data quality.

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
