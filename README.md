# Cynaris Data Analyst Intern — Project 1: Indian Market EDA

## Project overview
This beginner-level project performs exploratory data analysis (EDA) on Indian
NSE equity-market data using Python, Pandas, and Matplotlib. It studies trading
volume, turnover, symbol-level participation, daily returns, and data quality.

## Dataset
- Name: `tejhq/indian-markets` — NSE subset
- Source: https://huggingface.co/datasets/tejhq/indian-markets
- Dataset description: daily end-of-day NSE/BSE equity records.
- This project uses a reproducible shuffled sample of up to 100,000 rows.
- The assignment page also lists NSE 500 companies as a recommended dataset.

## Tools
- Python 3.10+
- Pandas
- Matplotlib
- Hugging Face Datasets

## Run the project
```bash
python -m pip install -r requirements.txt
python main.py --rows 100000
```

The first run requires an internet connection. The script streams the public NSE
dataset, saves the sampled data to `data/nse_sample.csv`, cleans it, and creates:
- `outputs/cleaned_nse_sample.csv`
- `outputs/symbol_summary.csv`
- Four Matplotlib charts
- `Business_Insight_Report.md` with five findings calculated from the run

## Repository structure
```text
Cynaris_Indian_Market_EDA/
├── main.py
├── README.md
├── Business_Insight_Report.md
├── requirements.txt
├── .gitignore
├── data/
└── outputs/
```

## Important note
This is descriptive educational analysis, not investment advice. The output is
based on a sample and should not be treated as a complete representation of the
Indian equity market.
