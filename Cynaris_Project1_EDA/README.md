# Cynaris Internship – Project 1: Exploratory Data Analysis

**Student:** Rajendra Prasad V  
**Role:** Data Analyst Intern  
**Tools:** Python, Pandas, Matplotlib

## Project overview
This project performs exploratory data analysis on a customer/lead dataset from an Indian real-estate business context. It examines customer segments, lead sources, locations, budgets, site visits, conversion status and recorded customer spend.

> Dataset-fit note: The provided dataset is a real-estate customer/lead dataset, not a conventional e-commerce or retail transactions dataset. The assignment brief allows an Indian business dataset but lists e-commerce, retail or HR as examples. If Cynaris strictly requires one of those categories, replace this dataset before submitting.

## Dataset
- File: `data/customer_profiles.csv`
- Records: 250
- Fields: 16
- Customer records span 2026-01-02 to 2026-10-27.
- No missing cells detected in the loaded dataset; duplicate customer IDs: 0.

## How to run
1. Install Python 3.9+.
2. Open a terminal in this folder.
3. Run `pip install -r requirements.txt`.
4. Run `python eda_analysis.py`.

The script prints descriptive statistics and grouped conversion summaries, then saves charts in `outputs/`.

## Five key findings
1. Overall, 56 of 250 records are marked **Closed Won**, a closed-won rate of **22.4%**.
2. **Luxury Upgrader** has the highest segment closed-won rate (34.2%), while **Channel Partner / Broker** has the lowest (15.0%).
3. **Organic Search** has the highest closed-won rate by lead source (25.5%). This is an observed association, not proof that the channel caused conversion.
4. **Bengaluru** is the largest city group with 205 records; Bengaluru accounts for 205 of 250 records.
5. Converted records have an average of 3.00 completed site visits versus 2.93 for records not marked Closed Won. The difference is descriptive and does not establish causality.

## Methodology and assumptions
- Loaded the CSV with Pandas and parsed `signup_date` as a date.
- Checked dataset dimensions, data types, missing values and duplicate customer IDs.
- Used `conversion_status == "Closed Won"` as the conversion definition.
- Used the midpoint of minimum and maximum budget as a simple budget estimate for exploratory summaries only.
- Compared groups using counts, means and conversion proportions.
- Created Matplotlib bar charts and a spend-by-status box plot.
- No predictive model or causal inference was attempted.

## Limitations
- This dataset contains 250 records and may be synthetic or curated; findings should not be generalized to the entire Indian property market.
- Conversion status is a snapshot; the data does not establish when a lead became a customer.
- Small city groups can produce unstable conversion percentages.
- Recorded spend should not automatically be interpreted as property transaction value or company revenue.

## Project structure
```text
Cynaris_Project1_EDA/
├── data/customer_profiles.csv
├── outputs/                 # generated charts
├── eda_analysis.py
├── README.md
└── requirements.txt
```
