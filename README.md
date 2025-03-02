# Dividend Stocks Data Processing

A simple Python utility for processing and combining dividend stock data from multiple CSV files.

## Project Description

This project provides Python scripts to combine data from three CSV files containing information about dividend stocks categorized as Aristocrats, Champions, and Kings. The scripts add category labels to each stock and create a consolidated CSV file for easier analysis.

The solution can extract payment month information from ex-dividend dates and provide statistics on the monthly distribution of payments across categories.

## Project Structure

```
dividend-stocks/
│
├── data/                          # Data directory
│   ├── DividendAristocrats_02032025.csv   # Dividend Aristocrats data
│   ├── DividendChampions_02032025.csv     # Dividend Champions data
│   ├── DividendKings_02032025.csv          # Dividend Kings data
│   └── CombinedDividendStocks.csv         # Output combined file (generated)
│
├── scripts/                       # Python scripts
│   ├── combine_csv_simple.py      # Simple version of the CSV combiner
│   └── combine_csv_advanced.py    # Advanced version with additional processing
│
├── README.md                      # This file
└── requirements.txt               # Project dependencies
```

## Requirements

- Python 3.6 or higher
- pandas library

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Simple Combiner

Run the simple version that just adds category labels and combines the files:

```bash
python scripts/combine_csv_simple.py
```

### Advanced Combiner

Run the advanced version with payment month extraction and statistics:

```bash
python scripts/combine_csv_advanced.py
```

## Input Data

The project expects three input CSV files with dividend stock data:

1. `DividendAristocrats_02032025.csv` - Dividend Aristocrats (stocks with 25+ years of dividend increases)
2. `DividendChampions_02032025.csv` - Dividend Champions (stocks with similar criteria as Aristocrats)
3. `DividendKings_02032025.csv` - Dividend Kings (stocks with 50+ years of dividend increases)

Each file contains extensive information about the stocks, including:
- Stock symbols and names
- Sector and industry classifications
- Dividend yield and payment information
- Ex-dividend and payment dates
- Years of consecutive dividend growth
- Price information

## Output

The scripts generate a combined CSV file (`CombinedDividendStocks.csv`) with all stocks and a new `category` column indicating whether each stock is an Aristocrat, Champion, or King.

The advanced script also adds:
- `payment_month` - Numerical month (1-12) derived from the ex-dividend date
- `payment_month_name` - Month name (January-December)

## Example Code

Simple version:

```python
import pandas as pd

# Read CSV files
aristocrats_df = pd.read_csv('data/DividendAristocrats_02032025.csv')
aristocrats_df['category'] = 'Aristocrat'

champions_df = pd.read_csv('data/DividendChampions_02032025.csv')
champions_df['category'] = 'Champion'

kings_df = pd.read_csv('data/DividendKings_02032025.csv')
kings_df['category'] = 'King'

# Combine dataframes
combined_df = pd.concat([aristocrats_df, champions_df, kings_df], ignore_index=True)

# Write to output file
combined_df.to_csv('data/CombinedDividendStocks.csv', index=False)

print(f"Combined CSV file created successfully with {len(combined_df)} stocks.")
```

## Notes

- There may be overlap between categories (some stocks may appear in multiple input files)
- The current implementation preserves all duplicates in the combined output
- To get a summary of dividend payments by month and category, use the advanced script

## Data Summary

Based on the analysis of the input files:
- Most dividend payments occur in March, April, and May
- Dividend Champions are the largest category with 124 stocks
- Dividend Kings are the smallest category with 51 stocks
- Dividend Aristocrats include 50 stocks
