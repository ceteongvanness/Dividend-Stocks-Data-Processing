# Dividend Stocks Data Processing

A simple Python utility for processing and combining dividend stock data from multiple CSV files.

## Project Description

This project provides Python scripts to combine data from three CSV files containing information about dividend stocks categorized as Aristocrats, Champions, and Kings. The scripts add category labels to each stock and create a consolidated CSV file for easier analysis.

The solution can extract payment month information from ex-dividend dates and provide statistics on the monthly distribution of payments across categories.

## Project Structure

```
Dividend-Stocks-Data-Processing/
│
├── data/                          # Data directory
│   ├── DividentAristocrats_02032025.csv   # Dividend Aristocrats data
│   ├── DividentChampions_02032025.csv     # Dividend Champions data
│   ├── DividentKing_02032025.csv          # Dividend Kings data
│   └── CombinedDividendStocks_*.csv       # Output combined file (generated with date)
│
├── scripts/                       # Python scripts
│   ├── combine_csv_simple.py      # Simple version of the CSV combiner
│   ├── combine_csv_advanced.py    # Advanced version with additional processing
│   └── combine_csv_multi_category.py      # Full version with advanced features
│
├── .github/workflows/             # GitHub Actions workflows
│   └── process-dividend-stocks.yml # Automated workflow configuration
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

### Multi-Category Combiner

Run the full version that handles multiple categories per stock with detailed analysis:

```bash
python scripts/combine_csv_multi_category.py
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

## GitHub Actions Automation
The project includes a GitHub Actions workflow that:
1. Runs automatically on schedule or when code is pushed
2. Processes the CSV files using the specified script
3. Creates a zip file of the results
4. Uploads the zip as an artifact for download
5. Commits the updated combined CSV file to the repository

To access the zip file:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select the latest workflow run
4. Download the artifact from the run summary

## Example Code

Multi-category handling:

```python
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
```

## Notes

- Many stocks appear in multiple input files (overlap between categories)
- This implementation preserves all category memberships in the combined output
- For stocks in multiple categories, data is prioritized from Kings, then Champions, then Aristocrats
- The output filename includes the current date (MMDDYYYY format)

## Data Summary

Based on the analysis of the input files:
- Most dividend payments occur in March, April, and May
- Dividend Champions are the largest category with 124 stocks
- Dividend Kings are the smallest category with 51 stocks
- Dividend Aristocrats include 50 stocks
- Many stocks belong to multiple categories (e.g., both Aristocrat and Champion)
