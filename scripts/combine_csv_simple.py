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
aristocrats_df = pd.read_csv(aristocrats_file)
aristocrats_df['is_aristocrat'] = True

champions_df = pd.read_csv(champions_file)
champions_df['is_champion'] = True

kings_df = pd.read_csv(kings_file)
kings_df['is_king'] = True

# Create a unified list of all unique symbols
all_symbols = pd.concat([
    aristocrats_df['symbol'], 
    champions_df['symbol'], 
    kings_df['symbol']
]).unique()

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

# Now merge in all the other data columns
for symbol in result_df['symbol']:
    # Get the row data for this symbol (prioritize kings, then champions, then aristocrats)
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
        continue
    
    # Copy all columns except the ones we've already handled
    for col in source_row.index:
        if col not in ['symbol', 'is_aristocrat', 'is_champion', 'is_king', 'category']:
            result_df.loc[result_df['symbol'] == symbol, col] = source_row[col]

# Sort by symbol (A-Z)
result_df = result_df.sort_values(by='symbol')

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
final_df.to_csv(output_file, index=False)

print(f"Combined CSV file created successfully with {len(final_df)} unique stocks.")
print(f"Output saved to: {output_file}")