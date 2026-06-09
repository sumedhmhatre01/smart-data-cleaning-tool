# Smart Data Cleaning Tool

A professional data cleaning and preprocessing application built with Streamlit, Pandas, and NumPy.

The tool helps users quickly analyze datasets, identify common data quality issues, apply automated cleaning techniques, and download the cleaned data for further analysis.

## Features

- Upload CSV files
- Dataset preview
- Dataset profiling dashboard
- Missing value detection
- Duplicate row detection
- Outlier detection using NumPy Z-Score
- Data quality scoring
- Smart rule-based cleaning suggestions
- Automatic data cleaning
- Cleaned dataset preview
- Download cleaned dataset as CSV

## Technologies Used

- Python
- NumPy
- Pandas
- Streamlit

## Auto Cleaning Operations

The Auto Clean feature performs:

- Removal of duplicate rows
- Filling numeric missing values using median
- Filling categorical missing values using mode

## Outlier Detection

Outliers are detected using the Z-Score method implemented entirely with NumPy without using SciPy.

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

