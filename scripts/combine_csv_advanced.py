import pandas as pd
from datetime import datetime

# Get today's date in the format MMDDYYYY
today_date = datetime.now().strftime('%m%d%Y')

# File paths
aristocrats_file = 'data/DividendAristocrats_02032025.csv'
champions_file = 'data/DividendChampions_02032025.csv'
kings_file = 'data/DividendKings_02032025.csv'
output_file = f'CombinedDividendStocks_{today_date}.csv'

# Read CSV files
print(f"Reading {aristocrats_file}...")
aristocrats_df = pd.read_csv(aristocrats_file)
aristocrats_df['is_aristocrat'] = True

print(f"Reading {champions_file}...")
champions_df = pd.read_csv(champions_file)
champions_df['is_champion'] = True

print(f"Reading {kings_file}...")
kings_df = pd.read_csv(kings_file)
kings_df['is_king'] = True

# Create a unified list of all unique symbols
all_symbols = pd.concat([
    aristocrats_df['symbol'], 
    champions_df['symbol'], 
    kings_df['symbol']
]).unique()

print(f"Found {len(all_symbols)} unique stock symbols across all files")

# Create a new dataframe with one row per unique symbol
result_df = pd.DataFrame({'symbol': all_symbols})

# Initialize category flags
result_df['is_aristocrat'] = False
result_df['is_champion'] = False
result_df['is_king'] = False

# Mark each symbol with its categories
result_df.loc[result_df['symbol'].isin(aristocrats_df['symbol']), 'is_aristocrat'] = True
result_df.loc[result_df['symbol'].isin(champions_df['symbol']), 'is_champion'] = True
result_df.loc[result_df['symbol'].isin(kings_df['symbol']), 'is_king'] = True

# Create a combined category string for each stock
def get_combined_category(row):
    categories = []
    if row['is_aristocrat']:
        categories.append('Aristocrat')
    if row['is_champion']:
        categories.append('Champion')
    if row['is_king']:
        categories.append('King')
    return ', '.join(categories)

result_df['category'] = result_df.apply(get_combined_category, axis=1)

# Now we need to merge in all the other data columns from the original files
# We'll prioritize data from kings, then champions, then aristocrats when there's overlap
print("Merging data from all sources...")
for symbol in result_df['symbol']:
    # Get the row data for this symbol
    king_rows = kings_df[kings_df['symbol'] == symbol]
    champion_rows = champions_df[champions_df['symbol'] == symbol]
    aristocrat_rows = aristocrats_df[aristocrats_df['symbol'] == symbol]
    
    # Prioritize in this order: king, champion, aristocrat
    if not king_rows.empty:
        source_row = king_rows.iloc[0].copy()
    elif not champion_rows.empty:
        source_row = champion_rows.iloc[0].copy()
    elif not aristocrat_rows.empty:
        source_row = aristocrat_rows.iloc[0].copy()
    else:
        # Should never happen
        continue
    
    # Copy all columns except the ones we've already handled
    for col in source_row.index:
        if col not in ['symbol', 'is_aristocrat', 'is_champion', 'is_king', 'category']:
            result_df.loc[result_df['symbol'] == symbol, col] = source_row[col]

# Sort by symbol (A-Z)
result_df = result_df.sort_values(by='symbol')

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
print("Adding payment month information...")
result_df['payment_month'] = result_df['payout_next_ex_date'].apply(extract_month)
result_df['payment_month_name'] = result_df['payment_month'].apply(get_month_name)

# Reorder columns to have symbol first and category second
all_columns = result_df.columns.tolist()
all_columns.remove('symbol')
all_columns.remove('category')
# Remove the individual category flags from the main columns
all_columns.remove('is_aristocrat')
all_columns.remove('is_champion')
all_columns.remove('is_king')
reordered_columns = ['symbol', 'category'] + all_columns

# Apply the new column order
final_df = result_df[reordered_columns]

# Write to output file
print(f"Writing combined data to {output_file}...")
final_df.to_csv(output_file, index=False)

print(f"Successfully combined stock data with multiple category labels.")
print(f"Total unique stocks in combined file: {len(final_df)}")
print(f"Output saved to {output_file}")

# Print some statistics
print("\nStock counts by category:")
aristocrat_count = sum(final_df['category'].str.contains('Aristocrat'))
champion_count = sum(final_df['category'].str.contains('Champion'))
king_count = sum(final_df['category'].str.contains('King'))
print(f"Aristocrats: {aristocrat_count}")
print(f"Champions: {champion_count}")
print(f"Kings: {king_count}")

# Print some examples of multi-category stocks
multi_category = final_df[final_df['category'].str.contains(',')]
if len(multi_category) > 0:
    print("\nExamples of stocks with multiple categories:")
    for i, row in multi_category.head(5).iterrows():
        print(f"{row['symbol']}: {row['category']}")

# Print monthly distribution
print("\nMonthly distribution of dividend payments:")
monthly_counts = final_df.groupby('payment_month_name').size()
print(monthly_counts)
