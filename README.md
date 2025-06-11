# Live Stock Data Fetcher

This script fetches and displays near real-time stock data from Yahoo Finance using the `yfinance` library.

## Features

*   Fetches key stock information (current price, day's high/low, volume, open, previous close).
*   Accepts a stock ticker symbol as a command-line argument.
*   Basic error handling for invalid tickers or network issues.

## Setup

### 1. Create a Virtual Environment (Recommended)

It's recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

*   On Windows:
    ```bash
    .\venv\Scripts\activate
    ```
*   On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```

### 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line, providing a stock ticker symbol as an argument. The ticker symbol will be converted to uppercase by the script.

```bash
python stock_fetcher.py <TICKER_SYMBOL>
```

### Examples:

*   Fetch data for Apple Inc. (AAPL):
    ```bash
    python stock_fetcher.py AAPL
    ```

*   Fetch data for Microsoft Corp. (MSFT):
    ```bash
    python stock_fetcher.py msft
    ```

*   Fetch data for SPDR S&P 500 ETF Trust (SPY):
    ```bash
    python stock_fetcher.py SPY
    ```

*   Fetch data for Bitcoin USD (BTC-USD):
    ```bash
    python stock_fetcher.py BTC-USD
    ```

## Output Example (for AAPL)

```
Data for AAPL:
  Current Price: 170.34
  Day's Low: 168.49
  Day's High: 171.27
  Volume: 52048292
  Market Open: 169.58
  Previous Close: 169.3
```
*(Note: Output values are illustrative and will vary based on current market data.)*

## Disclaimer

This script uses the `yfinance` library, which accesses data from Yahoo Finance. Data accuracy and availability depend on Yahoo Finance. Remember that financial data provided by Yahoo Finance can be delayed and is intended for personal, informational purposes only. Refer to Yahoo!'s terms of service for more details.
---

## Supertrend Analyzer (`supertrend_analyzer.py`)

This script performs a technical analysis using the Supertrend indicator on historical stock data. It calculates the Supertrend, identifies bullish/bearish trends and flip points, prints this analysis to the console, and generates a plot visualizing the closing price, Supertrend line, and buy/sell signals.

### Dependencies for Supertrend Analyzer

In addition to the common dependencies (`yfinance`, `requests`, `setuptools`), this script requires:

*   `pandas`
*   `pandas_ta` (for technical indicators)
*   `matplotlib` (for plotting)
*   `Pillow` (a dependency for `matplotlib` for image processing)
*   `numpy` (specifically a version less than 2.0, e.g., `numpy<2.0`, due to compatibility with `pandas_ta 0.3.14b0`)

Ensure these are installed, typically via:
`pip install -r requirements.txt`

### Usage for `supertrend_analyzer.py`

Run the script from the command line. You can specify the ticker symbol, historical data period, ATR length for Supertrend, and the Supertrend multiplier.

```bash
python supertrend_analyzer.py [--ticker TICKER] [--period PERIOD] [--atr_length LENGTH] [--multiplier MULTIPLIER]
```

**Command-Line Arguments:**

*   `--ticker`: Stock ticker symbol (e.g., MSFT, AAPL). Default: `MSFT`.
*   `--period`: Period for historical data (e.g., '1mo', '6mo', '1y', '5y', 'max'). Default: `1y`.
*   `--atr_length`: ATR period length for Supertrend calculation. Default: `10`.
*   `--multiplier`: Multiplier for the ATR to calculate Supertrend bands. Default: `3.0`.

**Examples:**

*   Run with default parameters (MSFT, 1 year, ATR 10, Multiplier 3):
    ```bash
    python supertrend_analyzer.py
    ```

*   Run for Apple (AAPL) for the last 2 years, with ATR length 7 and multiplier 2.5:
    ```bash
    python supertrend_analyzer.py --ticker AAPL --period 2y --atr_length 7 --multiplier 2.5
    ```

**Output:**

1.  **Console Output**: The script will print:
    *   Details of the ticker and parameters being used.
    *   A list of "Buy Flip Dates".
    *   A list of "Sell Flip Dates".
    *   A summary of "Trend Segments" (bullish/bearish with start and end dates).
2.  **Plot File**: A PNG image file will be saved in the script's directory, named according to the ticker and parameters (e.g., `MSFT_supertrend_P1y_ATR10_M3.0_plot.png`). This plot shows:
    *   The stock's closing prices.
    *   The Supertrend indicator line.
    *   Buy signals (green upward arrows) and Sell signals (red downward arrows) at flip points.

### Interpreting the Supertrend Output

*   **Supertrend Line**: When the price is above the Supertrend line, it generally indicates an uptrend. When the price is below, it indicates a downtrend.
*   **Flips**:
    *   A "Buy Flip" occurs when the trend changes from bearish to bullish.
    *   A "Sell Flip" occurs when the trend changes from bullish to bearish.
*   **Trend Segments**: These show the duration of continuous bullish or bearish periods as identified by the indicator.

**Disclaimer**: Technical analysis tools like Supertrend provide insights but do not guarantee future performance. Use this information as part of a broader investment strategy.
