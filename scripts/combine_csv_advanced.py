import pandas as pd
import os
from datetime import datetime

# Get today's date in the format MMDDYYYY
today_date = datetime.now().strftime('%m%d%Y')

# File paths
aristocrats_file = 'data/DividendAristocrats_02032025.csv'
champions_file = 'data/DividendChampions_02032025.csv'
kings_file = 'data/DividendKing_02032025.csv'
output_file = f'data/CombinedDividendStocks_{today_date}.csv'

# Read CSV files
print(f"Reading {aristocrats_file}...")
aristocrats_df = pd.read_csv(aristocrats_file)
aristocrats_df['category'] = 'Aristocrat'

print(f"Reading {champions_file}...")
champions_df = pd.read_csv(champions_file)
champions_df['category'] = 'Champion'

print(f"Reading {kings_file}...")
kings_df = pd.read_csv(kings_file)
kings_df['category'] = 'King'

# Combine dataframes
print("Combining datasets...")
combined_df = pd.concat([aristocrats_df, champions_df, kings_df], ignore_index=True)

# Sort by symbol (A-Z)
combined_df = combined_df.sort_values(by='symbol')

# Extract payment month from ex-date
def extract_month(date_str):
    if pd.isna(date_str):
        return None
    try:
        date_obj = pd.to_datetime(date_str)
        return date_obj.month
    except:
        return None

def get_month_name(month_num):
    if pd.isna(month_num):
        return None
    try:
        month_name = datetime(2025, int(month_num), 1).strftime('%B')
        return month_name
    except:
        return None

# Add payment month columns
combined_df['payment_month'] = combined_df['payout_next_ex_date'].apply(extract_month)
combined_df['payment_month_name'] = combined_df['payment_month'].apply(get_month_name)

# Reorder columns to have symbol first and category second
all_columns = combined_df.columns.tolist()
all_columns.remove('symbol')
all_columns.remove('category')
reordered_columns = ['symbol', 'category'] + all_columns

# Apply the new column order
combined_df = combined_df[reordered_columns]

# Write to output file
print(f"Writing combined data to {output_file}...")
combined_df.to_csv(output_file, index=False)

print(f"Successfully combined {len(aristocrats_df)} Aristocrats, {len(champions_df)} Champions, and {len(kings_df)} Kings.")
print(f"Total records in combined file: {len(combined_df)}")
print(f"Output saved to {output_file}")

# Print some statistics
print("\nMonthly distribution of dividend payments:")
monthly_counts = combined_df.groupby(['payment_month_name', 'category']).size().unstack(fill_value=0)
print(monthly_counts)
