import pandas as pd
from datetime import datetime

# Get today's date in the format MMDDYYYY
today_date = datetime.now().strftime('%m%d%Y')

# Generate output filename with today's date
output_file = f'CombinedDividendStocks_{today_date}.csv'

# Read CSV files
aristocrats_df = pd.read_csv('data/DividendAristocrats_02032025.csv')
aristocrats_df['category'] = 'Aristocrat'

champions_df = pd.read_csv('data/DividendChampions_02032025.csv')
champions_df['category'] = 'Champion'

kings_df = pd.read_csv('data/DividendKings_02032025.csv')
kings_df['category'] = 'King'

# Combine dataframes
combined_df = pd.concat([aristocrats_df, champions_df, kings_df], ignore_index=True)

# Sort by symbol (A-Z)
combined_df = combined_df.sort_values(by='symbol')

# Reorder columns to have symbol first and category second
all_columns = combined_df.columns.tolist()
all_columns.remove('symbol')
all_columns.remove('category')
reordered_columns = ['symbol', 'category'] + all_columns

# Apply the new column order
combined_df = combined_df[reordered_columns]

# Write to output file
combined_df.to_csv(output_file, index=False)

print(f"Combined CSV file created successfully with {len(combined_df)} stocks.")
print(f"Output saved to: {output_file}")
