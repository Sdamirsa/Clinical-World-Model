#!/usr/bin/env python3
"""
Explore WHO DALY data structure
"""

import pandas as pd
from pathlib import Path

# Define paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"

# Load data
csv_path = DATA_PATH / "WHO DALY 2021.csv"
df = pd.read_csv(csv_path)

print("Column Info:")
print(df.info())
print("\n" + "="*80 + "\n")

print("First 5 rows:")
print(df.head())
print("\n" + "="*80 + "\n")

print("GHE_CAUSE_CODE types:")
print(df['GHE_CAUSE_CODE'].dtype)
print("Sample values:")
print(df['GHE_CAUSE_CODE'].unique()[:20])
print("\n" + "="*80 + "\n")

print("GHE_CAUSE_TYPE unique values:")
print(df['GHE_CAUSE_TYPE'].unique())
print("\n" + "="*80 + "\n")

print("Sample diseases:")
print(df[['GHE_CAUSE_CODE', 'GHE_CAUSE_TITLE', 'GHE_CAUSE_TYPE']].drop_duplicates().head(20))