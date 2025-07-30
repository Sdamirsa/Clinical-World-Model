#!/usr/bin/env python3
"""
Analyze WHO DALY 2021 data to extract global disease statistics
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path

# Define paths
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data"
ANALYSIS_PATH = DATA_PATH / "analysis"

def load_daly_data():
    """Load the WHO DALY 2021 CSV file"""
    csv_path = DATA_PATH / "WHO DALY 2021.csv"
    return pd.read_csv(csv_path)

def analyze_global_daly(df):
    """Analyze DALY data to get global disease statistics"""
    
    # Filter for 2019 data (most recent pre-COVID year)
    df_2019 = df[df['YEAR'] == 2019]
    
    # Group by disease and sum across all countries, sexes, and age groups
    disease_daly = df_2019.groupby(['GHE_CAUSE_CODE', 'GHE_CAUSE_TITLE', 'GHE_CAUSE_TYPE']).agg({
        'DALY': 'sum',
        'DEATHS': 'sum',
        'POPULATION': 'sum'
    }).reset_index()
    
    # Calculate rates per 100,000
    disease_daly['DALY_PER_100K'] = (disease_daly['DALY'] / disease_daly['POPULATION']) * 100000
    disease_daly['DEATHS_PER_100K'] = (disease_daly['DEATHS'] / disease_daly['POPULATION']) * 100000
    
    # Sort by total DALY
    disease_daly = disease_daly.sort_values('DALY', ascending=False)
    
    # Add ranking
    disease_daly['GLOBAL_RANK'] = range(1, len(disease_daly) + 1)
    
    # Categorize by DALY burden
    disease_daly['DALY_CATEGORY'] = pd.cut(
        disease_daly['GLOBAL_RANK'],
        bins=[0, 10, 30, 50, float('inf')],
        labels=['very-high', 'high', 'moderate', 'low']
    )
    
    return disease_daly

def get_disease_categories(df):
    """Extract unique disease categories"""
    categories = df.groupby(['GHE_CAUSE_TYPE']).agg({
        'GHE_CAUSE_CODE': 'count'
    }).reset_index()
    categories.columns = ['category', 'count']
    return categories

def save_analysis_results(disease_stats, categories):
    """Save analysis results to JSON files"""
    ANALYSIS_PATH.mkdir(exist_ok=True)
    
    # Save disease statistics
    stats_output = {
        'data_source': 'WHO Global Health Estimates 2021',
        'analysis_year': 2019,
        'notes': 'Data represents top 25 economies, extrapolated for global burden',
        'total_diseases': len(disease_stats),
        'diseases': []
    }
    
    for _, row in disease_stats.iterrows():
        disease_entry = {
            'rank': int(row['GLOBAL_RANK']),
            'code': row['GHE_CAUSE_CODE'],
            'title': row['GHE_CAUSE_TITLE'],
            'type': row['GHE_CAUSE_TYPE'],
            'daly_total': float(row['DALY']),
            'daly_per_100k': float(row['DALY_PER_100K']),
            'deaths_total': float(row['DEATHS']),
            'deaths_per_100k': float(row['DEATHS_PER_100K']),
            'daly_category': row['DALY_CATEGORY']
        }
        stats_output['diseases'].append(disease_entry)
    
    # Save to JSON
    stats_path = ANALYSIS_PATH / 'global_daly_statistics.json'
    with open(stats_path, 'w') as f:
        json.dump(stats_output, f, indent=2)
    
    print(f"Saved disease statistics to {stats_path}")
    
    # Save top diseases summary
    top_diseases = disease_stats.head(50)
    summary_output = {
        'top_10_diseases': [],
        'top_30_diseases': [],
        'disease_categories': {}
    }
    
    # Top 10 diseases
    for _, row in top_diseases.head(10).iterrows():
        summary_output['top_10_diseases'].append({
            'rank': int(row['GLOBAL_RANK']),
            'title': row['GHE_CAUSE_TITLE'],
            'daly_total': float(row['DALY']),
            'type': row['GHE_CAUSE_TYPE']
        })
    
    # Top 30 diseases
    for _, row in top_diseases.head(30).iterrows():
        summary_output['top_30_diseases'].append({
            'rank': int(row['GLOBAL_RANK']),
            'title': row['GHE_CAUSE_TITLE'],
            'code': row['GHE_CAUSE_CODE']
        })
    
    # Count by category
    category_counts = disease_stats.groupby('GHE_CAUSE_TYPE').size().to_dict()
    summary_output['disease_categories'] = category_counts
    
    summary_path = ANALYSIS_PATH / 'daly_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary_output, f, indent=2)
    
    print(f"Saved summary to {summary_path}")
    
    return stats_path, summary_path

def print_top_diseases(disease_stats, n=20):
    """Print top N diseases by DALY"""
    print(f"\nTop {n} Diseases by Global DALY Burden (2019)")
    print("=" * 80)
    print(f"{'Rank':<6}{'Disease':<50}{'DALY (millions)':<20}{'Type':<20}")
    print("-" * 80)
    
    for _, row in disease_stats.head(n).iterrows():
        daly_millions = row['DALY'] / 1_000_000
        print(f"{row['GLOBAL_RANK']:<6}{row['GHE_CAUSE_TITLE'][:48]:<50}{daly_millions:<20.2f}{row['GHE_CAUSE_TYPE']:<20}")

if __name__ == "__main__":
    print("Loading WHO DALY 2021 data...")
    df = load_daly_data()
    
    print(f"Loaded {len(df)} records")
    print(f"Countries: {df['COUNTRY'].nunique()}")
    print(f"Years: {sorted(df['YEAR'].unique())}")
    print(f"Disease categories: {df['GHE_CAUSE_TYPE'].nunique()}")
    
    print("\nAnalyzing global DALY burden...")
    disease_stats = analyze_global_daly(df)
    
    print("\nExtracting disease categories...")
    categories = get_disease_categories(df)
    
    print("\nSaving analysis results...")
    stats_path, summary_path = save_analysis_results(disease_stats, categories)
    
    # Print summary
    print_top_diseases(disease_stats, n=30)
    
    print("\nAnalysis complete!")
    print(f"Results saved to:")
    print(f"  - {stats_path}")
    print(f"  - {summary_path}")