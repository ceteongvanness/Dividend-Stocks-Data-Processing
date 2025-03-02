import pandas as pd

# Read CSV files
aristocrats_df = pd.read_csv('DividentAristocrats_02032025.csv')
aristocrats_df['category'] = 'Aristocrat'

champions_df = pd.read_csv('DividentChampions_02032025.csv')
champions_df['category'] = 'Champion'

kings_df = pd.read_csv('DividentKing_02032025.csv')
kings_df['category'] = 'King'

# Combine dataframes
combined_df = pd.concat([aristocrats_df, champions_df, kings_df], ignore_index=True)

# Write to output file
combined_df.to_csv('CombinedDividendStocks.csv', index=False)

print(f"Combined CSV file created successfully with {len(combined_df)} stocks.")
